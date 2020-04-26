from . import async_requests, default_logger, redis_functions, influxdb_functions, redis_functions

import toml
import time

logger = default_logger.logger
config = toml.load("config.toml")


def init_app():
    # _selected_lines = ro.get_all_lines()[:50]
    logger.info("Initializing redis client...")
    _selected_lines = config['pymt']['selected_lines']

    redis_stops = redis_functions.load_stops(_selected_lines)
    influx_client = influxdb_functions.init_influxdb()

    start_loop(redis_stops, influx_client)


def start_loop(stops, influx_client):
    loop_timer = time.time()

    while True:

        timer_requests = time.time()

        try:
            logger.info("Querying async requests to OASTh...")
            responses = async_requests.get_stops([s.uid for s in stops])
            logger.info("Received {} responses in {} seconds".format(len(responses), time.time() - timer_requests))

            timer_parsing = time.time()
            if responses:
                for response, stop in zip(responses, stops):
                    try:
                        stop.update(response)
                    except Exception as e:
                        logger.exception("There was an exception while parsing received response: {}".format(e))

            logger.info("Parsed responses in: {} seconds".format(time.time() - timer_parsing))

            influxdb_functions.save_to_influx(influx_client, stops)

        except Exception as e:
            logger.exception("There was an exception while getting data from the server: {}".format(e))

        time.sleep(32.0 - ((time.time() - loop_timer) % 32.0))
