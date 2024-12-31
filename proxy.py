import logging
import socket
from server import server_main

# As this is a proxy server, we need to create both a client and a server socket.
# The server socket will listen for incoming connections from the client. 
# The client socket will send messages to the server socket on the server if required.

# Constants
SERVER_IP = 'localhost'
SERVER_PORT = 9999

# Create proxy cache dictionary
proxy_cache = {'video1': 'video1.mp4', 
               'video2': 'video2.mp4', 
               'video3': 'video3.mp4'}
    

def create_client_socket(port, origin, data, logger):
    """Cteate a client socket object"""
    # Create a client socket object using the socket class from the socket module
    # pass in the address family and the socket type as arguments
    # AF_INET is the address family for IPv4
    # SOCK_STREAM is the socket type for TCP connections
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Call the connect method on the socket object to try to connect to the server
        c.connect((origin, port))
        print(f"PROXY: Connected to {origin}:{port}")
        # Send a message to the server
        c.send(data.encode())
        # Receive data from the server
        data = c.recv(1024).decode()
    except socket.error as e:
        logger.error(f"Error connecting to server: {e}", exc_info=True)

    return data

def proxy_main(args, logger):
    """Create a server socket object and bind to IP/Port. Call create_client_socket to send data to server if necessary"""

    # Check if we need to clear the cache
    if args.clear_cache:
        proxy_cache.clear()
        logger.info("Cache cleared")

    # Create a server socket object
    s = socket.socket()

    # Bind the socket to the address and port
    s.bind(('localhost', args.port))

    # Listen for incoming connections. 
    # Note the listen method takes an argument which says we want to queue up to 5 connection requests before refusing connections.
    s.listen(5)
    logger.info(f"listening on localhost:{args.port}")

    # A forever loop to accept connections from the client until we interrupt it or an error occurs
    while True:
        client_socket, addr = s.accept()
        logger.info(f"Got connection from {addr}")

        # Receive data from the client
        client_data = client_socket.recv(1024).decode()
        logger.info(f"Received request for '{client_data}'")

        # Check if data is in cache
        if client_data in proxy_cache:
            # If in cache, send data directly to client.
            logger.info(f"X-Cache: HIT: {proxy_cache[client_data]}")
            logger.info(f"Sending '{proxy_cache[client_data]}' to client")
            try:
                client_socket.send(proxy_cache[client_data].encode())
                logger.info(f"Successfully sent {proxy_cache[client_data]} to client")
            except socket.error as e:
                logger.error(f"Error sending data to client: {e}", exc_info=True)    
        else:
            # If not in proxy cache, send request to server
            logger.info(f"X-Cache: MISS")
            # Create client socket on proxy server and connect to server socket on server
            server_data = create_client_socket(SERVER_PORT, SERVER_IP, client_data, logger)
            logger.info(f"Received '{server_data}' from server")
            # Send data to client socket
            logger.info(f"Sending '{server_data}' to client")
            client_socket.send(server_data.encode())
            # Add data to cache
            proxy_cache[client_data] = server_data
        
        # Close the client socket immediately after sending/receiving data
        client_socket.close()


# Note to view a list of processes running on a port on localhost, run the following command:
# lsof -i -P | grep -i "listen" 
# Reference - https://www.geeksforgeeks.org/socket-programming-python/
# Reference2 - https://docs.python.org/3/howto/sockets.html
# Neetcode reference - https://roadmap.sh/projects/caching-server``