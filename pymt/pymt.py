import time
from pprint import pprint

from pymt import default_logger, logger, influxdb_functions, mongo_functions, api, map
from pymt import selected_lines
from pymt.models.oasth import async_requests


# def init_app():
#     logger.info("Initializing redis client...")
#     _selected_lines = config['pymt']['selected_lines']
#
#     # redis_stops = redis_functions.load_stops(_selected_lines)
#     stops = mongo_functions.get_route_stops_dict()
#     influx_client = influxdb_functions.init_influxdb()
#
#     start_loop(stops, influx_client)


# def start_loop(stops, influx_client):
#     loop_timer = time.time()
#
#     while True:
#         timer_requests = time.time()
#
#         try:
#             # logger.log_time("Initiating requests")
#             # run()
#             logger.info("Querying async requests to OASTh...")
#             responses = async_requests.get_stops([s.uid for s in stops])
#             logger.info("Received {} responses in {} seconds".format(len(responses), time.time() - timer_requests))
#
#             timer_parsing = time.time()
#             if responses:
#                 for response, stop in zip(responses, stops):
#                     try:
#                         stop.update(response)
#                     except Exception as e:
#                         logger.exception("There was an exception while parsing received response: {}".format(e))
#
#             logger.info("Parsed responses in: {} seconds".format(time.time() - timer_parsing))
#
#             influxdb_functions.save_to_influx(influx_client, stops)
#
#         except Exception as e:
#             logger.exception("There was an exception while getting data from the server: {}".format(e))
#
#         time.sleep(32.0 - ((time.time() - loop_timer) % 32.0))


class CustomBus(object):
    def __init__(self, d):
        # self.__dict__ = d
        self.lon = float(d.get('CS_LNG'))
        self.lat = float(d.get('CS_LAT'))
        self.uuid = d.get('VEH_NO')
        self.route_code = d.get('ROUTE_CODE')
        self.timestamp = time.time_ns()


def time_function(func):
    def wrapper():
        start = time.time()
        func()
        print("Received {} responses in {} seconds".format("test", time.time() - start))

    return wrapper


@default_logger.log_time("Request and process task")
def get_buses(lines):
    buses = []

    routes_to_request = []

    for line in lines:
        logger.debug("Line: {}".format(line.name))
        logger.debug("Stops: {}".format(len(line.stops)))
        logger.debug("Line days: {}".format(line.days))

        for day in range(2):
            routes_to_request.append(line.days[day])
            # stop_telematics = api.get_line_telematics(line, day)

    # Get telematics
    route_telematics = api.get_async(routes_to_request)
    for r in route_telematics:
        if r is not None:
            for bus in r:
                bus = CustomBus(bus)
                buses.append(bus)
                logger.debug(bus.__dict__)

    return buses


# ---------------------------------------------------------------------------------

influx = influxdb_functions.init_influxdb()

if not selected_lines:
    selected_lines = [l.name for l in mongo_functions.get_all_lines()]
    
lines = []
for line_name in selected_lines:
    line = mongo_functions.get_line_by_name(line_name)
    line.stops = mongo_functions.get_route_stops(line_name)
    lines.append(line)

while True:
    buses = get_buses(lines)
    influxdb_functions.save_buses(influx, buses)

    # m = map.init_map()
    # [map.plot_route(m, line) for line in lines]
    # for bus in buses:
    #     map.plot_point(m, (bus.lat, bus.lon))
    # map.save_map(m)

    print("-" * 100)
    time.sleep(15)
