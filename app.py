# === app.py ===

import os
from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_cors import CORS

# === Modular Blueprint Imports ===
from routes.reply import reply_bp
from routes.revise import revise_bp
from routes.save_standard import save_standard_bp
from routes.email import email_bp
from routes.reply_email import reply_email_bp
from routes.reply_form import reply_form_bp


# === Flask App Initialisation ===
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# === Register Blueprints ===
app.register_blueprint(reply_bp)
app.register_blueprint(revise_bp)
app.register_blueprint(save_standard_bp)
app.register_blueprint(email_bp)
app.register_blueprint(reply_email_bp)
app.register_blueprint(reply_form_bp)

# === Serve Frontend (index.html) ===
@app.route("/")
def index():
    return render_template("index.html")

# === Static Files (optional, Flask serves static/ automatically) ===
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# === Healthcheck (optional) ===
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# === Error Handlers ===
@app.errorhandler(404)
def not_found(e):
    # API or SPA fallback
    if request.path.startswith('/api') or request.path.startswith('/inbox') or request.path.startswith('/reply'):
        return jsonify({"error": "Not found"}), 404
    return render_template("index.html"), 200

@app.errorhandler(500)
def server_error(e):
    if request.path.startswith('/api') or request.path.startswith('/inbox') or request.path.startswith('/reply'):
        return jsonify({"error": "Internal server error"}), 500
    return render_template("index.html"), 500

# === Main Runner ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
