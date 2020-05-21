from pymt import default_logger, logger, influxdb_functions, mongo_functions, api, map
from pymt import selected_lines
import pymt.models.oasth as model
import time


@default_logger.timer("Getting bus telematics...")
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
                bus = model.Bus(bus)
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

    m = map.init_map()
    [map.plot_route(m, line) for line in lines]
    for bus in buses:
        map.plot_bus(m, bus)
    map.save_map(m)

    print("-" * 100)
    time.sleep(15)
