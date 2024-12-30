import socket
import argparse
import proxy

# Create parser object
parser = argparse.ArgumentParser(description="Send a request to the proxy server")

# Add arguments
parser.add_argument('-d', '--data', type=str, required=True)

# Parse arguments
args = parser.parse_args()

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the proxy server
try:
    c.connect(('localhost', 3000))
    c.send(args.data.encode())
    print(c.recv(1024).decode())
except socket.error as e:
    print(f"Error connecting to proxy server: {e}")