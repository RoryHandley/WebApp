import logging
import socket

# Constants
PORT = 9999
IP = 'localhost'

server_cache = {'video4': 'video4.mp4',
                'video5': 'video5.mp4',
                'video6': 'video6.mp4'}

def server_main():

    # Create a server socket object using the socket class from the socket module
    try:
        s = socket.socket()
        print("SERVER: Socket successfully created")
    except socket.error as err:
        print("SERVER: Socket creation failed with error %s" %(err))

    # Bind the socket to the address and port
    # Note the bind method takes a tuple as an argument
    # Note localhost means we are listenning to calls from the local machine
    try:
        s.bind((IP, PORT))
        # Listen for incoming connections
        # 5 here means that 5 connections are kept waiting if the server is busy and if a 6th socket tries to connect then the connection is refused.
        s.listen(5)
        print(f"SERVER: Socket is listening on {IP}:{PORT}")
    except socket.error as err:
        print(f"SERVER: Socket binding failed with error {err}")

    # A forever loop until we interrupt it or an error occurs
    while True:
        # Accept connections from outside
        clientsocket, addr = s.accept()
        print(f"SERVER: Got connection from {addr}")
        data = clientsocket.recv(1024).decode()
        print(f"SERVER: Recieved request for '{data}'")
        
        clientsocket.send(server_cache[data].encode())

        

