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
'''


def main():

    DATA_FOLDER = Path("data")

    stop_ids = []

    with open(DATA_FOLDER / "oasth_stops.json", "r") as f:

        for d in json.load(f):
            stop_ids.append(d["stop_id"])
            # print(f'Stop ID: { str(stop_id) }')

        f.close()

    client = InfluxDBClient('localhost', 8086)
    client.create_database('bustests')
    client.switch_database('bustests')
    # print(client.get_list_database())
    # while True:
    saveToInflux(client, stop_ids)


def saveToInflux(client, stop_ids):

    print("heu")

    # with open(DATA_FOLDER / "stop_info_async.json", "a") as of:

    stop_ids = stop_ids[0:50]

    responses = async_requests.get_stops(stop_ids)
    # of.write('[')

    for response, stop_id in zip(responses, stop_ids):

        stop = Stop.Stop(response, stop_id)

        if(stop is not None):
            # of.write('\n')
            for bus in stop.buses:

                # current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

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

                client.write_points(json_body)

                # stop_json = {'stop_id': stop.stop_id,
                #              'buses': [b.__dict__ for b in stop.buses]}

                # json.dump(stop_json, of, indent=2, ensure_ascii=False)
                # if (stop_id != stop_ids[-1]):
                # of.write(',')

    # of.close()


if __name__ == '__main__':
    main()
