# === routes/save_standard.py ===

from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import json
from config import EMBED_MODEL, client
from utils.helpers import remove_personal_info, embed_text

save_standard_bp = Blueprint('save_standard_bp', __name__)

@save_standard_bp.route("/save-standard", methods=["POST"])
def save_standard():
    try:
        body = request.get_json(force=True)
        msg_raw = (body.get("message") or "").strip()
        reply   = (body.get("reply")   or "").strip()

        if not (msg_raw and reply):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        msg_redacted = remove_personal_info(msg_raw)

        # Append & persist
        record = {
            "timestamp": datetime.now().isoformat(),
            "message": msg_redacted,
            "reply": reply
        }
        path = "standard_responses.json"
        data = []
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
        data.append(record)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        # In-memory update if needed (handled elsewhere in prod)
        # You may need to reload in-memory if you use it.

        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"❌ SAVE ERROR: {e}")
        return jsonify({"status": "error", "message": "Save failed"}), 500
