from pathlib import Path
import sys
import re
import json
import requests
import async_requests
from modules import Stop as Stop


DATA_FOLDER = Path("data")

stop_ids = []

with open(DATA_FOLDER / "oasth_stops.json", "r") as f:

    for d in json.load(f):
        stop_ids.append(d["stop_id"])
        # print(f'Stop ID: { str(stop_id) }')

    f.close()


with open(DATA_FOLDER / "stop_info_async.json", "a") as of:

    stop_ids = stop_ids[0:50]

    responses = async_requests.get_stops(stop_ids)
    of.write('[')

    for response, stop_id in zip(responses, stop_ids):

        stop = Stop.Stop(response, stop_id)

        if(stop is not None):
            of.write('\n')

            stop_json = {'stop_id': stop.stop_id,
                         'buses': [b.__dict__ for b in stop.buses]}

            json.dump(stop_json, of, indent=2, ensure_ascii=False)
            if (stop_id != stop_ids[-1]):
                of.write(',')

    of.close()
