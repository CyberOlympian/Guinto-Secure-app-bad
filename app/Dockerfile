# Using an outdated Python base image with known vulnerabilities
FROM python:3.7-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose application port
EXPOSE 5000

# Run as root (security issue)
USER root

# Start the application
CMD ["python", "app/main.py"]
