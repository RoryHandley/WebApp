import multiprocessing
import argparse

from proxy import proxy_main
from server import server_main

def terminate_processes(processes):
    """Terminate all processes"""
    for process in processes:
        if process.is_alive():
            print(f"\n{process.name} is still running. Terminating...")
            process.terminate()
            process.join()
            print(f"{process.name} terminated successfully.")

def parse_args():
    """Parse command line arguments"""
    # Now we need to take in the port and origin arguments from the command line
    # Create a parser object using the ArgumentParser class from the argparse module
    parser = argparse.ArgumentParser(description="Run a server and proxy server")

    # Call the add_argument method to add arguments
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('-o','--origin', type=str, required=True)

    # Call the parse_args method to parse the command line arguments
    args = parser.parse_args()

    return args

if __name__ == "__main__":

    # Parse command line arguments
    args = parse_args()

    # Create processes
    process1 = multiprocessing.Process(target=server_main)
    process2 = multiprocessing.Process(target=proxy_main, args=(args,))

    processes = [process1, process2]
    
    try:
        # Start Processes
        process1.start()
        process2.start()

        # Use join method to wait until processes are finished before proceeding
        process1.join()
        process2.join()

        # Print process IDs
        print("Processes started successfully. Process IDs:")
        print(f"Server Process ID: {process1.pid}")
        print(f"Proxy Process ID: {process2.pid}")

        # Ask user for input to terminate processes
        input("\nPress Enter to terminate processes...\n")
    except KeyboardInterrupt:
        terminate_processes(processes)
        print("\nProcesses terminated successfully.")




# Multiprocessing reference - https://www.geeksforgeeks.org/multiprocessing-python-set-1/