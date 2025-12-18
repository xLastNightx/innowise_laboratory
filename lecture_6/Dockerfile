"""
Creating and launch of your app
"""
FROM python:3.11-slim

# creating working app
WORKDIR /app

COPY requirements.txt .

# making relations
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# open port
EXPOSE 8000

# launch app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# for correct launch enter docker run -p 8000:8000 fastapi-app:latest