# utils/helpers.py (EMAIL BRIDGE CODE)

import datetime
from models import Session, Email
import imaplib
import email as pyemail
from email.header import decode_header

# === Fetch all inbox emails for a customer (not dismissed) ===
def fetch_emails(customer_id):
    session = Session()
    emails = session.query(Email)\
        .filter_by(customer_id=customer_id, dismissed_at=None)\
        .order_by(Email.date_received.desc())\
        .all()
    result = [{
        "id": e.id,
        "subject": e.subject,
        "from_address": e.from_address,
        "body": (e.body[:200] if e.body else ""),  # Preview
        "date_received": e.date_received.strftime('%Y-%m-%d %H:%M')
    } for e in emails]
    session.close()
    return result

# === Fetch single email by ID and customer ===
def fetch_single_email(customer_id, email_id):
    session = Session()
    e = session.query(Email)\
        .filter_by(customer_id=customer_id, id=email_id)\
        .first()
    if not e:
        session.close()
        return {}
    result = {
        "id": e.id,
        "subject": e.subject,
        "from_address": e.from_address,
        "body": e.body,
        "date_received": e.date_received.strftime('%Y-%m-%d %H:%M')
    }
    session.close()
    return result

# === Dismiss (skip) email by ID for customer ===
def dismiss_email(customer_id, email_id, user_id=None):
    session = Session()
    e = session.query(Email)\
        .filter_by(customer_id=customer_id, id=email_id)\
        .first()
    if e:
        e.dismissed_at = datetime.datetime.utcnow()
        e.dismissed_by = user_id
        session.commit()
    session.close()

# === Sync emails from IMAP and upsert ===
def sync_emails_for_customer(customer_id, imap_host=None, imap_user=None, imap_pass=None):
    # You may want to get these from env/config if not provided
    import os
    if not imap_host: imap_host = os.getenv("IMAP_HOST")
    if not imap_user: imap_user = os.getenv("IMAP_USER")
    if not imap_pass: imap_pass = os.getenv("IMAP_PASS")

    session = Session()
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(imap_user, imap_pass)
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    new_count = 0
    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = pyemail.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")
                from_addr = msg.get("From")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                date_received = msg.get("Date")
                try:
                    date_parsed = pyemail.utils.parsedate_to_datetime(date_received)
                except Exception:
                    date_parsed = datetime.datetime.utcnow()

                exists = session.query(Email).filter_by(
                    customer_id=customer_id,
                    subject=subject,
                    from_address=from_addr,
                    date_received=date_parsed
                ).first()
                if not exists:
                    new_email = Email(
                        customer_id=customer_id,
                        subject=subject,
                        from_address=from_addr,
                        body=body,
                        date_received=date_parsed
                    )
                    session.add(new_email)
                    new_count += 1
    session.commit()
    session.close()
    mail.logout()
    return new_count

# === Save outgoing email (if needed for audit or threading) ===
def save_email(customer_id, subject, from_address, body, thread_id=None, user_id=None):
    session = Session()
    new_email = Email(
        customer_id=customer_id,
        subject=subject,
        from_address=from_address,
        body=body,
        date_received=datetime.datetime.utcnow(),
        thread_id=thread_id,
        processed_by=user_id,
        processed_at=datetime.datetime.utcnow()
    )
    session.add(new_email)
    session.commit()
    session.close()
