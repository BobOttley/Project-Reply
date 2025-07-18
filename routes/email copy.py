# routes/email.py

from flask import Blueprint, request, jsonify
from utils.helpers import (
    fetch_emails,
    fetch_single_email,   # <-- This import was missing before
    save_email,
    dismiss_email
)

email_bp = Blueprint("email", __name__)

@email_bp.route("/inbox", methods=["GET"])
def inbox():
    customer_id = request.args.get("customer_id")
    emails = fetch_emails(customer_id)
    return jsonify(emails)

@email_bp.route("/sync", methods=["POST"])
def sync():
    data = request.get_json()
    customer_id = data.get("customer_id")
    synced = sync_emails_for_customer(customer_id)
    return jsonify({"synced": synced})

@email_bp.route("/inbox/email/<int:email_id>", methods=["GET"])
def get_email(email_id):
    customer_id = request.args.get("customer_id")
    email = fetch_single_email(customer_id, email_id)
    return jsonify(email)

@email_bp.route("/inbox/email/<int:email_id>/dismiss", methods=["POST"])
def dismiss(email_id):
    customer_id = request.get_json().get("customer_id")
    dismiss_email(customer_id, email_id)
    return jsonify({"status": "dismissed"})

# Dummy sync for progress (remove or update if you implement real sync logic)
def sync_emails_for_customer(customer_id):
    # No-op for now. You can implement real IMAP logic later.
    return True
