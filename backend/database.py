from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database file name
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"

# Create the SQLAlchemy engine
# "check_same_thread": False is needed for SQLite to work with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.
    Yields a session and closes it when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
