from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os
import re

from utils.config_loader import load_extraction_config
from models import Session, Parent, Child, Enquiry, PipelineStage, Email
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
from utils.entity_extraction import extract_entities_with_gpt
from utils.crm_upsert import upsert_parent, upsert_child

reply_bp = Blueprint('reply_bp', __name__)

# Lazy load KB embeddings and metadata
doc_embeddings, metadata = None, None
def load_kb_once():
    global doc_embeddings, metadata
    if doc_embeddings is None or metadata is None:
        doc_embeddings, metadata = load_kb()
load_kb_once()

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

def normalize_keys(d: dict) -> dict:
    """Normalize dictionary keys by stripping and converting to snake_case."""
    return {k.strip().lower().replace(" ", "_"): v for k, v in d.items()}

@reply_bp.route("/inbox/email/<int:email_id>/dismiss", methods=["POST"])
def dismiss_email(email_id):
    """Handle email dismissal."""
    session = Session()
    try:
        # Get current user info
        user_id = request.json.get('user_id') or 'system'
        
        # Find the email
        email = session.query(Email).filter_by(id=email_id).first()
        
        if not email:
            return jsonify({"error": "Email not found"}), 404
            
        # Update email status using dismiss method
        email.dismiss(user_id=user_id)
        session.commit()
        
        return jsonify({
            "success": True,
            "message": "Email dismissed successfully",
            "email_id": email_id,
            "status": email.status
        })
        
    except Exception as e:
        print(f"❌ DISMISS EMAIL ERROR: {str(e)}")
        session.rollback()
        return jsonify({"error": str(e)}), 500
        
    finally:
        session.close()

@reply_bp.route("/reply/email", methods=["POST"])
def generate_reply():
    session = Session()
    try:
        body = request.get_json(force=True)
        print(f"DEBUG: Received request body: {json.dumps(body, indent=2)}")
        
        question_raw = (body.get("message") or "").strip()
        form_data = body.get("form_data")
        url_box_text = (body.get("url_box") or "").strip()
        url_map = parse_url_box(url_box_text)
        instruction_raw = (body.get("instruction") or "").strip()
        customer_id = body.get("customer_id", "LOCAL-TEST")

        if not question_raw and not form_data:
            return jsonify({"error": "No message or form data provided."}), 400

        question = remove_personal_info(question_raw)
        instruction = remove_personal_info(instruction_raw)

        # Load customer extraction config
        extraction_config = load_extraction_config(customer_id)
        extracted_data = extract_entities_with_gpt(client, question_raw, extraction_config)
        print(f"DEBUG: Initial extraction result: {json.dumps(extracted_data, indent=2)}")

        extracted_data = normalize_keys(extracted_data)
        
        # Enhanced email extraction with fallbacks
        if not extracted_data.get("parent_email"):
            email = (
                extract_any_email_from_dict(form_data) or
                extract_email_from_text(question_raw) or
                extract_any_email_from_dict(extracted_data) or
                "unknown@noemail.com"
            )
            extracted_data["parent_email"] = email

        # Build parent data with improved defaults
        parent_data = {
            "name": extracted_data.get("parent_name") or extracted_data.get("name", "Unknown Parent"),
            "email": extracted_data.get("parent_email"),
            "phone": extracted_data.get("parent_phone") or extracted_data.get("phone", "")
        }

        # Always unpack tuple from upsert_parent
        parent, is_new_parent = upsert_parent(session, customer_id, parent_data)

        # Handle child data if present
        child = None
        if any(k for k in extracted_data.keys() if 'child' in k):
            child_info = extracted_data
            child_data = {
                "name": child_info.get("child_name") or child_info.get("name", ""),
                "year_group": child_info.get("child_year_group") or child_info.get("year_group", "")
            }
            if any(child_data.values()):
                child, is_new_child = upsert_child(session, customer_id, parent.id, child_data)

        # Create enquiry record
        pipeline_stage = session.query(PipelineStage).filter_by(name="New").first()
        enquiry = Enquiry(
            customer_id=customer_id,
            parent_id=parent.id,
            child_id=child.id if child else None,
            enquiry_date=datetime.utcnow(),
            source="form" if form_data else "email",
            raw_text=question_raw,
            pipeline_stage_id=pipeline_stage.id if pipeline_stage else None
        )
        session.add(enquiry)
        session.commit()

        # Get relevant knowledge base context
        q_vec = embed_text(question, client, EMBED_MODEL)
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

        # Build CRM summary
        crm_summary = f"Parent: {parent.name} ({parent.email})\n"
        if child:
            crm_summary += f"Child: {child.name}, Year Group: {child.year_group or 'N/A'}\n"
        crm_summary += f"Enquiry received on {enquiry.enquiry_date.strftime('%d %B %Y')}\n"
        crm_summary += f"Additional info: {extracted_data.get('additional_comments', '')}"

        # Load customer-specific config
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

        # Compose GPT prompt
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

Original message or form data:
\"\"\"
{question_raw}

School Info:
\"\"\"
{top_context}
\"\"\"

Sign off:
{sign_off}
""".strip()

        # Generate reply
        reply_md = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        ).choices[0].message.content.strip()

        reply_md = clean_gpt_email_output(reply_md)
        reply_md = insert_links(reply_md, url_map)
        reply_html = markdown_to_html(reply_md)

        return jsonify({"reply": reply_html})

    except Exception as e:
        print(f"❌ REPLY ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()