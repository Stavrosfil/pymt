import functools
import time

from pymt.default_logger import logger


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


def performance(client, measurement_name):
    def inner(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()  # 1
            value = func(*args, **kwargs)
            end_time = time.perf_counter()  # 2
            run_time = end_time - start_time  # 3
            json_body = {
                "measurement": measurement_name,
                # "tags": "stop",
                "time": time.time_ns(),
                "fields": {
                    "time_s": run_time
                },
            }
            client.write_points([json_body])

            return value

        return wrapper_timer

    return inner
