import psycopg2
from psycopg2.extras import DictCursor
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
DATABASE_URL = os.getenv("DATABASE_URL")

def clean_header(header):
    if header is None:
        return ""
    decoded, encoding = decode_header(header)[0]
    return decoded.decode(encoding or "utf-8") if isinstance(decoded, bytes) else decoded

def fetch_and_store_emails(customer_id):
    if not customer_id:
        print("❌ customer_id is required.")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=DictCursor)

        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        print(f"📥 Fetching {len(email_ids)} emails for customer_id={customer_id}...")

        for eid in email_ids:
            res, msg_data = mail.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            unique_id = msg.get("Message-ID")
            if not unique_id:
                continue  # skip broken emails

            cursor.execute(
                "SELECT 1 FROM emails WHERE customer_id=%s AND unique_id=%s",
                (customer_id, unique_id)
            )
            if cursor.fetchone():
                continue  # already stored

            subject = clean_header(msg.get("Subject"))
            from_address = clean_header(msg.get("From"))
            to_address = clean_header(msg.get("To"))
            date_received = parsedate_to_datetime(msg.get("Date"))

            # Get plain text body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

            cursor.execute("""
                INSERT INTO emails (
                    unique_id, customer_id, subject, from_address, to_address,
                    body, status, date_received
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                unique_id, customer_id, subject, from_address, to_address,
                body, 'unprocessed', date_received
            ))

            print(f"✅ Saved for {customer_id}: {subject} from {from_address}")

        conn.commit()
        mail.logout()
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Use your real customer_id value or keep as 'LOCAL-TEST'
    fetch_and_store_emails(customer_id="LOCAL-TEST")
