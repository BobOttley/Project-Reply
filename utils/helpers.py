# === utils/helpers.py ===

import re
import os
import numpy as np
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()  # Load .env at import

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.mail.us-east-1.awsapps.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))

def get_workmail_creds(customer_id):
    # All customer_ids use the same creds for now. Expand as needed.
    email_addr = os.getenv("EMAIL_ACCOUNT")
    email_pass = os.getenv("EMAIL_PASSWORD")
    if not email_addr or not email_pass:
        raise Exception("EMAIL_ACCOUNT or EMAIL_PASSWORD not set in .env")
    return {
        "email": email_addr,
        "password": email_pass
    }

# --- Parse URL Box ---
def parse_url_box(url_text):
    url_map = {}
    if not url_text:
        return url_map
    parts = re.split(r'[;\n]+', url_text.strip())
    for part in parts:
        if '=' in part:
            anchor, url = part.split('=', 1)
            url_map[anchor.strip()] = url.strip()
    return url_map

# --- Insert Links in Text ---
def insert_links(text, url_map):
    def safe_replace(match):
        word = match.group(0)
        for anchor, url in url_map.items():
            if word.lower() == anchor.lower():
                return f"[{word}]({url})"
        return word

    if not url_map:
        return text
    sorted_anchors = sorted(url_map.keys(), key=len, reverse=True)
    if not sorted_anchors:
        return text
    pattern = r'\b(' + '|'.join(re.escape(a) for a in sorted_anchors) + r')\b'
    return re.sub(pattern, safe_replace, text, flags=re.IGNORECASE)

# --- Remove Personal Info / PII ---
PII_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    r"\b(?:\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}\b",
    r"\b(?:\+44\s?1\d{3}|\(?01\d{3}\)?|\(?02\d{3}\)?)\s?\d{3}\s?\d{3,4}\b",
    r"\+?\d[\d\s\-().]{7,}\d",
    r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b",
]

def remove_personal_info(text: str) -> str:
    if not text:
        return text
    for pat in PII_PATTERNS:
        text = re.sub(pat, "[redacted]", text, flags=re.I)
    text = re.sub(
        r"\b(my name is|i am|i’m|i’m called)\s+(mr\.?|mrs\.?|ms\.?|miss)?\s*[A-Z][a-z]+\b",
        "my name is [redacted]", text, flags=re.I
    )
    text = re.sub(
        r"\bDear\s+(Mr\.?|Mrs\.?|Ms\.?|Miss)?\s*[A-Z][a-z]+\b",
        "Dear [redacted]", text, flags=re.I
    )
    text = re.sub(
        r"\b(?:regards|thanks|thank you|sincerely|best wishes|kind regards)[,]?\s+[A-Z][a-z]+\b",
        "[redacted]", text, flags=re.I
    )
    return text

# --- Embedding (requires OpenAI client passed in) ---
def embed_text(text: str, client, model_name: str) -> np.ndarray:
    text = text.replace("\n", " ")
    res  = client.embeddings.create(model=model_name, input=[text])
    return np.array(res.data[0].embedding)

# --- Markdown to HTML ---
def markdown_to_html(text: str) -> str:
    return re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)',
        lambda m: f'<a href="{m.group(2)}" target="_blank">{m.group(1)}</a>',
        text
    )

# --- Clean GPT Email Output ---
def clean_gpt_email_output(md: str) -> str:
    md = md.strip()
    md = re.sub(r"^```(?:markdown)?", "", md, flags=re.I).strip()
    md = re.sub(r"```$", "", md, flags=re.I).strip()
    md = re.sub(r"^(markdown:|subject:)[\s]*", "", md, flags=re.I).strip()
    md = re.sub(r"^Subject:.*\n?", "", md, flags=re.I)
    md = re.sub(r"\*\*(.*?)\*\*", r"\1", md)
    md = re.sub(r"__(.*?)__", r"\1", md)
    paragraphs = [p.strip() for p in md.split('\n\n') if p.strip()]
    new_paragraphs = []
    for para in paragraphs:
        lines = para.split('\n')
        if all(line.strip().startswith(('- ', '* ')) for line in lines):
            bullets = [f"<li>{line[2:].strip()}</li>" for line in lines]
            new_paragraphs.append("<ul>" + "".join(bullets) + "</ul>")
        else:
            new_paragraphs.append(f"<p>{para}</p>")
    md = "\n".join(new_paragraphs)
    md = re.sub(r'</p>\s*<p>', '</p><p>', md)
    md = re.sub(r'<p>(\s*<ul>.*?</ul>)</p>', r'\1', md, flags=re.DOTALL)
    md = re.sub(r'<p>\s*</p>', '', md)
    return md.strip()

# --- Cosine Similarity ---
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ===== AWS WorkMail IMAP Email Fetching =====

from email.utils import parsedate_to_datetime

from email.utils import parsedate_to_datetime

def fetch_emails(customer_id=None, limit=10):
    creds = get_workmail_creds(customer_id or "default")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(creds["email"], creds["password"])
    mail.select('inbox')
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        mail.logout()
        return []

    email_ids = messages[0].split()[-limit:]
    emails = []

    for i, eid in enumerate(reversed(email_ids)):
        status, msg_data = mail.fetch(eid, "(RFC822)")
        if status != "OK":
            continue
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode(errors="replace")

                from_ = msg.get("From")
                date_ = msg.get("Date")
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                            try:
                                body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                                break
                            except Exception:
                                body = ""
                else:
                    try:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                    except Exception:
                        body = ""

                emails.append({
                    "id": i + 1,
                    "subject": subject.strip(),
                    "from_address": from_.strip(),
                    "date_received": date_,  # Just return as-is
                    "body": body.strip()[:3000]
                })

    mail.logout()
    return emails



def fetch_single_email(customer_id, email_id):
    all_emails = fetch_emails(customer_id)
    for em in all_emails:
        if em["id"] == email_id:
            return em
    return None

def save_email(customer_id, email_data):
    # Optional: Implement persistent storage as needed
    pass

def dismiss_email(customer_id, email_id):
    # Optional: Mark as dismissed in your DB
    pass
