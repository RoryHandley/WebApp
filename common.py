import logging

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