# === utils/email_sync.py ===

import os, sys
from datetime import datetime
from dotenv import load_dotenv
from imap_tools import MailBox, AND

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Session, Email

# Load environment variables
load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
CUSTOMER_ID = os.getenv("CUSTOMER_ID", "LOCAL-TEST")


def fetch_and_upsert_emails():
    """Fetch new (unseen) emails and store only if not already in DB."""
    session = Session()
    try:
        print("📥 Connecting to mailbox...")
        with MailBox(IMAP_HOST).login(IMAP_USER, IMAP_PASS) as mailbox:
            print("✅ Connected. Checking for new emails...")

            new_count = 0
            for msg in mailbox.fetch(AND(seen=False)):
                unique_id = msg.uid
                exists = session.query(Email).filter_by(unique_id=unique_id).first()
                if exists:
                    continue  # Already saved

                email_record = Email(
                    unique_id=unique_id,
                    user_id=None,
                    thread_id=msg.headers.get("Thread-Index") or None,
                    subject=msg.subject or "(No Subject)",
                    from_address=msg.from_,
                    to_address=", ".join(msg.to or []),
                    body=msg.text or msg.html or "",
                    status="unprocessed",
                    date_received=msg.date or datetime.utcnow(),
                    direction="incoming",
                    customer_id=CUSTOMER_ID
                )

                session.add(email_record)
                new_count += 1
                print(f"📨 Saved: {email_record.subject}")

            session.commit()
            print(f"✅ Sync complete. {new_count} new email(s) stored.")

    except Exception as e:
        print(f"❌ Email sync error: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    fetch_and_store_emails()
