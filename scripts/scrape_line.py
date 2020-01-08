import requests
from bs4 import BeautifulSoup
import re
from modules import Line as Line
from modules import Stop as Stop
import json
from pathlib import Path
import time
from urllib.parse import urlparse, parse_qs


DATA_FOLDER = Path("data")

"""

This script scrapes the stops and url parameters of a requested line id.
Input:  line_id (int)
Output: JSON object with all the info for the line stops

TODO: Convert the json object to sqlite output

Example json line object (to be depricated )
---------------------------------------------------------------------------
{
    "line_id": 146,
    "line_number": "01N",
    "line_description": "Κ.Τ.Ε.Λ. - ΑΕΡΟΔΡΟΜΙΟ ΝΥΧΤΕΡΙΝΟ",
    "generated_url": "http://m.oasth.gr/#index.php?md=4&sn=2&line=146&dhm="
}
---------------------------------------------------------------------------
"""

# --------------------------------- GET DATA --------------------------------- #

BASE_URL = "http://m.oasth.gr/index.php"
HEADERS = {"X-Requested-With": "XMLHttpRequest"}
PARAMS = {'md': 4, 'sn': 2, 'line': 146, 'dhm': '&', 'f': 1}
# generated_url = 'http://m.oasth.gr/#index.php?md=4&sn=2&line=146&dhm=&f=1'

session = requests.Session()
response = session.get(BASE_URL, params=PARAMS, headers=HEADERS).text
session.close()

# ------------------------------ BEAUTIFUL SOUP ------------------------------ #

soup = BeautifulSoup(response, 'html5lib')
print(soup.prettify())

# We get two menu divisions: start  -> dest
#                            dest   -> start
# This time the importand info is loaded with js, and is found under the 'menu' tag
# The only difference is that we discard the first menu division, because it belongs to the unloaded page.
line_directions = soup.find_all('div', attrs={'class': 'menu'})

parsed_stops = []

# Get all the individual stops for each direction.
for direction in line_directions:
    stops = direction.find_all('h3')
    for stop in stops:
        # !: We must remove '#' from the url or the urlparse lib will not work properly.
        href = stop.find('a', href=True).get('href').replace('#', '')
        index = stop.find('span', attrs={'class': 'sp2'}).text
        name = stop.find('span', attrs={'class': 'spt'}).text

        parsed_url = parse_qs(urlparse(str(href)).query)
        params = {}

        params['md'] = parsed_url['md'][0]
        params['sn'] = parsed_url['sn'][0]
        params['start'] = parsed_url['start'][0]
        params['sorder'] = parsed_url['sorder'][0]
        params['rc'] = parsed_url['rc'][0]
        params['line'] = parsed_url['line'][0]
        params['dir'] = parsed_url['dir'][0]

        print(params, name)
        parsed_stops.append(Stop.Stop(params=params, name=name))

# print(parsed_stops)

# -------------------------- SAVE DATA TO JSON FILE -------------------------- #


def save_to_json():

    with open(DATA_FOLDER / "test.json", "a") as of:

        to_json = []

        for stop in parsed_stops:

            p_line = {'stop_name': stop.name,
                      'params': stop.params, }
            to_json.append(p_line)

        json.dump(to_json, of, indent=2, ensure_ascii=False)

        of.close()


save_to_json()
