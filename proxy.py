import time
import socket
import redis
import redis.exceptions
import sys
from server import server_main

# As this is a proxy server, we need to create both a client and a server socket.
# The server socket will listen for incoming connections from the client. 
# The client socket will send messages to the server socket on the server if required.

# Dont like having to pass a logger object to every function. Can we make it global?


# Constants
SERVER_IP = 'localhost'
SERVER_PORT = 9999
REATTEMPTS = 3
    

def redis_cache_data(logger, client_data=None, server_data=None, clear_cache=False):
    """Store/Retrieve data in Redis Cache"""
    
    # Create a Redis client object. 
    r = redis.Redis(host='localhost', port=6379, db=0)
    # Test the connection. If the connection is unnsuccessful, an exception will be raised which we handle in the parent function. 
    r.ping()
    logger.info("Successfully connected to Redis Server. Cache available.")

    # Check if we need to clear the cache
    if clear_cache:
        # Clear the cache
        r.flushdb()
        return

    # If its just client_data (e.g. video3), we are checking if the data is in cache
    if client_data and not server_data:
        logger.info(f"Sending request to Redis Cache for {client_data}...")

        user_data = r.get(client_data)
        if user_data:
            logger.info(f"{client_data} X-Cache HIT: '{user_data.decode()}' retrieved from Redis Cache")
            return user_data
        else:
            logger.info(f"{client_data} X-Cache MISS: No Data retrieved from Redis Cache")
            return False
    else:
        # If its both client_data and server_data, we are adding data to cache
        logger.info(f"Adding data to Redis Cache...")
        r.set(client_data, server_data)
        logger.info(f"Data '{server_data}' added to Redis Cache")
        return
        

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
        logger.info(f"Connected to {origin}:{port}")
        # Send a message to the server
        c.send(data.encode())
        # Receive data from the server
        data = c.recv(1024).decode()
    except socket.error as e:
        logger.error(f"Error connecting to server: {e}", exc_info=True)

    return data

def proxy_main(args, logger):
    """Create a server socket object and bind to IP/Port. Call create_client_socket to send data to server if necessary"""
    # First check if we need to clear the cache
    if args.clear_cache:
        # Clear the cache
        redis_cache_data(logger, clear_cache=True)
        logger.info("Cache cleared on Redis Server")

    # Create a server socket object
    s = socket.socket()

    for i in range(0, REATTEMPTS):
        try:
            # Bind the socket to the address and port
            s.bind(('localhost', args.port))
            break
        except OSError:
            # OSError will occur when we try to bind IP/Port but previous process hasn't released them yet.
            if i <= REATTEMPTS:
                logger.error(f"IP and Port currently in use. Reattempting binding (Attempt {i + 1}/{REATTEMPTS})")
                # Increment counter
                i += 1 
                # Wait 5 seconds between reattempts.
                time.sleep(5)
            else:
                logger.error(f"Max retries attempted. Aborting....")
                sys.exit()

    # Listen for incoming connections. 
    # Note the listen method takes an argument which says we want to queue up to 5 connection requests before refusing connections.
    s.listen(5)
    logger.info(f"Binding Successful. listening on localhost:{args.port}")

    # A forever loop to accept connections from the client until we interrupt it or an error occurs
    while True:
        # Accepting incoming connections.
        client_socket, addr = s.accept()
        logger.info(f"Got connection from {addr}")

        # Cache Flag.
        cache_available = True

        # Receive data from the client
        client_data = client_socket.recv(1024).decode()
        logger.info(f"Received request for '{client_data}'")

        # Check if data is in Redis Cache
        try:
            cached_data = redis_cache_data(logger, client_data=client_data)
        except redis.exceptions.ConnectionError:
            cache_available = False
            logger.error("Unable to connect to Redis Server. No Cache available.")

        if cache_available and cached_data:
            try:
                client_socket.send(cached_data)
                logger.info(f"'{cached_data.decode()}' sent to client")
            except socket.error as e:
                logger.error(f"Error sending data to client: {e}", exc_info=True)
            continue  # Continue to the next iteration to accept new connections
        else:
            logger.info("No Cache available. Requesting data from server")
            # If not in proxy cache or unable to connect, we need to send a request to server
            server_data = create_client_socket(SERVER_PORT, SERVER_IP, client_data, logger)
            logger.info(f"Received '{server_data}' from server")
            # Send data to client socket
            logger.info(f"Sending '{server_data}' to client")
            # Add data to cache if cache available.
            try:
                redis_cache_data(logger, client_data=client_data, server_data=server_data)
                logger.info(f"Cache Available. {server_data} added to cache")
            except redis.exceptions.ConnectionError:
                logger.error("No cache available. Data not added to cache.")
            client_socket.send(server_data.encode())
        
        # Close the client socket immediately after sending/receiving data
        client_socket.close()

# Things to do:
# 1. Bug hit when ctrl+c is pressed. Need to handle this exception
# 2. Host SQLIte database on a separate server to simulate a real-world scenario and show benefits of caching



# Note to view a list of processes running on a port on localhost, run the following command:
# lsof -i -P | grep -i "listen" 
# Sockets Reference1 - https://www.geeksforgeeks.org/socket-programming-python/
# Sockets Reference2 - https://docs.python.org/3/howto/sockets.html
# Redis Client Reference - https://www.geeksforgeeks.org/redis-cache/
# Redis Server Reference - https://redis.io/docs/latest/operate/oss_and_stack/management/config/
# Neetcode reference - https://roadmap.sh/projects/caching-server``