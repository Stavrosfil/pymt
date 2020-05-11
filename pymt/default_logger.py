import logging
import time

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('pymt.log')

# Set severety logging level
logger.setLevel(logging.INFO)
f_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
# c_format = f_format = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s - %(name)s - %(message)s')
c_format = f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


def log_time(message):

    def inner(method):
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            if 'log_time' in kw:
                name = kw.get('log_name', method.__name__.upper())
                kw['log_time'][name] = int((te - ts) * 1000)
            else:
                logger.info("{}: {} @ {}ms".format(message, method.__name__, (te - ts) * 1000))
            return result

        return timed

    return inner
