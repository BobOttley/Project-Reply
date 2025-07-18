Summary
Each file and folder plays a distinct role, from core app logic to CRM data management, GPT prompt engineering, email integration, and frontend UI. Together, they form a powerful AI-driven admissions CRM system that is flexible, multi-tenant, and highly personalised.

If you want, I can help you generate a polished markdown version of this for your README file or help explain any part in more detail!







You said:
can you write a full complete readme file


ChatGPT said:
Certainly! Here's a complete, polished README file for your Smart Reply Project, covering everything from setup to architecture and usage:

Smart Reply Project
Overview
Smart Reply is a modular, multi-tenant AI-powered admissions assistant designed to help independent schools manage parent enquiries efficiently. It combines GPT-driven email reply generation, CRM integration, and seamless email syncing to deliver personalised, professional communication.

Features
AI-Powered Reply Generation: Generates warm, professional email responses tailored to each enquiry using OpenAI GPT models.

Flexible Entity Extraction: Dynamically extracts key information (parent details, child info, interests) from free-text or structured enquiry forms.

CRM Integration: Stores parents, children, and enquiries in a relational database with unique account numbers and deduplication logic.

Email Syncing & Inbox Management: Syncs emails from IMAP/AWS WorkMail, links emails to enquiries, and provides a polished inbox UI.

Knowledge Base Retrieval: Uses vector embeddings to fetch relevant school policy and information content to enrich GPT prompts.

Template Matching & Sentiment Analysis: Matches common queries to pre-approved static replies and analyses sentiment for tailored responses.

Revision Workflow: Allows admissions staff to revise AI-generated replies with context-aware edits.

Multi-Customer Support: Supports custom configurations, extraction schemas, and branding for different schools/groups.

Tech Stack
Backend: Python, Flask, SQLAlchemy, SQLite (or other DB)

AI: OpenAI GPT models (gpt-4o-mini for generation, embedding models for search)

Frontend: HTML, CSS, JavaScript (with custom chatbot UI and inbox)

Data Storage: Local file storage for configs and embeddings; relational DB for CRM data

Email Integration: IMAP/AWS WorkMail with syncing and management

Project Structure
yaml
Copy
project_root/
├── app.py                        # Main Flask application entry
├── config.py                     # Central app config and OpenAI client setup
├── routes/                      # API route handlers
│   ├── reply.py                 # Reply generation endpoint
│   ├── revise.py                # Reply revision endpoint
│   ├── save_standard.py         # Manage static reply templates
│   └── email.py                 # Email sync and inbox management
├── utils/                       # Utility modules
│   ├── helpers.py               # Text processing, markdown, similarity
│   ├── crm_upsert.py            # Upsert functions for CRM entities
│   ├── entity_extraction.py     # GPT entity extraction utilities
│   ├── config_loader.py         # Dynamic config loader for extraction schemas
│   └── account_utils.py         # Account number generator helpers
├── templates/
│   └── index.html               # Frontend chat and inbox UI
├── static/
│   ├── styles.css               # Styling and branding
│   └── script.js                # Frontend interaction logic
├── embeddings/
│   ├── metadata.pkl             # KB metadata for retrieval
│   └── doc_embeddings.pkl       # KB vector embeddings
├── config/
│   └── extraction_config_<customer_id>.json  # Per-customer GPT extraction configs
├── standard_responses.json      # Static Q&A templates for quick replies
├── models.py                    # SQLAlchemy ORM models for CRM and emails
└── README.md                    # This file
Setup & Installation
Clone the repo and navigate into it:

bash
Copy
git clone <repo-url>
cd project_root
Create and activate a Python virtual environment:

bash
Copy
python3 -m venv venv
source venv/bin/activate
Install required packages:

bash
Copy
pip install -r requirements.txt
Configure environment variables:
Create a .env file with:

ini
Copy
OPENAI_API_KEY=your_openai_api_key
EMAIL_ACCOUNT=your_email@example.com
EMAIL_PASSWORD=your_email_password
IMAP_SERVER=imap.mail.us-east-1.awsapps.com
IMAP_PORT=993
Prepare extraction config files:
Place per-customer JSON configs in the config/ folder, e.g., extraction_config_LOCAL-TEST.json.

Run database migrations or initialize DB:
The app uses SQLAlchemy and auto-creates tables on first run.

Start the Flask app:

bash
Copy
flask run
Access the frontend:
Open http://localhost:5000 in your browser.

Usage
Use the frontend chat interface to submit enquiries or paste parent emails.

Sync inbox via provided buttons to import emails automatically.

View, reply, dismiss emails from the inbox panel.

Generate and revise AI-powered replies enriched by CRM data and school KB.

Manage static reply templates for common questions.

Extending & Customizing
Add new extraction fields by updating customer extraction configs.

Customize school info and branding via school_config.json.

Integrate with other email providers by extending email.py.

Build CRM dashboards or pipeline management UIs.

Adapt for multi-user access and authentication.

Contributing
Contributions, bug reports, and feature requests are welcome! Please submit via GitHub Issues or Pull Requests.

License
Specify your license here (e.g., MIT, Apache 2.0).

Contact
For questions or support, reach out to the development team at support@example.com.

Last updated: 18 July 2025