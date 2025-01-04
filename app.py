import multiprocessing
import argparse
import logging
import sys

from proxy import proxy_main
from server import server_main

def setup_custom_logger(name):
    """Function to create logger object for each process"""
    # Create custom logger object using the Logger class from the logging module
    logger = logging.getLogger(name)
    # Set the minimum log level to INFO
    # Note this will default to WARNING if we don't set it, which is inherited from the root logger
    logger.setLevel(logging.INFO)

    # Unlike with the root logger, we can't use the basicConfig method to configure the logger
    # Instead, we need to configure the custom object using handlers and formatters
    
    # Create a file handler to send log messages to a file
    # Create a stream handler to send log messages to the console
    file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Once we've initialzed the handlers, we need to add them to the logger using the addHandler method
    # Note the handlers can be viewed by looking at the .handlers attribute of the logger object
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Handlers send the logs to the output destination, whereas formatter objects specify the layout of the log messages
    # Create a formatter object using the Formatter class from the logging module
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s', 
                                  datefmt="%Y-%m-%d %H:%M")
    
    # Add the formatter to the handlers
    # Note setFormatter is a method of the Handler class, whereas addHandler is a method of the Logger class
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    """ Note below is how we would do the same thing with the root logger
    
    logging.basicConfig(filename="app.log",
                        encoding="utf-8",
                        filemode="a",
                        level=logging.DEBUG, 
                        format='%(asctime)s:%(name)s:%(message)s',
                        datefmt="%Y-%m-%d %H:%M",
                        )
    """

    # Return the logger object
    return logger

def terminate_processes(processes, log):
    """Terminate all processes"""
    for process in processes:
        if process.is_alive():
            log.info(f"{process.name} is still running. Terminating...")
            # Terminate the process
            process.terminate()
            # Use the join method to wait until the process is terminated
            process.join()
            log.info(f"{process.name} terminated successfully.")

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
    logger = setup_custom_logger("PROXY")
    logger.info("Starting Proxy Server")
    proxy_main(args, logger)

def start_server():
    """Start the server"""
    logger = setup_custom_logger("SERVER")
    logger.info("Starting Server")
    server_main(logger)

if __name__ == "__main__":
    # Create a logger object for the main process
    logger = setup_custom_logger("APP")
    
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
        terminate_processes(processes, logger)
        logger.info("All Processes terminated successfully.")

# Multiprocessing reference - https://www.geeksforgeeks.org/multiprocessing-python-set-1/
# Logging reference - https://realpython.com/python-logging/