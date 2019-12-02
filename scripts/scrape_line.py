import requests
from bs4 import BeautifulSoup
import re
from modules import Line as Line
from modules import Stop as Stop
import json
from pathlib import Path
from selenium import webdriver
import selenium as se
import time
from urllib.parse import urlparse, parse_qs


DATA_FOLDER = Path("data")

"""
Example json line object
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

# BASE_URL = "http://m.oasth.gr/#index.php"
# PARAMS = {"md": 4}
HEADERS = {"X-Requested-With": "XMLHttpRequest"}
generated_url = 'http://m.oasth.gr/#index.php?md=4&sn=2&line=146&dhm=&f=1'


options = se.webdriver.ChromeOptions()
options.add_argument('headless')
driver = se.webdriver.Chrome(options=options)
driver.get(generated_url)
time.sleep(0.5)
response = driver.page_source
driver.close()


# ------------------------------ BEAUTIFUL SOUP ------------------------------ #

soup = BeautifulSoup(response, 'html5lib')
# print(soup.prettify())

# We get two menu divisions: start  -> dest
#                            dest   -> start
# This time the importand info is loaded with js, and is found under the 'menu' tag
# The only difference is that we discard the first menu division, because it belongs to the unloaded page.
line_directions = soup.find_all('div', attrs={'class': 'menu'})[1:]

parsed_stops = []

# Get all the individual stops for each direction.
for direction in line_directions:
    stops = direction.find_all('h3')
    for stop in stops:
        # !: We must remove '#' from the url or the urlparse lib will not work properly.
        href = stop.find('a', href=True).get('href').replace('#', '')
        index = stop.find('span', attrs={'class': 'sp2'}).text
        name = stop.find('span', attrs={'class': 'spt'}).text

        print(href, index, name)
        parsed_stops.append(Stop.Stop(url=href, name=name))

# print(parsed_stops)

# -------------------------- SAVE DATA TO JSON FILE -------------------------- #


def save_to_json():

    with open(DATA_FOLDER / "test.json", "a") as of:

        to_json = []

        for stop in parsed_stops:

            parsed_url = urlparse(str(href))
            stop_id = parse_qs(parsed_url.query)['start'][0]
            index = parse_qs(parsed_url.query)['sorder'][0]
            direction = parse_qs(parsed_url.query)['dir'][0]

            p_line = {'stop_id': stop_id,
                      'index': index,
                      'dir': direction,
                      'stop_url': stop.url,
                      'stop_name': stop.name, }
            to_json.append(p_line)

        json.dump(to_json, of, indent=2, ensure_ascii=False)

        of.close()


save_to_json()
