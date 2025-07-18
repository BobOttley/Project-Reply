from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os

from models import Session, Parent, Child, Enquiry
from config import client
from utils.helpers import (
    remove_personal_info,
    parse_url_box,
    clean_gpt_email_output,
    insert_links,
    markdown_to_html
)
from utils.crm_upsert import upsert_parent, upsert_child
from utils.entity_extraction import extract_entities_with_gpt
# Add your extraction config loader if needed

revise_bp = Blueprint('revise_bp', __name__)

@revise_bp.route("/revise", methods=["POST"])
def revise():
    session = Session()
    try:
        body = request.get_json(force=True)
        message_raw = (body.get("message") or "").strip()
        prev_reply = (body.get("previous_reply") or "").strip()
        instruction_raw = (body.get("instruction") or "").strip()
        url_box_text = (body.get("url_box") or "").strip()
        form_data = body.get("form_data")
        customer_id = body.get("customer_id", "LOCAL-TEST")

        if not prev_reply:
            return jsonify({"error": "Missing previous reply."}), 400
        if not (message_raw or form_data):
            return jsonify({"error": "Missing enquiry message or form data."}), 400

        message = remove_personal_info(message_raw)
        instruction = remove_personal_info(instruction_raw)
        url_map = parse_url_box(url_box_text)

        # Compose input text for extraction
        input_text = message if message else json.dumps(form_data)

        # Optionally do entity extraction to get CRM context (if you want to update CRM here)
        customer_extraction_config = load_extraction_config(customer_id)  # Implement this
        extracted_data = extract_entities_with_gpt(client, input_text, customer_extraction_config)

        # Upsert parent/child if needed (optional in revise)
        parent = upsert_parent(session, customer_id, extracted_data.get("parent", {}))
        child = None
        if "child" in extracted_data:
            child = upsert_child(session, customer_id, parent.id, extracted_data.get("child", {}))

        # Build CRM summary for prompt (you can customize as needed)
        crm_summary = f"Parent: {parent.name} ({parent.email})\n"
        if child:
            crm_summary += f"Child: {child.name}, Year Group: {child.year_group or 'N/A'}\n"

        prompt = f"""
Revise the admissions reply below according to the instruction.

Instruction: {instruction}

Enquiry details:
\"\"\"
{crm_summary}

Original message or form data:
\"\"\"
{input_text}

Current reply (Markdown):
\"\"\"
{prev_reply}
\"\"\"

Return only the revised reply in Markdown.
""".strip()

        new_md = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        ).choices[0].message.content.strip()

        new_md = clean_gpt_email_output(new_md)
        new_md_linked = insert_links(new_md, url_map)

        return jsonify({"reply": markdown_to_html(new_md_linked)})

    except Exception as e:
        print(f"❌ REVISION ERROR: {e}")
        return jsonify({"error": "Revision failed."}), 500
    finally:
        session.close()
