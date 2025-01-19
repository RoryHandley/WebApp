import sqlite3
import socket
import os

# 3rd party imports
from common import setup_custom_logger

# Create global logger
logger = setup_custom_logger("SERVER")

# Constants
# Lets take this out of the script and put it in a config file 
PORT = 9999
IP = '0.0.0.0'

def retrieve_data_from_db():
    """Create a connection object to our SQLite database"""
    
    db_path = '/app/videos.db'

    if not os.path.exists(db_path):
        logger.error(f"Database file not found at {db_path}")
        raise FileNotFoundError(f"Database file not found at {db_path}")
        
    
    # Create a connection object
    conn = sqlite3.connect(db_path)

    # Set the row_factory attribute of the connection object to sqlite3.Row
    # This will make sure the data is returned as a dictionary where the keys are the column names and the values are the row values
    conn.row_factory = sqlite3.Row

    return conn


def server_main():

    # Create a server socket object using the socket class from the socket module
    try:
        s = socket.socket()
        logger.info("Socket successfully created")
    except socket.error as err:
        logger.error(f"Socket creation failed with error {err}", exc_info=True)

    # Bind the socket to the address and port
    # Note the bind method takes a tuple as an argument
    # Note localhost means we are listenning to calls from the local machine
    try:
        s.bind((IP, PORT))
        # Listen for incoming connections
        # 5 here means that 5 connections are kept waiting if the server is busy and if a 6th socket tries to connect then the connection is refused.
        s.listen(5)
        logger.info(f"Socket is listening on {IP}:{PORT}")
    except socket.error as err:
        logger.exception(f"Socket binding failed with error {err}")
        # Note below would achieve the same thing. (Exception Info = True)
        logger.error(f"Socket binding failed with error {err}", exc_info=True)

    # A forever loop until we interrupt it or an error occurs
    while True:
        # Accept connections from outside
        clientsocket, addr = s.accept()
        logger.info(f"Got connection from {addr}")
        # Receive data from the client
        data = clientsocket.recv(1024).decode()
        logger.info(f"Recieved request for '{data}'")
        # Send query to SQLite database
        logger.info(f"Trying to connect to database.....")
        
        try:
            con = retrieve_data_from_db()
            cur = con.cursor()
            logger.info("Successfully connected to database")
        except FileNotFoundError as e:
            logger.error(f"Error connecting to database: {e}")
            clientsocket.send("Error connecting to database".encode())
            # Continue to the next iteration of the loop to accept new connections
            continue

        # Execute the query
        # Note column names are case sensitive and must be enclosed in backticks
        try:
            cur.execute("SELECT `Video Data` FROM videos WHERE `Video Title`=?", (data,))
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e}")
            clientsocket.send("Error executing query".encode())
            # Continue to the next iteration of the loop to accept new connections
            continue

        # Fetch the first result. Note fetchone returns a tuple
        result = cur.fetchone()
        
        # Close the connection to the database
        con.close()

        if result:
            # Send the first element of the tuple to the client
            clientsocket.send(result[0].encode())
            logger.info(f"Sending '{result[0]}' to client")
        else:
            clientsocket.send("Video not found".encode())
            logger.info("Video not found")

        # Close the client socket
        clientsocket.close()

if __name__ == "__main__":
    server_main()

        

