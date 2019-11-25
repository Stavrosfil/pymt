import requests
from bs4 import BeautifulSoup
import json
import re
import oasth_parsing as oasth_parser
# import time

of = open("stop_info.json", "a")

# http://m.oasth.gr/index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1&ref=1
url = "http://m.oasth.gr/index.php"
# reqdata = {"md": 4, "sn": 3, "start": 820,
#            "sorder": 1, "rc": 2282, "line": 620, "dir": 1}

session = requests.Session()

with open("oasth_stops.txt", "r") as f:

    # TODO: Convert oasth_stops.txt file to a json one for better data handling.
    for line in f:

        stop_id = re.search(r'\d+', line).group()

        print(f'Stop ID: { str(stop_id) }')

        reqdata = {"md": 4, "sn": 3, "start": stop_id}

        response = session.get(url, params=reqdata, headers={
                               "X-Requested-With": "XMLHttpRequest"})

        soup = BeautifulSoup(response.text, 'html5lib')
        # print(soup.prettify())

        if (soup.find('div', attrs={'class': 'err'}) is None):

            payload_arivals = soup.find('div', attrs={'class': 'menu'})

            parsed_buses = oasth_parser.parse_buses(payload_arivals)

            stop_json = {'stop_id': stop_id, 'buses': [
                i.__dict__ for i in parsed_buses]}
            json.dump(stop_json, of, indent=2, ensure_ascii=False)

            of.write('\n')

            # print(json.dumps(oasth_parser.parse_buses(
            #     payload_arivals), ensure_ascii=False))


f.close()
