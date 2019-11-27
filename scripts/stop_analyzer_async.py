import requests
from bs4 import BeautifulSoup
import json
import re
import oasth_parsing as oasth_parser
import async_requests
# import time

of = open("stop_info_async.json", "a")

with open("oasth_stops.txt", "r") as f:

    stop_ids = []

    # TODO: Convert oasth_stops.txt file to a json one for better data handling.
    for line in f:
        stop_id = re.search(r'\d+', line).group()
        print(f'Stop ID: { str(stop_id) }')
        stop_ids.append(stop_id)

    responses = async_requests.get_stops(stop_ids)
    # print(responses)

    # ------------------------------ BEAUTIFUL SOUP ------------------------------ #

    soups = [BeautifulSoup(response, 'html5lib') for response in responses]
    # print(soup.prettify())

    # ---------------------------------- PARSING --------------------------------- #

    for soup in soups:

        if (soup.find('div', attrs={'class': 'err'}) is None):

            payload_arivals = soup.find('div', attrs={'class': 'menu'})

            parsed_buses = oasth_parser.parse_buses(payload_arivals)

            stop_json = {'stop_id': stop_id, 'buses': [
                i.__dict__ for i in parsed_buses]}
            json.dump(stop_json, of, indent=2, ensure_ascii=False)

            of.write(',\n')

            # print(json.dumps(oasth_parser.parse_buses(
            #     payload_arivals), ensure_ascii=False))


f.close()
