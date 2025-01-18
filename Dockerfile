# Base image
FROM python:3.9-slim

# Install system dependencies, including sqlite3 CLI tool and Redis server
RUN apt-get update && apt-get install -y sqlite3 redis-server

# Copy application code
COPY . /app

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports (3000 for the application, 6379 for Redis)
EXPOSE 3000
EXPOSE 6379  

# Start Redis server and your application
CMD service redis-server start && python3 app.py -p 3000 -o 0.0.0.0



