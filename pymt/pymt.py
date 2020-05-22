from pymt import default_logger, logger, influxdb_functions, mongo_functions, api, map
from pymt import config
import pymt.models.oasth as model
import time
import datetime


@default_logger.timer("Getting bus telematics...")
def get_buses(lines):
    # Get telematics
    route_telematics = api.get_async([l.get_telematics_url(day) for day in range(2) for l in lines])
    return [model.Bus(b) for route in route_telematics for b in route if b]


# ---------------------------------------------------------------------------------

influx = influxdb_functions.init_influxdb()
selected_lines = config['pymt']['selected_lines']


def load_lines(days, lines=selected_lines):
    _lines = []
    if not lines:
        _lines = mongo_functions.get_all_lines()
    else:
        _lines = [mongo_functions.get_line_by_name(line_name) for line_name in lines]
    [logger.debug(f"Selected lines: {l.__dict__}") for l in _lines]
    for d in days:
        for line in _lines:
            line.stops[d] = mongo_functions.get_route_stops(route_id=line.days[d])
    return _lines


def run():
    today = datetime.datetime.today().weekday()
    days = [today * 2, today * 2 + 1]
    logger.debug(days)
    loaded_lines = load_lines(days)

    while True:

        new_day = datetime.datetime.today().weekday()
        if new_day != today:
            days = [new_day * 2, new_day * 2 + 1]
            loaded_lines = load_lines(days)

        for l in loaded_lines:
            logger.debug("Line: {}".format(l.name))
            logger.debug("Stops: {}".format(len(l.stops)))
            logger.debug("Line days: {}".format(l.days))

        buses = get_buses(loaded_lines)
        [logger.debug(b.__dict__) for b in buses]

        influxdb_functions.save_buses(influx, buses)

        m = map.init_map()
        [map.plot_route(m, line, days) for line in loaded_lines]
        for bus in buses:
            map.plot_bus(m, bus)
        map.save_map(m)

        print("-" * 100)
        time.sleep(15)
