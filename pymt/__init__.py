import toml

from pymt import default_logger

logger = default_logger.logger
config = toml.load("config.toml")
selected_lines = config['pymt']['selected_lines']
