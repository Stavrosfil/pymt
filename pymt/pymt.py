import time
from pprint import pprint

from pymt import logger, config, influxdb_functions, mongo_functions, redis_functions, api
from pymt import selected_lines
from pymt.models.oasth import async_requests


def init_app():
    logger.info("Initializing redis client...")
    _selected_lines = config['pymt']['selected_lines']

    # redis_stops = redis_functions.load_stops(_selected_lines)
    stops = mongo_functions.get_route_stops_dict()
    influx_client = influxdb_functions.init_influxdb()

    start_loop(stops, influx_client)


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


class CustomBus(object):
    def __init__(self, d):
        self.__dict__ = d


# m = map.init_map()

for line in selected_lines:
    print("Line:\t\t", line)
    stops = mongo_functions.get_route_stops(line)
    print("Stops:\t\t", len(stops))

    line = mongo_functions.get_line_by_name(line)

    print("Line days:\t", line.days)
    stop_telematics = api.get_line_telematics(line)
    buses = []
    if stop_telematics is not None:
        for bus in stop_telematics:
            print(bus)
            bus = CustomBus(bus)
            buses.append(bus)
            coords = (bus.CS_LAT, bus.CS_LNG)
            # map.plot_point(m, coords)

    # pprint(stop_telematics, indent=1)
    print("-" * 100)
    # map.plot_route(m, stops)

# map.save_map(m)
