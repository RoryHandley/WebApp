# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install Redis and other required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the proxy folder and common.py into the container at the root of /app
COPY proxy/proxy.py ./proxy.py
COPY common.py ./common.py

# Install Python dependencies specific to the proxy
COPY proxy/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the proxy server listens
EXPOSE 3000

# Start both Redis server and the Python proxy script
CMD ["sh", "-c", "redis-server --daemonize yes && python proxy.py"]
