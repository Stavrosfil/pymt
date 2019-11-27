import requests
from bs4 import BeautifulSoup
import json
import re
import oasth_parsing as oasth_parser
import async_requests
import Stop
# import time

of = open("stop_info_async.json", "a")

with open("oasth_stops.txt", "r") as f:

    stop_ids = []

    # TODO: Convert oasth_stops.txt file to a json one for better data handling.
    for line in f:
        stop_id = re.search(r'\d+', line).group()
        # print(f'Stop ID: { str(stop_id) }')
        stop_ids.append(stop_id)

    responses = async_requests.get_stops(stop_ids)

    # ------------------------------ BEAUTIFUL SOUP ------------------------------ #

    stop_soups = [BeautifulSoup(response, 'html5lib')
                  for response in responses]

    # ---------------------------------- PARSING --------------------------------- #

    of.write('[')

    for stop_soup, stop_id in zip(stop_soups, stop_ids):

        stop = oasth_parser.parse_stop(stop_soup, stop_id)

        if(stop is not None):

            of.write('\n')

            stop_json = {'stop_id': stop.stop_id,
                         'buses': [b.__dict__ for b in stop.buses]}

            json.dump(stop_json, of, indent=2, ensure_ascii=False)

            if (stop_id != stop_ids[-1]):
                of.write(',')

f.close()
