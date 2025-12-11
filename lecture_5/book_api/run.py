import uvicorn
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Display startup information
    print("=" * 50)
    print("Book Collection API")
    print("=" * 50)
    print("Project structure:")
    print(f"  Current directory: {os.path.abspath('.')}")
    print(f"  App file:         {os.path.abspath('app/main.py')}")
    print(f"  Database:         {os.path.abspath('database/books.db')}")
    print("-" * 50)
    print("Starting server...")
    print("Swagger UI:    http://127.0.0.1:8000/docs")
    print("ReDoc:         http://127.0.0.1:8000/redoc")
    print("=" * 50)

    # Start the server
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
