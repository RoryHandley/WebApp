# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the proxy folder and common.py into the container at the root of /app
COPY proxy/proxy.py ./proxy.py
COPY common.py ./common.py

# Install Python dependencies specific to the proxy
COPY proxy/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the proxy server listens
EXPOSE 3000

# Command to run the proxy server
CMD ["python", "proxy.py"]

