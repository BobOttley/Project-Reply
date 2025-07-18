import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from models import Session, Email
from dotenv import load_dotenv

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))

def clean_header(header):
    if header is None:
        return ""
    decoded, encoding = decode_header(header)[0]
    return decoded.decode(encoding or "utf-8") if isinstance(decoded, bytes) else decoded

def fetch_and_store_emails(customer_id, user_id=None):
    """
    Fetches all emails from the inbox and stores them in the DB
    tagged with the given customer_id and (optionally) user_id.
    """
    if not customer_id:
        print("❌ customer_id is required.")
        return

    session = Session()
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        print(f"📥 Fetching {len(email_ids)} emails for customer_id={customer_id} user_id={user_id}...")

        for eid in email_ids:
            res, msg_data = mail.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            msg_id = msg.get("Message-ID")
            if not msg_id:
                continue  # skip broken emails

            # Check if already saved for this customer (avoid cross-tenant mixing)
            if session.query(Email).filter_by(customer_id=customer_id, message_id=msg_id).first():
                continue

            subject = clean_header(msg.get("Subject"))
            from_address = clean_header(msg.get("From"))
            date = parsedate_to_datetime(msg.get("Date"))

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

            new_email = Email(
                customer_id=customer_id,
                user_id=user_id,
                message_id=msg_id,
                from_address=from_address,
                subject=subject,
                body=body,
                date_received=date,
                status="unprocessed"
            )
            session.add(new_email)
            print(f"✅ Saved for {customer_id}: {subject} from {from_address}")

        session.commit()
        mail.logout()
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    # For manual testing only: set your test customer_id and user_id
    fetch_and_store_emails(customer_id="LOCAL-TEST", user_id=None)

