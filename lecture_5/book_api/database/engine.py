from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define database file path in the database folder
DATABASE_PATH = os.path.join(BASE_DIR, "database", "books.db")

# Create database directory if it doesn't exist
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.

    Yields:
    - Database session

    Ensures session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables defined in models.

    This function should be called during application startup.
    """
    try:
        # Import models here to avoid circular imports
        from app import models

        # Create all tables
        Base.metadata.create_all(bind=engine)
        print(f"Database tables created: {DATABASE_PATH}")

        return True
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False
