import sys
import time

import geohash2
from influxdb import InfluxDBClient

import pymt.helpers.metadata
from pymt import logger, config

_influx_uri = config['influxdb']['uri']
_influx_port = config['influxdb']['port']
_influx_db = config['influxdb']['db']


class InfluxClient:
    # TODO: Initialize object in a sensible way
    client = influx_client = InfluxDBClient(_influx_uri, _influx_port)
    client.switch_database(_influx_db)

    def __init__(self):
        try:
            logger.info("Initializing InfluxDB client: {}:{}".format(_influx_uri, _influx_port))
            influx_client = InfluxDBClient(_influx_uri, _influx_port)
            logger.info("Client initialized successfully")
        except Exception as e:
            logger.exception("Failed to initialize InfluxDB client: {}".format(e))
            sys.exit()

        try:
            dbs = influx_client.get_list_database()
            if {'name': _influx_db} not in dbs:
                logger.info("Creating database: {}".format(_influx_db))
                influx_client.create_database(_influx_db)
            logger.info("Switching to database: {}".format(_influx_db))
            influx_client.switch_database(_influx_db)
            logger.info("Successfully switched to: {}".format(_influx_db))
        except Exception as e:
            logger.exception("Could not switch to or create {}: {}".format(_influx_db, e))
            sys.exit()

        self.client = influx_client

    @pymt.helpers.metadata.performance(client, "run_time")
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

        self.batch_start(len(buses))
        self.write_json(json_body)
        self.batch_end(len(buses))

    def batch_start(self, number):
        json_body = {
            "measurement": "batch_start",
            # "tags": "start",
            "time": time.time_ns(),
            "fields": {
                "buses": number
            }
        }
        self.write_json([json_body])

    def batch_end(self, number):
        json_body = {
            "measurement": "batch_stop",
            # "tags": "stop",
            "time": time.time_ns(),
            "fields": {
                "number": number,
            },
        }
        self.write_json([json_body])

    # def performance(self, measurement_name, run_time):
    #     json_body = {
    #         "measurement": measurement_name,
    #         # "tags": "stop",
    #         "time": time.time_ns(),
    #         "fields": run_time,
    #     }
    #     self.write_json(json_body)

    def write_json(self, json_body):
        if not isinstance(json_body, list):
            json_body = list(json_body)
        try:
            self.client.write_points(json_body)
        except Exception as e:
            logger.exception("There was an error writing to the database: {}".format(e))
