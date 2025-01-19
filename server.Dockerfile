# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the server folder and common.py into the container at the root of /app
COPY server/server.py ./server.py
COPY common.py ./common.py

# Install Python dependencies specific to the server
COPY server/requirements.txt ./requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the server listens
EXPOSE 9999

# Command to run the server
CMD ["python", "server.py"]

