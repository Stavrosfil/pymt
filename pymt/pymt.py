import datetime
import time

import pymt.helpers.infl
import pymt.helpers.metadata
import pymt.models.oasth as model
from pymt import logger, api, map
from pymt.helpers import infl, mon

influx_client = infl.InfluxClient()


@pymt.helpers.infl.performance(prefix="pymt")
@pymt.helpers.metadata.timer("Getting bus telematics...")
def get_buses(routes):
    logger.warning(f"Route urls to request: {len(routes)}")
    route_telematics = api.get_async(routes)
    return [model.Bus(b) for route in route_telematics for b in route if b]


def run():
    today = datetime.datetime.today().weekday()
    days = [today * 2, today * 2 + 1]
    logger.warning(f"Days: {days}")
    loaded_lines = mon.load_lines(days)

    while True:

        new_day = datetime.datetime.today().weekday()
        if new_day != today:
            days = [new_day * 2, new_day * 2 + 1]
            today = new_day
            loaded_lines = mon.load_lines(days)
            logger.warning(f"Days: {days}")

        for l in loaded_lines:
            logger.debug("Line: {}".format(l.name))
            logger.debug("Stops: {}".format(len(l.stops)))
            logger.debug("Line days: {}".format(l.days))

        routes = [y for day in days for l in loaded_lines if (y := l.get_telematics_url(day)) is not None]
        influx_client.batch_start(len(routes))

        buses = get_buses(routes)
        [logger.debug(b.__dict__) for b in buses]
        logger.info(f"Received {len(buses)} bus objects")

        influx_client.save_buses(buses)
        influx_client.batch_end(len(buses))

        m = map.init_map()
        [map.plot_route(m, line, days) for line in loaded_lines]
        for bus in buses:
            map.plot_bus(m, bus)
        map.save_map(m)

        print("-" * 100)
        time.sleep(15)
