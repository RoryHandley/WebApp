import logging
import socket

# Constants
# Lets take this out of the script and put it in a config file 
PORT = 9999
IP = 'localhost'

server_memory = {'video1': 'video1.mp4',
                'video2': 'video2.mp4',
                'video3': 'video3.mp4',
                'video4': 'video4.mp4',
                'video5': 'video5.mp4',
                'video6': 'video6.mp4'}

def server_main(logger):

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
        data = clientsocket.recv(1024).decode()
        logger.info(f"Recieved request for '{data}'")
        
        clientsocket.send(server_memory[data].encode())

        

