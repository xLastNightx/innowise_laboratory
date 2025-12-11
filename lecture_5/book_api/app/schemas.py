from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# Base book schema


class BookBase(BaseModel):
    """
    Base schema for book data.

    Fields:
    - title: Book title 
    - author: Book author 
    - year: Publication year 
    """
    title: str = Field(..., min_length=1, max_length=200, example="1984")
    author: str = Field(..., min_length=1, max_length=100,
                        example="George Orwell")
    year: Optional[int] = Field(None, ge=1000, le=2100, example=1949)

# Schema for creating a book


class BookCreate(BookBase):
    """Schema for creating a new book (same as BookBase)."""
    pass

# Schema for book response


class BookResponse(BookBase):
    """
    Schema for book response with additional fields.

    Additional fields:
    - id: Unique book identifier
    - created_at: Timestamp when book was added
    """
    id: int
    created_at: Optional[datetime] = None

    # Pydantic v2 configuration
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "1984",
                "author": "George Orwell",
                "year": 1949,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    )

# Schema for updating a book


class BookUpdate(BaseModel):
    """
    Schema for updating book information.

    All fields are optional - only provided fields will be updated.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=2100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "1984 Updated",
                "year": 1950
            }
        }
    )


Book = BookResponse
