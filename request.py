import socket
import argparse 
import time

# Create parser object
parser = argparse.ArgumentParser(description="Send a request to the proxy server")

# Add arguments
parser.add_argument('-d', '--data', type=str, required=True)

# Parse arguments
args = parser.parse_args()

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the proxy server
# Connect to the proxy server
try:
    c.connect(('localhost', 3000))
    start_time = time.time()  # Capture start time
    c.send(args.data.encode())
    response = c.recv(1024).decode()
    end_time = time.time()  # Capture end time
    print(response)
    
    # Calculate time taken in microseconds
    time_taken = (end_time - start_time) * 1_000_000  # Convert seconds to microseconds
    print(f"Time taken: {time_taken:.2f} microseconds")
except socket.error as e:
    print(f"Error connecting to proxy server: {e}")
finally:
    c.close()