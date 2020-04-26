import async_requests
import time
from influxdb import InfluxDBClient
import redis_operations as ro
import default_logger
import sys
import toml

logger = default_logger.logger
config = toml.load("config.toml")


def main():
    # _selected_lines = ro.get_all_lines()[:50]
    logger.info("Initializing redis client...")

    _selected_lines = config['pymt']['selected_lines']
    _influx_uri = config['influxdb']['uri']
    _influx_port = config['influxdb']['port']
    _influx_db = config['influxdb']['db']

    try:
        logger.info("Loading stops for lines: {}".format(_selected_lines))
        logger.info("Initializing redis client...")
        stops = ro.get_line_stops(_selected_lines)
        logger.info("Stops loaded from Redis: {}".format(len(stops)))
    except Exception as e:
        logger.exception("Failed to fetch data from Redis client: {}".format(e))
        sys.exit()

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
        logger.exception("Could not switch to {}: {}".format(_influx_db, e))
        sys.exit()

    start_loop(stops, influx_client)


def start_loop(stops, influx_client):
    loop_timer = time.time()

    while True:

        timer_requests = time.time()

        try:
            logger.info("Quering async requests to OASTh...")
            responses = async_requests.get_stops([s.uid for s in stops])
            logger.info("Received {} responses in {} seconds".format(len(responses), time.time() - timer_requests))
        except Exception as e:
            logger.exception("There was an exception while getting data from the server: {}".format(e))

        timer_parsing = time.time()

        if responses != []:
            for response, stop in zip(responses, stops):
                try:
                    stop.update(response)
                except Exception as e:
                    logger.exception("There was an exception while parsing received response: {}".format(e))

        logger.info("Parsed responses in: {} seconds".format(time.time() - timer_parsing))

        saveToInflux(influx_client, stops)

        time.sleep(32.0 - ((time.time() - loop_timer) % 32.0))


def saveToInflux(client, stops):
    logger.info("Writing to InfluxDB...")
    time2 = time.time()

    json_body = []

    for stop in stops:

        if (stop is not None):

            for bus in stop.buses:
                json_body.append(
                    {
                        "measurement": "busArival",
                        "tags": {
                            "bus_id": bus.bus_id,
                            "line_number": bus.line_number,
                            "stop_id": stop.uid,
                            "direction": stop.params['dir']
                        },
                        "time": bus.timestamp,
                        "fields": {
                            "estimated_arival": bus.arival
                        }
                    }
                )

    try:
        client.write_points(json_body)
        # print(json_body)
        logger.info("Successfully written in {} seconds".format(time.time() - time2))
    except Exception as e:
        logger.exception("There was an error writing to the database: {}".format(e))


if __name__ == '__main__':
    main()
