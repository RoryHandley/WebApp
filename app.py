import multiprocessing
import argparse
import logging
import sys

# 3rd party imports
from proxy import proxy_main
from server import server_main
import common

logger = common.setup_custom_logger("APP")

def terminate_processes(processes):
    """Terminate all processes"""
    
    logger.info("KeyboardInterupt received - Terminating processes...")

    for process in processes:
        if process.is_alive():
            logger.info(f"{process.name} is still running. Terminating...")
            # Terminate the process
            process.terminate()
            # Use the join method to wait until the process is terminated
            process.join()
            logger.info(f"{process.name} terminated successfully.")

def parse_args():
    """Parse command line arguments"""
    # Now we need to take in the port and origin arguments from the command line
    # Create a parser object using the ArgumentParser class from the argparse module
    parser = argparse.ArgumentParser(description="Run a server and proxy server")

    # Call the add_argument method to add arguments
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('-o','--origin', type=str, required=True)
    parser.add_argument('--clear_cache', action='store_true')

    # Call the parse_args method to parse the command line arguments
    args = parser.parse_args()

    return args

def start_proxy(args):
    """Start the proxy server"""
    logger.info("Starting Proxy Server")
    proxy_main(args)

def start_server():
    """Start the server"""
    logger.info("Starting Server")
    server_main()

if __name__ == "__main__":
    # Create a logger object for the main process
    logger = common.setup_custom_logger("APP")
    
    # Parse command line arguments
    args = parse_args()

    # Create processes
    # Note args requires a tuple as an argument, so if the tuple has only one element we need to add a comma to force it to be recognized as a tuple
    process1 = multiprocessing.Process(target=start_server)
    process2 = multiprocessing.Process(target=start_proxy, args=(args,))
    
    # Add processes to a list
    processes = [process1, process2]

    try:
        # Start Processes
        process1.start()
        process2.start()

        # Print process IDs
        logger.info(f"{process1.pid} started successfully.")
        logger.info(f"{process2.pid} started successfully.")

        # Use join method to wait until processes are finished before proceeding
        # Note because each process contains an infinite loop, we will never reach the code after the join method
        process1.join()
        process1.join()

    except KeyboardInterrupt:
        terminate_processes(processes)
        logger.info("All Processes terminated successfully.")

# Multiprocessing reference - https://www.geeksforgeeks.org/multiprocessing-python-set-1/
# Logging reference - https://realpython.com/python-logging/