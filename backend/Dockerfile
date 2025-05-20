# Use official slim Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

ENV PYTHONPATH=/app


# Install system dependencies (for psycopg2 and bcrypt)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy everything inside the backend folder
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install "numpy<2.0.0"
RUN pip install --default-timeout=100 --retries=10 --no-cache-dir -r requirements.txt


# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
