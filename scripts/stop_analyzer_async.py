from pathlib import Path
import sys
import re
import json
import requests
import async_requests
import Stop as Stop
sys.path.append('/home/stavrosfil/repos/pymt/scripts/modules')

# import time


data_folder = Path("data")

od = data_folder / "stop_info_async.json"

of = open(od, "a")

# of = open("/data/stop_info_async.json", "a")

with open('oasth_stops.json') as f:

    stop_ids = []

    data = json.load(f)

    # TODO: Convert oasth_stops.txt file to a json one for better data handling.
    for d in data:
        # print(f'Stop ID: { str(stop_id) }')
        stop_ids.append(d["stop_id"])

    # stop_ids = stop_ids[0:50]

    responses = async_requests.get_stops(stop_ids)

    # ---------------------------------- PARSING --------------------------------- #

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

f.close()
of.close()
