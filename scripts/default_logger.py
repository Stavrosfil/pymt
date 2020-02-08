# logging_example.py

import logging

# Create a custom logger
logger = logging.getLogger('pymt')

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('pymt.log', 'a')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_format = f_format = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s - %(name)s - %(message)s',
                                        datefmt='%d-%b-%y %H:%M:%S',)

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
