from models import init_db
from sqlalchemy import text

def main():
    """Run database migrations for Smart Reply"""
    print("🚀 Starting database migration...")

    try:
        Session = init_db()
        session = Session()

        # List of required columns to check and add
        required_columns = {
            "status": "ALTER TABLE emails ADD COLUMN status VARCHAR DEFAULT 'unprocessed'",
            "customer_id": "ALTER TABLE emails ADD COLUMN customer_id VARCHAR DEFAULT 'LOCAL-TEST'"
        }

        for column, alter_sql in required_columns.items():
            try:
                session.execute(text(f"SELECT {column} FROM emails LIMIT 1"))
                print(f"✅ Column '{column}' already exists.")
            except Exception:
                print(f"➕ Adding column '{column}' to emails table...")
                session.execute(text(alter_sql))

        session.commit()
        print("✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration error: {str(e)}")
        raise

    finally:
        session.close()

if __name__ == "__main__":
    main()
