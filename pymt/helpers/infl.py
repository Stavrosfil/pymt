import sys
import geohash2
from influxdb import InfluxDBClient
from pymt import logger, config, default_logger

_influx_uri = config['influxdb']['uri']
_influx_port = config['influxdb']['port']
_influx_db = config['influxdb']['db']


def init_influxdb():
    try:
        logger.info("Initializing InfluxDB client: {}:{}".format(_influx_uri, _influx_port))
        influx_client = InfluxDBClient(_influx_uri, _influx_port)
        logger.info("Client initialized successfully")
    except Exception as e:
        logger.exception("Failed to initialize InfluxDB client: {}".format(e))
        sys.exit()

    try:
        dbs = influx_client.get_list_database()
        if {'name': 'bus_arrivals'} not in dbs:
            logger.info("Creating database: {}".format(_influx_db))
            influx_client.create_database(_influx_db)
        logger.info("Switching to database: {}".format(_influx_db))
        influx_client.switch_database(_influx_db)
        logger.info("Successfully switched to: {}".format(_influx_db))
    except Exception as e:
        logger.exception("Could not switch to or create {}: {}".format(_influx_db, e))
        sys.exit()

    return influx_client


@default_logger.timer("Writing to InfluxDB...")
def save_buses(client, buses):
    json_body = []

    for bus in buses:
        if bus is not None:
            geohash = geohash2.encode(bus.lat, bus.lon, precision=7)
            json_body.append(
                {
                    "measurement": "bus_location",
                    "tags": {
                        "uuid": bus.uuid,
                        "route_code": bus.route_code,
                        "geohash": geohash
                    },
                    "time": bus.timestamp,
                    "fields": {
                        "lon": bus.lon,
                        "lat": bus.lat,
                        "geohash": geohash,
                    }
                }
            )

    try:
        client.write_points(json_body)
    except Exception as e:
        logger.exception("There was an error writing to the database: {}".format(e))
