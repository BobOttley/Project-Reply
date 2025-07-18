# email.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Session, Email
import os
from dotenv import load_dotenv
from utils.email_sync import fetch_and_upsert_emails


# Load environment variables from .env file
load_dotenv()

email_bp = Blueprint('email_bp', __name__)

@email_bp.route("/inbox/email/<int:email_id>/dismiss", methods=["POST"])
def dismiss_email(email_id):
    """Handle email dismissal."""
    session = Session()
    try:
        email = session.query(Email).filter_by(id=email_id).first()
        if not email:
            return jsonify({"error": "Email not found"}), 404
        if request.is_json:
            data = request.get_json()
            dismissed_by = data.get('dismissed_by', 'RobertOttley')
        else:
            dismissed_by = 'RobertOttley'
        email.status = 'dismissed'
        email.dismissed_at = datetime.utcnow()
        email.dismissed_by = dismissed_by
        session.commit()
        return jsonify({
            "success": True,
            "message": "Email dismissed successfully",
            "email_id": email_id,
            "status": email.status,
            "dismissed_at": email.dismissed_at.isoformat() if email.dismissed_at else None,
            "dismissed_by": email.dismissed_by
        })
    except Exception as e:
        session.rollback()
        print(f"❌ DISMISS EMAIL ERROR: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        session.close()

@email_bp.route("/inbox/email/<int:email_id>", methods=["GET"])
def get_email(email_id):
    """Get email details."""
    session = Session()
    try:
        email = session.query(Email).filter_by(id=email_id).first()
        if not email:
            return jsonify({"error": "Email not found"}), 404
        return jsonify({
            "id": email.id,
            "subject": email.subject,
            "from_address": email.from_address,
            "body": email.body,
            "status": email.status,
            "date_received": email.date_received.isoformat() if email.date_received else None,
            "dismissed": email.status == 'dismissed',
            "dismissed_at": email.dismissed_at.isoformat() if email.dismissed_at else None,
            "dismissed_by": email.dismissed_by
        })
    except Exception as e:
        print(f"❌ GET EMAIL ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@email_bp.route("/inbox", methods=["GET"])
def get_inbox():
    """Get inbox contents."""
    session = Session()
    try:
        emails = session.query(Email).filter(
            Email.status != 'dismissed'
        ).order_by(Email.date_received.desc()).all()
        return jsonify([{
            "id": email.id,
            "subject": email.subject,
            "from_address": email.from_address,
            "body": email.body,
            "date_received": email.date_received.isoformat() if email.date_received else None,
            "status": email.status
        } for email in emails])
    except Exception as e:
        print(f"❌ GET INBOX ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@email_bp.route("/sync-emails", methods=["POST"])
def sync_emails():
    """Manually fetch latest emails from IMAP and insert into DB."""
    try:
        data = request.get_json() or {}
        customer_id = data.get("customer_id", "LOCAL-TEST")
        imap_host = os.getenv("IMAP_SERVER")
        imap_port = int(os.getenv("IMAP_PORT", "993"))
        imap_user = os.getenv("EMAIL_ACCOUNT")
        imap_pass = os.getenv("EMAIL_PASSWORD")

        if not all([imap_host, imap_user, imap_pass]):
            return jsonify({"success": False, "error": "Missing IMAP configuration"}), 500

        fetch_and_upsert_emails(customer_id, imap_host, imap_user, imap_pass)
        return jsonify({"success": True})
    except Exception as e:
        print(f"❌ SYNC EMAILS ERROR: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
