import functools
import sys
import time

import geohash2
from influxdb import InfluxDBClient

import pymt.helpers.metadata
from pymt import logger, config

_influx_uri = config['influxdb']['uri']
_influx_port = config['influxdb']['port']
_locations_db = config['influxdb']['db']
_metrics_db = config['influxdb']['metrics_db']


def init_client(uri, port, db):
    try:
        logger.info("Initializing InfluxDB client: {}:{}".format(uri, port))
        influx_client = InfluxDBClient(uri, port)
        logger.info("Client initialized successfully")
    except Exception as e:
        logger.exception("Failed to initialize InfluxDB client: {}".format(e))
        sys.exit()

    try:
        dbs = influx_client.get_list_database()
        if {'name': db} not in dbs:
            logger.info("Creating database: {}".format(db))
            influx_client.create_database(db)
        logger.info("Switching to database: {}".format(db))
        influx_client.switch_database(db)
        logger.info("Successfully switched to: {}".format(db))
    except Exception as e:
        logger.exception("Could not switch to or create {}: {}".format(db, e))
        sys.exit()

    return influx_client


metrics_client = init_client(_influx_uri, _influx_port, _metrics_db)


def performance(measurement_name=None, prefix=None):
    def inner(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()  # 1
            value = func(*args, **kwargs)
            end_time = time.perf_counter()  # 2
            run_time = end_time - start_time  # 3
            if measurement_name is None:
                mn = func.__name__
            else:
                mn = measurement_name
            json_body = {
                "measurement": f"{prefix}.{mn}" if prefix is not None else mn,
                # "tags": "stop",
                "time": time.time_ns(),
                "fields": {
                    "time_s": run_time
                },
            }
            metrics_client.write_points([json_body])

            return value

        return wrapper_timer

    return inner


class InfluxClient:

    def __init__(self):
        self.client = init_client(_influx_uri, _influx_port, _locations_db)

    @performance(prefix="influx")
    @pymt.helpers.metadata.timer("Writing to InfluxDB...")
    def save_buses(self, buses):
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
                        }
                    }
                )

        self.write_json(json_body)

    def batch_start(self, requests):
        json_body = {
            "measurement": "batch_start",
            "time": time.time_ns(),
            "fields": {
                "requests": requests,
            }
        }
        self.write_json([json_body])

    def batch_end(self, buses):
        json_body = {
            "measurement": "batch_stop",
            "time": time.time_ns(),
            "fields": {
                "buses": buses,
            },
        }
        self.write_json([json_body])

    def write_json(self, json_body):
        if not isinstance(json_body, list):
            json_body = list(json_body)
        try:
            self.client.write_points(json_body)
        except Exception as e:
            logger.exception("There was an error writing to the database: {}".format(e))
