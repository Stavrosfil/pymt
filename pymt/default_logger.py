import logging
import time

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


def timer(message=None):
    """Print the runtime of the decorated function"""

    def inner(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            if message:
                logger.info("[{}]: {}".format(func.__name__, message))
            else:
                logger.info("[{}]: Running...".format(func.__name__))
            start_time = time.perf_counter()  # 1
            value = func(*args, **kwargs)
            end_time = time.perf_counter()  # 2
            run_time = end_time - start_time  # 3
            logger.info(f"[{func.__name__}]: Finished in {run_time:.4f} secs")
            return value

        return wrapper_timer

    return inner


@timer()
def custom_timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        logger.info("Finished loop")
        return value

    return wrapper_timer


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
                logger.info("{}: {} @ {:.5}s".format(message, method.__name__, (te - ts)))
            return result

        return timed

    return inner
