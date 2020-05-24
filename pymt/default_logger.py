import logging


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def init_logger():
    # c_format = f_format = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s - %(name)s - %(message)s')
    # c_format = f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    c_format = f_format = logging.Formatter(f'{bcolors.WARNING}[%(levelname)s] {bcolors.HEADER}- %(message)s')

    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('pymt.log')

    # Set severity logging level
    logger.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
