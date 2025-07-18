from models import Base, engine

def init_db():
    print("Creating all tables...")
    Base.metadata.create_all(engine)
    print("All tables created successfully.")

if __name__ == "__main__":
    init_db()
