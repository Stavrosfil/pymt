import async_requests
import time
from influxdb import InfluxDBClient
import redis_operations as ro
import logging
import sys


def main():

    # SELECTED_LINES = ro.get_all_lines()[:50]

    SELECTED_LINES = ['01N', '01X', '02K', '03K', '10', '07', '31']
    INFLUX_URI = 'localhost'
    INFLUX_PORT = 8089
    INFLUX_DB = 'bus_arrivals'

    logging.basicConfig(filename='pymt.log',
                        filemode='a',
                        format='%(asctime)s - %(process)d - %(levelname)s - %(name)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO)

    try:
        logging.info("Loading stops for lines: {}".format(SELECTED_LINES))
        logging.info("Initializing redis client...")
        stops = ro.get_line_stops(SELECTED_LINES)
        logging.info("Stops loaded from Redis: {}".format(len(stops)))
    except Exception as e:
        logging.error("Failed to fetch data from Redis client: {}".format(e))
        sys.exit()

    try:
        logging.info("Initializing InfluxDB client: {}:{}".format(INFLUX_URI, INFLUX_PORT))
        influx_client = InfluxDBClient(INFLUX_URI, INFLUX_PORT)
        logging.info("Client initialized successfully")
    except Exception as e:
        logging.error("Failed to initialize InfluxDB client: {}".format(e))
        sys.exit()

    try:
        dbs = influx_client.get_list_database()
        if {'name': 'bus_arrivals'} not in dbs:
            logging.info("Creating database: {}".format(INFLUX_DB))
            influx_client.create_database(INFLUX_DB)
        logging.info("Switching to database: {}".format(INFLUX_DB))
        influx_client.switch_database(INFLUX_DB)
        logging.info("Successfully switched to: {}".format(INFLUX_DB))
    except Exception as e:
        logging.error("Could not switch to {}: {}".format(INFLUX_DB, e))
        sys.exit()

    start_loop(stops, influx_client)


def start_loop(stops, influx_client):

    loop_timer = time.time()

    while True:

        logging.info("Quering async requests to OASTh...")
        time1 = time.time()

        try:
            responses = async_requests.get_stops([s.uid for s in stops])
            logging.info("Received {} responses in {} seconds".format(len(responses), time.time() - time1))
        except Exception as e:
            logging.error("There was an exception while getting data from the server: {}".format(e))

        if responses != []:
            for response, stop in zip(responses, stops):
                try:
                    stop.update(response)
                except Exception as e:
                    logging.error("There was an exception while parsing received response: {}".format(e))

        saveToInflux(influx_client, stops)

        time.sleep(32.0 - ((time.time() - loop_timer) % 32.0))


def saveToInflux(client, stops):

    logging.info("Writing to InfluxDB...")
    time2 = time.time()

    json_body = []

    for stop in stops:

        if(stop is not None):

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
        logging.info("Successfully written in {} seconds".format(time.time() - time2))
    except Exception as e:
        logging.error("There was an error writing to the database: {}".format(e))


if __name__ == '__main__':
    main()
