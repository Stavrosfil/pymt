from pymt import logger, api, map, default_logger
from pymt.helpers import infl, mon
import pymt.models.oasth as model
import time
import datetime

influx = infl.init_influxdb()


@default_logger.timer("Getting bus telematics...")
def get_buses(lines):
    # Get telematics
    route_telematics = api.get_async([l.get_telematics_url(day) for day in range(2) for l in lines])
    return [model.Bus(b) for route in route_telematics for b in route if b]


def run():
    today = datetime.datetime.today().weekday()
    days = [today * 2, today * 2 + 1]
    logger.debug(days)
    loaded_lines = mon.load_lines(days)

    while True:

        new_day = datetime.datetime.today().weekday()
        if new_day != today:
            days = [new_day * 2, new_day * 2 + 1]
            loaded_lines = mon.load_lines(days)

        for l in loaded_lines:
            logger.debug("Line: {}".format(l.name))
            logger.debug("Stops: {}".format(len(l.stops)))
            logger.debug("Line days: {}".format(l.days))

        buses = get_buses(loaded_lines)
        [logger.debug(b.__dict__) for b in buses]

        infl.save_buses(influx, buses)

        m = map.init_map()
        [map.plot_route(m, line, days) for line in loaded_lines]
        for bus in buses:
            map.plot_bus(m, bus)
        map.save_map(m)

        print("-" * 100)
        time.sleep(15)
