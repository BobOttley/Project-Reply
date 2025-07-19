Smart Reply
Smart Reply is a modular, multi-tenant AI-powered admissions assistant for independent schools. It automates parent email replies, manages CRM data, integrates with your inbox, and enables personalised, professional communication—all through a fast, modern web UI.

🚀 Features
AI-Powered Replies – Generates warm, professional parent replies using OpenAI GPT models.

Entity Extraction – Parses emails and forms for parent/child names, interests, year group, etc.

Inbox Sync – Connects to IMAP or AWS WorkMail to import and manage live emails.

Sentiment Scoring – Classifies tone and sentiment to guide more human replies.

Static & AI Replies – Uses pre-approved standard replies or GPT-generated fallback responses.

Revision Flow – Enables edits, refinements, CTA suggestions, and final review before sending.

Smart Save – Allows saving refined replies to improve future matches.

Multi-Tenant – Seamlessly handles multiple schools or groups via customer-specific configs.

Modular Architecture – Easy to extend with CRM, events, analytics, dashboards, etc.

🧠 Tech Stack
Backend: Python 3.11+, Flask, SQLAlchemy, SQLite (or Postgres)

AI Models: OpenAI GPT (gpt-4o-mini), text-embedding-3-small

Frontend: HTML, CSS, JS (modular Smart Reply UI)

Storage: Local filesystem (embeddings, configs) + SQL DB (email, CRM)

Email Sync: IMAP or AWS WorkMail (via imap-tools)

Deployment: GitHub + Render

📁 Project Structure
bash
Copy
Edit
project_root/
├── app.py                         # Main Flask entrypoint
├── config.py                      # OpenAI + environment config
├── models.py                      # SQLAlchemy models
├── requirements.txt               # All pip dependencies
├── runtime.txt                    # Python version for Render
├── .env                           # Local environment variables
│
├── routes/                        # Flask route handlers
│   ├── reply.py                   # Reply generation logic
│   ├── revise.py                  # Revision workflow
│   ├── save_standard.py           # Save/edit static responses
│   └── email.py                   # Email sync & inbox
│
├── utils/                         # Utility logic
│   ├── helpers.py                 # Similarity, link insertions, etc.
│   ├── entity_extraction.py       # GPT entity extraction
│   ├── config_loader.py           # Load school configs
│   ├── crm_upsert.py              # CRM dedupe/save
│   └── email_sync.py              # Fetch live emails from inbox
│
├── templates/
│   └── index.html                 # Full Smart Reply interface
│
├── static/
│   ├── styles.css                 # Frontend styling
│   └── script.js                  # All JS logic (inbox + Smart Reply)
│
├── kb/
│   └── <customer_id>/embeddings/  # Embeddings, metadata, PDFs
│
├── config/
│   ├── extraction_config_<id>.json  # Per-customer extraction logic
│   └── school_config_<id>.json      # Branding + tone for each school
│
├── standard_responses.json        # Approved responses (static matching)
└── README.md                      # This file
⚙️ Setup Instructions
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/BobOttley/SMART_REPLY_UK.git
cd SMART_REPLY_UK
2. Create a virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install Python dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Create .env file
ini
Copy
Edit
OPENAI_API_KEY=your_openai_key
EMAIL_ACCOUNT=your_email@example.com
EMAIL_PASSWORD=your_password
IMAP_SERVER=imap.mail.us-east-1.awsapps.com
IMAP_PORT=993
CUSTOMER_ID=LOCAL-TEST
5. Run migration (adds status column to emails table if needed)
bash
Copy
Edit
python utils/migrate.py
6. Fetch emails
bash
Copy
Edit
python utils/email_sync.py
7. Start the Flask server
bash
Copy
Edit
flask run
🌐 Deploying to Render
Required Files:
requirements.txt

runtime.txt (should contain python-3.11)

.env (set in Render dashboard, not committed)

Untracked database: add to .gitignore:

bash
Copy
Edit
smart_reply.db
*.pyc
__pycache__/
.env
Add these to .gitignore if not already present:
bash
Copy
Edit
smart_reply.db
kb/
.env
*.pkl
__pycache__/
🧪 Usage
Inbox Panel: View, open, dismiss parent emails.

Reply Panel: Paste emails or form data to generate replies.

Revise: Apply tweaks and save updated reply templates.

Multi-Customer: Just change the CUSTOMER_ID and associated config files.

🔧 Extending
Add new entity tags via config/extraction_config_<id>.json

Refine school branding/tone in school_config_<id>.json

Add custom CTAs or template variants to standard_responses.json

Attach event modules, CRMs, dashboards, or WhatsApp integrations

🛠 Deployment Fixes
If Render gives gunicorn: command not found:

Make sure this is in requirements.txt:

ini
Copy
Edit
gunicorn==21.2.0
Add a runtime.txt with:

Copy
Edit
python-3.11
🤝 Contributing
Bug reports, feature requests, and improvements welcome.
Please open a GitHub issue or pull request.

📬 Contact
For questions or onboarding support, email:
support@penai.co.uk

Last updated: 18 July 2025
Maintained by Bob Ottley

