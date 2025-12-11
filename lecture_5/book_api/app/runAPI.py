from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from contextlib import asynccontextmanager
from datetime import datetime
import os

from . import models, schemas
from database.engine import get_db, create_tables

# Lifespan manager for application startup/shutdown events


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    """
    # Startup event
    print("Starting Book Collection API...")

    # Create database tables
    create_tables()

    # Check database file creation
    db_path = os.path.join(os.path.dirname(__file__),
                           "..", "database", "books.db")
    if os.path.exists(db_path):
        print(f"Database created: {db_path}")
    else:
        print(f"Database file will be created on first request")

    yield

    print("Stopping Book Collection API...")

# Create FastAPI application with lifespan
app = FastAPI(
    title="Book Collection API",
    description="A REST API for managing personal book collections",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint for API health check and documentation.
    """
    return {
        "message": "Welcome to Book Collection API",
        "description": "A REST API for managing personal book collections",
        "version": "1.0.0",
        "endpoints": {
            "add_book": "POST /books/",
            "get_all_books": "GET /books/",
            "get_book": "GET /books/{id}",
            "update_book": "PUT /books/{id}",
            "delete_book": "DELETE /books/{id}",
            "search_books": "GET /books/search/"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.post("/books/",
          response_model=schemas.Book,
          status_code=status.HTTP_201_CREATED,
          tags=["Books"])
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> schemas.Book:
    """
    Add a new book to the collection.

    Required fields:
    - title: Book title
    - author: Book author

    Optional field:
    - year: Publication year
    """
    # Check if book with same title and author already exists
    existing_book = db.query(models.Book).filter(
        models.Book.title.ilike(book.title),
        models.Book.author.ilike(book.author)
    ).first()

    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book '{book.title}' by {book.author} already exists"
        )

    # Create new book record
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    # Convert SQLAlchemy model to Pydantic model
    return schemas.Book.model_validate(db_book)


@app.get("/books/",
         response_model=List[schemas.Book],
         tags=["Books"])
def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500,
                       description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> List[schemas.Book]:
    """
    Get all books with pagination support.
    """
    # Query books with pagination
    books = db.query(models.Book).offset(skip).limit(limit).all()

    # Convert SQLAlchemy models to Pydantic models
    return [schemas.Book.model_validate(book) for book in books]


@app.get("/books/{book_id}",
         response_model=schemas.Book,
         tags=["Books"])
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> schemas.Book:
    """
    Get a specific book by its ID.

    Required parameter:
    - book_id: The unique identifier of the book
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    # Convert SQLAlchemy model to Pydantic model
    return schemas.Book.model_validate(db_book)


@app.put("/books/{book_id}",
         response_model=schemas.Book,
         tags=["Books"])
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db)
) -> schemas.Book:
    """
    Update book information.

    Required parameter:
    - book_id: The unique identifier of the book to update

    Optional fields (update only provided fields):
    - title: New book title
    - author: New book author
    - year: New publication year
    """
    # Find the book to update
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    update_data = book_update.model_dump(exclude_unset=True)

    # Check if update would create a duplicate book
    if 'title' in update_data or 'author' in update_data:
        new_title = update_data.get('title', db_book.title)
        new_author = update_data.get('author', db_book.author)

        # Look for other books with same title and author
        existing = db.query(models.Book).filter(
            models.Book.title.ilike(new_title),
            models.Book.author.ilike(new_author),
            models.Book.id != book_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this title and author already exists"
            )

    # Apply updates to the database model
    for field, value in update_data.items():
        setattr(db_book, field, value)

    # Save changes
    db.commit()
    db.refresh(db_book)

    # Return updated book as Pydantic model
    return schemas.Book.model_validate(db_book)


@app.delete("/books/{book_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Books"])
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a book by its ID.

    Required parameter:
    - book_id: The unique identifier of the book to delete
    """
    # Find the book to delete
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    # Delete the book
    db.delete(book)
    db.commit()

    # Return 204 No Content (empty response)
    return


@app.get("/books/search/",
         response_model=List[schemas.Book],
         tags=["Search"])
def search_books(
    title: Optional[str] = Query(
        None, description="Search by title (partial match)"),
    author: Optional[str] = Query(
        None, description="Search by author (partial match)"),
    year: Optional[int] = Query(
        None, description="Search by exact publication year"),
    db: Session = Depends(get_db)
) -> List[schemas.Book]:
    """
    Search books by various criteria.

    Optional parameters:
    - title: Partial match on book title (case-insensitive)
    - author: Partial match on author name (case-insensitive)
    - year: Exact publication year
    """
    # Start with base query
    query = db.query(models.Book)

    # Apply filters based on provided parameters
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))

    if year:
        query = query.filter(models.Book.year == year)

    # Execute query and get results
    books = query.all()

    # Convert SQLAlchemy models to Pydantic models
    return [schemas.Book.model_validate(book) for book in books]


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "service": "book-collection-api",
        "timestamp": datetime.now().isoformat()
    }
