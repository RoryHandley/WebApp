Client-Server Architecture with Proxy, Database, and Caching
This project implements a client-server architecture with a proxy server, a database backend, and caching using Redis. The client sends requests to the proxy server, which caches the data retrieved from the database. If a cached result exists, the proxy will return the cached data to the client; otherwise, it queries the database and updates the cache.

The entire application has been containerized using Docker to simplify deployment and ensure consistency across environments. With Docker, all dependencies, including the application, Redis server, and SQLite database, are bundled together in containers, making it easy to run and manage the application in any environment.

Components
Server (server.py)
The server listens for incoming client connections on a specified IP and port. Upon receiving a request, the server queries a SQLite database (videos.db) for data matching the request. It sends the data or an error message back to the client.

Proxy (proxy.py)
The proxy server listens for incoming client connections. It checks if the requested data exists in the Redis cache. If the data is cached, the proxy returns the cached response. If not, it forwards the request to the server, retrieves the data, stores it in the cache, and sends the response back to the client.

Client (client.py)
The client sends a request to the proxy server with specific data. It waits for a response from the proxy, which in turn is from the server (or the cache). The client measures the round-trip time of the request in microseconds.

App (app.py)
The main application file that orchestrates the entire system. It initiates the proxy server, connects to the Redis database, and integrates the caching mechanism.

Logging (logger.py)
Custom logging is implemented using Python's logging module. Logs are written to both a file (app.log) and displayed in the console for easy monitoring.

Requirements
Python 3.x
SQLite3
Redis (install Redis server locally or use a remote Redis service)
argparse module for handling command-line arguments
logging module for logging messages
redis Python package for caching
Running the Application with Docker
The application has been containerized using Docker. To run the application within Docker containers, follow these steps:

Build the Docker Image
From the root of the project directory, run the following command to build the Docker image:

docker build -t webapp-image .

Run the Docker Container
After building the image, start the container with the following command:

docker run -p 3000:3000 webapp-image
This will map port 3000 on your local machine to port 3000 in the container (for the application). The application and Redis server will run within the same container.

Access the Application
You can now send requests to localhost:3000 to interact with the application.
