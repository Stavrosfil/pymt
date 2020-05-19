import sys
import time
import geohash_hilbert as ghh

from influxdb import InfluxDBClient

from pymt import logger, config
from pymt.models.oasth import Stop

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


def save_to_influx(client, stops):
    logger.info("Writing to InfluxDB...")
    time2 = time.time()

    json_body = []

    for stop in stops:
        if stop is not None:
            for bus in stop.buses:
                json_body.append(
                    {
                        "measurement": "bus_arrival",
                        "tags": {
                            "bus_id": bus.uuid,
                            "line_number": bus.route_code,
                            "stop_id": stop.uid,
                            "direction": stop.params['dir']
                        },
                        "time": bus.timestamp,
                        "fields": {
                            "estimated_arrival": bus.arrival
                        }
                    }
                )

    try:
        client.write_points(json_body)
        logger.info("Successfully written in {} seconds".format(time.time() - time2))
    except Exception as e:
        logger.exception("There was an error writing to the database: {}".format(e))


def save_buses(client, buses):
    logger.info("Writing to InfluxDB...")
    time2 = time.time()

    json_body = []

    for bus in buses:
        if bus is not None:
            json_body.append(
                {
                    "measurement": "bus_location",
                    "tags": {
                        "uuid": bus.uuid,
                        "route_code": bus.route_code,
                        "geohash": ghh.encode(lng=bus.lon, lat=bus.lat, precision=5)
                    },
                    "time": bus.timestamp,
                    "fields": {
                        "lon": bus.lon,
                        "lat": bus.lat,
                        "geohash": ghh.encode(lng=bus.lon, lat=bus.lat, precision=5),
                    }
                }
            )

    try:
        client.write_points(json_body)
        logger.info("Successfully written in {} seconds".format(time.time() - time2))
    except Exception as e:
        logger.exception("There was an error writing to the database: {}".format(e))