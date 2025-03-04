import logging


def get_logger(
    fname="seviper.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
):
    """
    Configures and returns a logger instance.

    If the logger does not already have handlers, this function sets up a file
    handler and a console handler with the specified logging level, format, and
    date format.

    Parameters:
    fname (str): The filename for the log file. Defaults to "seviper.log".
    level (int): The logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.
    format (str): The format string for log messages. Defaults to "[%(asctime)s] %(levelname)s - %(message)s".
    datefmt (str): The date format string for log messages. Defaults to "%H:%M:%S".

    Returns:
    logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger()

    if not logger.hasHandlers():
        logging.basicConfig(filename=fname, level=level, format=format, datefmt=datefmt)
        console = logging.StreamHandler()
        console.setLevel(level=level)
        console.setFormatter(logging.Formatter(fmt=format, datefmt=datefmt))

        logging.getLogger().addHandler(console)

    return logging
