# Client-Server Architecture with Proxy, Database, and Caching

This project implements a client-server architecture with a proxy server, a database backend, and caching using Redis. The client sends requests to the proxy server, which caches the data retrieved from the database. If a cached result exists, the proxy will return the cached data to the client; otherwise, it queries the server and updates the cache.

The entire application has been containerized using Docker to simplify deployment and ensure consistency across environments. With Docker, all dependencies, including the application, Redis server, and SQLite database, are bundled into separate containers, making it easy to run and manage the application in any environment.

---

## Components

### **1. Server (`server.py`)**
- **Purpose**: Handles requests from the proxy server.
- **Behavior**: 
  - Listens for incoming client connections on a specified IP and port.
  - Queries a SQLite database (`videos.db`) for matching data upon request.
  - Returns the requested data or an error message back to the proxy server.

### **2. Proxy (`proxy.py`)**
- **Purpose**: Acts as an intermediary between the client and server. Implements caching using Redis.
- **Behavior**: 
  - Listens for client connections on port `3000`.
  - Checks the Redis cache for requested data.
  - If cached data exists, returns it to the client.
  - If not, forwards the request to the server, retrieves the response, stores it in Redis, and sends it back to the client.

### **3. Caching (Redis)**
- **Purpose**: Improves application performance by caching frequently accessed data.
- **Setup**: Redis runs alongside the proxy server in the same container.

### **4. Database (`videos.db`)**
- **Purpose**: Stores data queried by the server.
- **Type**: SQLite database.
- **Behavior**: Contains a `videos` table with structured data. Queries are performed on this table by the server.

### **5. Logging (`common.py`)**
- **Purpose**: Provides centralized logging for both the proxy and server.
- **Setup**:
  - Logs are written to `app.log`.
  - Both console and file-based logs are implemented using Python’s `logging` module.

---

## Requirements
- Python 3.x
- SQLite3
- Redis
- Python libraries:
  - `argparse`
  - `logging`
  - `redis`

---

## Running the Application with Docker

The application has been containerized using Docker. It consists of two containers:
1. **Proxy Container**: Runs the proxy application and Redis server.
2. **Server Container**: Runs the server application and includes the SQLite database.

### Steps to Run the Application

### **1. Build the Docker Images**
Navigate to the root directory of the project and build the images for both the proxy and server:

# Build the Proxy Image
```bash
docker build -f proxy.Dockerfile -t proxy-image .
```

# Build the Server Image
```bash
docker build -f server.Dockerfile -t server-image .
```

# Start the Server Container
```bash
docker run --network app-network --name server-container server-image
```

# Start the Proxy Container 
- **-p**: Map port 3000 on local machine to port 3000 inside container
- **--network app-network**: Specify the docker network so containers can interact.
```bash
docker run -p 3000:3000 --network app-network --name proxy-container proxy-image
```
