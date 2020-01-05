from pathlib import Path
import sys
import re
import json
import requests
import async_requests
from modules import Stop as Stop

from datetime import datetime

from influxdb import InfluxDBClient

'''
A script to analyze a selected stop and output the data to an InfluxDB server.

TODO: Input is a line or a stop?
'''


def main():

    DATA_FOLDER = Path("data")

    stop_ids = []

    try:
        print(">>> Opening line data file...")
        with open(DATA_FOLDER / "test.json", "r") as f:

            for stop in json.load(f):
                stop_ids.append(stop["params"]["start"])

                # print(f'Stop ID: { str(stop_ids[-1]) }')

            print("Read {} stops".format(len(stop_ids)))

            f.close()

    except IOError as e:
        print("Could not read file: ", DATA_FOLDER / "test.json")

    client = InfluxDBClient('localhost', 8086)
    client.create_database('bustests')
    client.switch_database('bustests')
    # print(client.get_list_database())

    saveToInflux(client, stop_ids)


def saveToInflux(client, stop_ids):

    print(">>> Quering async requests to server...")

    # stop_ids = stop_ids[0:50]

    responses = async_requests.get_stops(stop_ids)

    print("Received {} responses".format(len(responses)))
    print(">>> Writing data to influxdb server...")

    for response, stop_id in zip(responses, stop_ids):

        stop = Stop.Stop(response, stop_id)

        if(stop is not None):

            for bus in stop.buses:

                json_body = {
                    "measurement": "busArival",
                    "tags": {
                        "bus_id": bus.bus_id,
                        "line_number": bus.line_number,
                        "stop_id": stop.stop_id
                    },
                    # "time": current_time,
                    "fields": {
                        "estimated_arival": bus.arival
                    }
                }

                json_body = [json_body, ]

                try:
                    client.write_points(json_body)
                except Exception as e:
                    print("There was an error writing to the database: {}".format(e))

    print("Files successfully written!")


if __name__ == '__main__':
    main()
