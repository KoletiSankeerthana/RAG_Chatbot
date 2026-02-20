from database import engine, Base
from models import User # Importing models to register them with Base.metadata

def create_tables():
    """
    Creates all tables defined in the models using SQLAlchemy's metadata.
    """
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()
