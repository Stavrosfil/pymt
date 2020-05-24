import logging

import toml

from pymt import default_logger

logger = default_logger.init_logger()
config = toml.load("config.toml")
selected_lines = config['pymt']['selected_lines']

level = config['pymt']['log_level']

logger.setLevel(logging.DEBUG if level == 'DEBUG' else logging.INFO)
