from flask import Blueprint, request, jsonify
from datetime import datetime
import os

from models import Session, Email

email_bp = Blueprint('email_bp', __name__)

@email_bp.route("/inbox/email/<int:email_id>/dismiss", methods=["POST"])
def dismiss_email(email_id):
    """Handle email dismissal."""
    session = Session()
    try:
        # Get the email
        email = session.query(Email).filter_by(id=email_id).first()
        
        if not email:
            return jsonify({"error": "Email not found"}), 404
        
        # Set dismissal information
        email.status = 'dismissed'
        email.dismissed_at = datetime.utcnow()
        email.dismissed_by = 'RobertOttley'  # Using your actual login
        
        # Commit changes
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
        return jsonify({"error": str(e)}), 500
        
    finally:
        session.close()