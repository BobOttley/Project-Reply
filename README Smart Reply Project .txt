Smart Reply – Project Overview (As of July 2025)
What is Smart Reply?
Smart Reply is a modular, multi-tenant AI-powered admissions assistant for independent schools. It automates parent email replies, manages CRM data, integrates with school inboxes, and delivers warm, professional communications—all via a modern web interface.

Key Features
AI-Powered Replies: GPT-based generation of human-sounding, helpful, and on-brand email responses to parent queries.

Entity Extraction: Automatically pulls names, children, interests, year groups, etc., from emails and forms.

Inbox Sync: Connects to IMAP/AWS WorkMail, imports and manages live emails.

Sentiment Scoring: Analyses tone/sentiment to guide reply strategy and track trends.

Static & AI Replies: Combines standard (pre-approved) replies with AI fallbacks.

Revision Flow: Lets staff refine replies, insert CTAs, edit, and save templates for future matching.

Smart Save: “Learns” from edits—saving high-quality replies to improve future matches.

Multi-Tenant: Manages multiple schools/groups with isolated configs, data, and knowledge.

Modular Architecture: Extensible with CRM, events, analytics, dashboards, WhatsApp, and more.

Technical Stack
Backend: Python 3.11+, Flask, SQLAlchemy, SQLite or PostgreSQL

AI Models: OpenAI GPT-4o/4o-mini, text-embedding-3-small

Frontend: HTML, CSS, JavaScript (custom modular UI)

Storage: Local filesystem for embeddings/configs; SQL DB for email/CRM; S3 for production storage

Email Sync: IMAP or AWS WorkMail (using imap-tools)

Deployment: GitHub + Render (with PostgreSQL, Gunicorn, env vars set via dashboard)

Multi-Tenancy: Everything (email, CRM, KB) tied to customer_id and (if enabled) user_id

Project Structure
bash
Copy
Edit
project_root/
├── app.py                      # Main Flask entrypoint
├── config.py                   # OpenAI/environment config
├── models.py                   # SQLAlchemy models
├── requirements.txt            # Pip dependencies
├── runtime.txt                 # Python version for Render
├── .env                        # Local env variables (not committed)
│
├── routes/                     # Flask route modules
│   ├── reply.py                # Reply generation
│   ├── revise.py               # Revision workflow
│   ├── save_standard.py        # Save/edit static responses
│   └── email.py                # Email sync & inbox
│
├── utils/                      # Utilities
│   ├── helpers.py              # Similarity, link insertions, etc.
│   ├── entity_extraction.py    # GPT entity extraction
│   ├── config_loader.py        # Load configs
│   ├── crm_upsert.py           # CRM dedupe/save
│   └── email_sync.py           # Fetch emails from inbox
│
├── templates/
│   └── index.html              # Full Smart Reply UI
│
├── static/
│   ├── styles.css              # Frontend CSS
│   └── script.js               # All JS logic (inbox + Smart Reply)
│
├── kb/
│   └── <customer_id>/embeddings/  # Embeddings, metadata, PDFs
│
├── config/
│   ├── extraction_config_<id>.json  # Per-customer extraction logic
│   └── school_config_<id>.json      # Branding + tone per school
│
├── standard_responses.json     # Approved static responses
├── .gitignore                 # Ignore db, env, pyc, etc.
└── README.md
Setup/Usage
Clone repo:
git clone https://github.com/BobOttley/SMART_REPLY_UK.git && cd SMART_REPLY_UK

Create venv:
python3 -m venv venv && source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Add .env:
Set OpenAI key, email creds, IMAP server/port, CUSTOMER_ID

Run migration:
python utils/migrate.py

Fetch emails:
python utils/email_sync.py

Start Flask server:
flask run (or gunicorn app:app on Render)

Render Deployment Tips
Ensure requirements.txt includes gunicorn==21.2.0

runtime.txt must contain python-3.11

Set .env variables in Render dashboard (never commit secrets!)

Ignore these in Git:

bash
Copy
Edit
smart_reply.db
kb/
.env
*.pkl
__pycache__/
Extending / Customising
Entity tags:
Add in config/extraction_config_<id>.json

Branding/tone:
Set in config/school_config_<id>.json

CTAs & templates:
Extend standard_responses.json

Modules:
Plug in events, analytics, dashboards, WhatsApp, etc.

Recent Upgrades
Full Multi-Tenancy:
All routes, data, and logic are customer-aware (customer_id/user_id)

PostgreSQL Support:
Render uses Postgres instead of SQLite; all DB logic supports both

Worker for Email Sync:
Background worker fetches emails on Render; not tied to Flask server thread

Modular Flask Routing:
Each module (reply, revise, save, email) is a standalone route file

Modern UI:
All features in one tabbed interface: Inbox, Reply, CRM, Settings (admin)

CRM Integration:
Parent-student data stored, searched, and linked to emails; new accounts created on reply

Advanced Search & Dedupe:
Search CRM by name/email/child; no duplicate accounts

Editable Standard Replies:
Save, edit, and match static templates with Markdown links

Sentiment Tracking:
All replies show sentiment 1–10 and an explanation

Revision & CTA Flow:
Add CTAs, refine replies, insert hyperlinks using selection tool

Admin Routing Rules:
Staff manage notification/email routing from the web UI (rules editable via modal)

Customer-aware S3 Storage:
All knowledge base files go to kb/<customer_id>/embeddings/ (local or S3)

New Scraper:
Scrapes school sites/PDFs, chunks, builds metadata, and generates everything for embedding

Inbox Preview & Junk Filtering:
Shows email subject/snippet, with "Dismiss" to ignore junk (no reply generated)

How to Contribute / Get Help
Open a GitHub issue or pull request for bugs or features

Email support: support@penai.co.uk

Last updated: 20 July 2025
Maintained by: Robert Ottley, PEN.ai