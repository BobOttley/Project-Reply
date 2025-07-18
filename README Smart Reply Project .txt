Smart Reply Project
Smart Reply is a modular, multi-tenant AI-powered admissions assistant for independent schools. It automates parent email replies, manages CRM data, integrates with your inbox, and enables personalised, professional communication—all in a fast, modern web UI.

Features
AI-Powered Replies: Instantly generates warm, professional responses to parent enquiries using OpenAI GPT models.

Flexible Entity Extraction: Extracts parent/child info, interests, and context from emails or web forms.

CRM Integration: Links emails and enquiries to CRM entities with deduplication and unique account numbers.

Inbox Management: Syncs emails from IMAP or AWS WorkMail and displays them in a polished, two-panel inbox UI.

Knowledge Base Retrieval: Uses semantic embeddings to pull the most relevant school info and policies for replies.

Template Matching & Sentiment Analysis: Matches queries to static approved replies and analyses sentiment for quality/context.

Revision Workflow: Allows staff to revise and refine AI-generated emails before sending.

Multi-Customer Support: Easily onboard multiple schools or groups with custom configs and branding.

Modular & Extensible: Designed for rapid iteration and easy addition of new features (CRM dashboards, analytics, etc.).

Tech Stack
Backend: Python, Flask, SQLAlchemy, SQLite (or your DB of choice)

AI: OpenAI GPT models (gpt-4o-mini for generation, embedding models for KB search)

Frontend: HTML, CSS, JavaScript (custom inbox and chat UI)

Data Storage: Local files for embeddings/configs; database for CRM/email data

Email Integration: IMAP / AWS WorkMail syncing and management

Project Structure
php
Copy
Edit
project_root/
├── app.py                        # Main Flask application entrypoint
├── config.py                     # App config and OpenAI setup
├── routes/                       # API route handlers
│   ├── reply.py                  # Reply generation
│   ├── revise.py                 # Revision endpoint
│   ├── save_standard.py          # Static reply templates
│   └── email.py                  # Email sync/inbox management
├── utils/                        # Utility modules
│   ├── helpers.py                # Text processing, similarity, markdown, etc.
│   ├── crm_upsert.py             # CRM upsert logic
│   ├── entity_extraction.py      # GPT entity extraction tools
│   ├── config_loader.py          # Dynamic config loader
│   └── account_utils.py          # Account number logic
├── templates/
│   └── index.html                # Main web UI (inbox + chat)
├── static/
│   ├── styles.css                # CSS and branding
│   └── script.js                 # Frontend JS logic
├── embeddings/
│   ├── metadata.pkl              # KB metadata for retrieval
│   └── doc_embeddings.pkl        # Embedding vectors
├── config/
│   └── extraction_config_<customer_id>.json  # Per-customer extraction configs
├── standard_responses.json       # Static replies for common queries
├── models.py                     # SQLAlchemy models
└── README.md                     # This file
Setup & Installation
Clone the repository:

bash
Copy
Edit
git clone <repo-url>
cd project_root
Create and activate a virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
Configure environment variables:

Create a .env file:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key
EMAIL_ACCOUNT=your_email@example.com
EMAIL_PASSWORD=your_email_password
IMAP_SERVER=imap.mail.us-east-1.awsapps.com
IMAP_PORT=993
Prepare extraction configs:

Place per-customer JSON configs in the config/ folder (e.g. extraction_config_LOCAL-TEST.json).

Run database migrations (if needed):

The app auto-creates tables on first run with SQLAlchemy.

Start the Flask app:

bash
Copy
Edit
flask run
Access the frontend:

Open http://localhost:5000 in your browser.

Usage
Use the Smart Reply inbox to view, reply, or dismiss parent emails.

Paste parent emails or enquiry forms into the Smart Reply panel for instant, context-aware responses.

Revise, refine, and save standard replies.

Manage multiple schools by swapping customer configs and branding.

All data is stored locally or in your configured database.

Extending & Customising
Add fields to entity extraction by editing the per-customer configs.

Adjust branding and school info via school_config.json.

Integrate additional email providers or CRM modules as needed.

Build dashboards, analytics, or advanced pipeline features.

Contributing
Contributions, bug reports, and feature requests are welcome!
Please submit via GitHub Issues or Pull Requests.

License
Specify your project license here (e.g. MIT, Apache 2.0).

Contact
For questions or support, contact the development team at
support@example.com

Last updated: 18 July 2025