from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.engine import Base


class Book(Base):
    """
    SQLAlchemy model for books table.

    Attributes:
    - id: Primary key, auto-incrementing integer
    - title: Book title (required)
    - author: Book author (required)
    - year: Publication year (optional)
    - created_at: Timestamp when record was created
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        """Convert SQLAlchemy model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
