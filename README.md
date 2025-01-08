This project implements a simple client-server architecture where the client sends requests to the server via a proxy. The proxy firstly checks the cache server (Redis) - If the file is in cache, it is returned to the client. If the file is not in cache, the proxy sends a request to the server which will then retrieve the data from a SQLite database and then send the response back to the client. The client measures the time taken for the request-response cycle and displays the result in microseconds.

Components
1. Server (server.py)
The server listens for incoming client connections on a specified IP and port.
Upon receiving a request, the server queries a SQLite database (videos.db) for data matching the request. It sends the data or an error message back to the client.

2. Proxy (proxy.py)
The proxy server listens for incoming client connections.
It forwards client requests to the main server and sends the response back to the client.
It operates as a bridge between the client and the server.

3. Client (client.py)
The client sends a request to the proxy server with specific data.
It waits for a response from the proxy, which in turn is from the server.
The client measures the round-trip time of the request in microseconds.

4. Logger (logger.py)
Custom logging is implemented using Python's logging module.
Logs are written to both a file (app.log) and displayed in the console for easy monitoring.

Requirements
Python 3.x
SQLite3
argparse module for handling command-line arguments
logging module for logging messages
