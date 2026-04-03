# Use an official lightweight Python image
FROM python:3.13-slim

# Set environment variables for Flask
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

# Create and set working directory
WORKDIR /app

# Install system dependencies (optional: for SQLite, matplotlib, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Flask default port
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run"]
