print("🚦 Email fetcher script started - very first line")

import psycopg2
print("✅ Imported psycopg2")
from psycopg2.extras import DictCursor
print("✅ Imported DictCursor")
import imaplib
print("✅ Imported imaplib")
import email
print("✅ Imported email module")
from email.header import decode_header
print("✅ Imported decode_header")
from email.utils import parsedate_to_datetime
print("✅ Imported parsedate_to_datetime")
from dotenv import load_dotenv
print("✅ Imported load_dotenv")
import os
print("✅ Imported os")
import time
print("✅ Imported time")

# Load environment variables
load_dotenv()
print("✅ Loaded .env")

DATABASE_URL = os.getenv("DATABASE_URL")
print("🔑 DATABASE_URL:", DATABASE_URL)
CUSTOMER_ID = os.getenv("CUSTOMER_ID")
print("🔑 CUSTOMER_ID:", CUSTOMER_ID)
POLL_INTERVAL = int(os.getenv("EMAIL_POLL_INTERVAL", "60"))  # seconds
print("🔑 POLL_INTERVAL:", POLL_INTERVAL)

def clean_header(header):
    if header is None:
        return ""
    decoded, encoding = decode_header(header)[0]
    return decoded.decode(encoding or "utf-8") if isinstance(decoded, bytes) else decoded

def fetch_and_store_emails_for_user(account):
    user_id = account["user_id"]
    email_account = account["email_account"]
    email_password = account["email_password"]
    imap_server = account["imap_server"]
    imap_port = int(account["imap_port"])

    print(f"🔄 [FETCH] Starting fetch for {CUSTOMER_ID}/{user_id} ({email_account})")

    conn = None
    cursor = None
    mail = None
    try:
        print("🔗 Connecting to Postgres…")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=DictCursor)
        print("✅ Connected to DB")

        print(f"🔗 Connecting to IMAP: {imap_server}:{imap_port}")
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(email_account, email_password)
        print("✅ Logged in to IMAP")
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print(f"❌ IMAP search failed for {CUSTOMER_ID}/{user_id} with status: {status}")
            return

        email_ids = messages[0].split()
        print(f"📥 Fetching {len(email_ids)} emails for customer_id={CUSTOMER_ID}, user_id={user_id}")

        for eid in email_ids:
            res, msg_data = mail.fetch(eid, "(RFC822)")
            if res != "OK":
                print(f"❌ Failed to fetch email id {eid} for {CUSTOMER_ID}/{user_id}")
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            unique_id = msg.get("Message-ID")
            if not unique_id:
                print(f"⚠️ Skipping email without Message-ID for {CUSTOMER_ID}/{user_id}")
                continue  # skip broken emails

            cursor.execute(
                "SELECT 1 FROM emails WHERE customer_id=%s AND user_id=%s AND unique_id=%s",
                (CUSTOMER_ID, user_id, unique_id)
            )
            if cursor.fetchone():
                print(f"⚠️ Email {unique_id} already stored for {CUSTOMER_ID}/{user_id}")
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
                    unique_id, customer_id, user_id, subject, from_address, to_address,
                    body, status, date_received
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                unique_id, CUSTOMER_ID, user_id, subject, from_address, to_address,
                body, 'unprocessed', date_received
            ))

            print(f"✅ Saved for {CUSTOMER_ID}/{user_id}: {subject} from {from_address}")

        conn.commit()
        print(f"💾 Commit complete for {CUSTOMER_ID}/{user_id}")
        mail.logout()
        print(f"📤 Logged out IMAP for {CUSTOMER_ID}/{user_id}")
    except Exception as e:
        print(f"❌ Error for {CUSTOMER_ID}/{user_id}: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        if mail:
            try:
                mail.logout()
            except Exception:
                pass

def get_active_user_accounts_for_customer(customer_id):
    print(f"🔍 Fetching active user accounts for customer {customer_id}")
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            SELECT user_id, email_account, email_password, imap_server, imap_port
            FROM accounts
            WHERE active = TRUE AND customer_id = %s
        """, (customer_id,))
        accounts = cursor.fetchall()
        print(f"🔍 Found {len(accounts)} account(s) for {customer_id}")
        return [dict(row) for row in accounts]
    except Exception as e:
        print(f"❌ Error fetching user accounts for customer {customer_id}: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print(f"🚦 Starting email fetcher worker for customer_id={CUSTOMER_ID} (poll interval: {POLL_INTERVAL} seconds)")
    while True:
        accounts = get_active_user_accounts_for_customer(CUSTOMER_ID)
        if not accounts:
            print("⚠️ No active user accounts found. Sleeping...")
        for account in accounts:
            fetch_and_store_emails_for_user(account)
        print(f"😴 Sleeping for {POLL_INTERVAL} seconds...\n")
        time.sleep(POLL_INTERVAL)
