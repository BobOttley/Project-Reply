# create_tables.py

from models import Base, engine

# This will create all tables defined in your models.py using the engine (database connection).
Base.metadata.create_all(engine)

print("✅ Tables created successfully!")
