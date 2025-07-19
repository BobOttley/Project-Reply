from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, Index, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
import os
from dotenv import load_dotenv

# Load .env for DATABASE_URL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
    raise RuntimeError("DATABASE_URL must be set to a PostgreSQL connection string!")

Base = declarative_base()

class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)
    account_number = Column(String, unique=True, nullable=True, index=True)
    customer_id = Column(String, nullable=True, index=True)  # <-- Added
    children = relationship("Child", back_populates="parent")
    enquiries = relationship("Enquiry", back_populates="parent")

class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    dob = Column(DateTime, nullable=True, index=True)
    year_group = Column(String, nullable=True)
    interests = Column(Text, nullable=True)
    account_number = Column(String, unique=True, nullable=True, index=True)
    customer_id = Column(String, nullable=True, index=True)  # <-- Added
    parent = relationship("Parent", back_populates="children")
    enquiries = relationship("Enquiry", back_populates="child")

    __table_args__ = (
        UniqueConstraint('parent_id', 'name', 'dob', name='uix_parent_child_name_dob'),
    )

class PipelineStage(Base):
    __tablename__ = "pipeline_stages"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Enquiry(Base):
    __tablename__ = "enquiries"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=True, index=True)
    enquiry_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    source = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)
    pipeline_stage_id = Column(Integer, ForeignKey("pipeline_stages.id"), nullable=True)
    customer_id = Column(String, nullable=True, index=True)  # <-- Added

    parent = relationship("Parent", back_populates="enquiries")
    child = relationship("Child", back_populates="enquiries")
    pipeline_stage = relationship("PipelineStage")

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    unique_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=True)
    thread_id = Column(String, nullable=True, index=True)
    subject = Column(String, nullable=True)
    from_address = Column(String, nullable=True)
    to_address = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    status = Column(String, default='unprocessed')
    date_received = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    dismissed_by = Column(String, nullable=True)
    dismissed_at = Column(DateTime, nullable=True)
    processed_by = Column(String, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    direction = Column(String, nullable=True)
    customer_id = Column(String, nullable=True, default="LOCAL-TEST", index=True)

    def dismiss(self, user_id=None):
        self.status = 'dismissed'
        self.dismissed_at = datetime.datetime.utcnow()
        self.dismissed_by = user_id
        return self

    def __repr__(self):
        return f"<Email(id={self.id}, subject='{self.subject}', status='{self.status}')>"

# === Database Migration Helper (OPTIONAL) ===
def migrate_db(engine):
    """Perform any necessary database migrations"""
    from sqlalchemy import inspect, text
    inspector = inspect(engine)
    existing_columns = {col['name'] for col in inspector.get_columns('emails')}
    with engine.connect() as conn:
        if 'status' not in existing_columns:
            conn.execute(text("ALTER TABLE emails ADD COLUMN status VARCHAR DEFAULT 'unprocessed'"))
        conn.commit()

# === INIT DB ===
def init_db(db_url=DATABASE_URL):
    """Initialize database with proper error handling"""
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        migrate_db(engine)  # Run migrations if needed
        return sessionmaker(bind=engine)
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")
        raise

# Create Session class
try:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
except Exception as e:
    print(f"❌ Error creating database: {str(e)}")
    raise
