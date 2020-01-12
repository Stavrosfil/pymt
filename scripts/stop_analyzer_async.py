from pathlib import Path
import json
import async_requests
from modules import Stop as Stop
import time
from influxdb import InfluxDBClient

'''
A script to analyze a selected stop and output the data to an InfluxDB server.

TODO: Input is a line or a stop?
'''

stop_ids = []
stop_dirs = []


def main():

    DATA_FOLDER = Path("data")

    try:
        print("\n>>> Opening line data file...")
        with open(DATA_FOLDER / "test.json", "r") as f:

            for stop in json.load(f):
                stop_ids.append(stop["params"]["start"])
                stop_dirs.append(stop["params"]["dir"])

                # print(f'Stop ID: { str(stop_ids[-1]) }')

            print("Read {} stops".format(len(stop_ids)))

            f.close()

    except IOError as e:
        print("Could not read file: ", DATA_FOLDER / "test.json")
        print(e)

    client = InfluxDBClient('localhost', 8089)
    client.create_database('bustests')
    client.switch_database('bustests')
    # print(client.get_list_database())

    loop_timer = time.time()

    while True:

        saveToInflux(client)

        time.sleep(32.0 - ((time.time() - loop_timer) % 32.0))


def saveToInflux(client):

    # stop_ids = stop_ids[0:50]

    print("\n>>> Quering async requests to server...")
    time1 = time.time()
    responses = async_requests.get_stops(stop_ids)
    print("Received {} responses in {} seconds".format(
        len(responses), time.time() - time1))

    print("\n>>> Writing data to influxdb server...")
    time2 = time.time()

    json_body = []

    for response, stop_id, direction in zip(responses, stop_ids, stop_dirs):

        stop = Stop.Stop(response, stop_id)

        if(stop is not None):

            for bus in stop.buses:

                json_body.append(
                    {
                        "measurement": "busArival",
                        "tags": {
                            "bus_id": bus.bus_id,
                            "line_number": bus.line_number,
                            "stop_id": stop_id,
                            "direction": direction
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
    except Exception as e:
        print("There was an error writing to the database: {}".format(e))

    print("Files successfully written in {} seconds".format(time.time() - time2))


if __name__ == '__main__':
    main()
