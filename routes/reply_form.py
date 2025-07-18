from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os
import re

from utils.config_loader import load_extraction_config
from models import Session, Parent, Child, Enquiry, PipelineStage
from config import client, EMBED_MODEL, SIMILARITY_THRESHOLD, RESPONSE_LIMIT, load_kb
from utils.helpers import (
    parse_url_box,
    insert_links,
    remove_personal_info,
    embed_text,
    markdown_to_html,
    clean_gpt_email_output,
    cosine_similarity
)
from utils.crm_upsert import upsert_parent, upsert_child

reply_form_bp = Blueprint('reply_form_bp', __name__)

# Lazy load KB embeddings and metadata once
doc_embeddings, metadata = None, None
def load_kb_once():
    global doc_embeddings, metadata
    if doc_embeddings is None or metadata is None:
        doc_embeddings, metadata = load_kb()
load_kb_once()

def normalize_keys(d: dict) -> dict:
    """Normalize dictionary keys by stripping and converting to snake_case."""
    return {k.strip().lower().replace(" ", "_"): v for k, v in d.items()}

def extract_email_from_text(text: str) -> str | None:
    """Extract email from text using regex pattern."""
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None

def extract_any_email_from_dict(data: dict) -> str | None:
    """Recursively find any valid email in a nested dict or string."""
    if not data:
        return None
    flat = json.dumps(data, ensure_ascii=False)
    found = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', flat)
    return found[0] if found else None

@reply_form_bp.route("/reply/form", methods=["POST"])
def reply_to_form():
    session = Session()
    try:
        body = request.get_json(force=True)
        print(f"DEBUG: Received request body: {json.dumps(body, indent=2)}")
        
        form_data = body.get("form_data")
        url_box_text = (body.get("url_box") or "").strip()
        url_map = parse_url_box(url_box_text)
        instruction_raw = (body.get("instruction") or "").strip()
        customer_id = body.get("customer_id", "LOCAL-TEST")

        if not form_data:
            return jsonify({"error": "No form data provided."}), 400

        # Normalize form keys
        form_data = normalize_keys(form_data)

        # Remove any personal info if needed from fields
        for key in form_data:
            if isinstance(form_data[key], str):
                form_data[key] = remove_personal_info(form_data[key])

        # Enhanced email extraction with multiple fallbacks
        parent_email = (
            form_data.get("parent_email") or
            form_data.get("email") or
            extract_email_from_text(json.dumps(form_data)) or
            extract_any_email_from_dict(form_data) or
            "unknown@noemail.com"
        )

        # Build parent and child data with improved defaults
        parent_data = {
            "name": form_data.get("parent_name") or form_data.get("name", "Unknown Parent"),
            "email": parent_email,
            "phone": form_data.get("parent_phone") or form_data.get("phone", "")
        }

        child_data = {
            "name": form_data.get("child_name") or form_data.get("name", ""),
            "year_group": form_data.get("child_year_group") or form_data.get("year_group", "")
        }

        # Upsert parent and child
        parent = upsert_parent(session, customer_id, parent_data)
        child = None
        if any(child_data.values()):
            child = upsert_child(session, customer_id, parent.id, child_data)

        # Create enquiry record
        pipeline_stage = session.query(PipelineStage).filter_by(name="New").first()
        enquiry = Enquiry(
            customer_id=customer_id,
            parent_id=parent.id,
            child_id=child.id if child else None,
            enquiry_date=datetime.utcnow(),
            source="form",
            raw_text=json.dumps(form_data),
            pipeline_stage_id=pipeline_stage.id if pipeline_stage else None
        )
        session.add(enquiry)
        session.commit()

        # Prepare input text summary for embedding and prompt
        input_text = json.dumps(form_data, indent=2)

        # Retrieve top knowledge base context
        q_vec = embed_text(input_text, client, EMBED_MODEL)
        sims = [(cosine_similarity(q_vec, vec), meta) for vec, meta in zip(doc_embeddings, metadata)]
        top = [m for m in sims if m[0] >= SIMILARITY_THRESHOLD]
        top = sorted(top, key=lambda x: x[0], reverse=True)[:RESPONSE_LIMIT]

        if top:
            context_blocks = [
                f"{m['text']}\n[Info source]({m.get('url', '')})" if m.get('url') else m['text']
                for _, m in top
            ]
            top_context = "\n---\n".join(context_blocks)
        else:
            top_context = ""

        # Load school config with defaults
        config_path = os.path.join("config", f"extraction_config_{customer_id}.json")
        try:
            with open(config_path, "r") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}

        staff_name = cfg.get("staff_name", "Admissions Team")
        job_title = cfg.get("job_title", "Admissions")
        school_name = cfg.get("school_name", "the School")
        school_type = cfg.get("school_type", "school")
        sign_off = cfg.get("sign_off", "The Admissions Team")
        rules_block = cfg.get("rules_block", "- Only use school-approved information. Never hallucinate.")

        crm_summary = f"Parent: {parent.name} ({parent.email})\n"
        if child:
            crm_summary += f"Child: {child.name}, Year Group: {child.year_group or 'N/A'}\n"
        crm_summary += f"Enquiry received on {enquiry.enquiry_date.strftime('%d %B %Y')}\n"
        crm_summary += f"Additional info: {form_data.get('additional_comments', '')}"

        prompt = f"""
TODAY'S DATE IS {datetime.utcnow().strftime('%d %B %Y')}.

You are {staff_name}, {job_title} at {school_name}, a {school_type}.

Write a warm, professional email reply to the prospective family based on the enquiry details below.
Use only the approved school information provided.

Rules:
{rules_block}

Enquiry details:
\"\"\"
{crm_summary}

Original form data:
\"\"\"
{input_text}

School Info:
\"\"\"
{top_context}
\"\"\"

Sign off:
{sign_off}
""".strip()

        reply_md = client.chat.completions.create(
            model="gpt-4",  # Changed from gpt-4o-mini
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        ).choices[0].message.content.strip()

        reply_md = clean_gpt_email_output(reply_md)
        reply_md = insert_links(reply_md, url_map)
        reply_html = markdown_to_html(reply_md)

        return jsonify({"reply": reply_html})

    except Exception as e:
        print(f"❌ REPLY FORM ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()