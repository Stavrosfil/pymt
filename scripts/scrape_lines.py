import requests
from bs4 import BeautifulSoup
import re
from modules import Line as Line
import json
from pathlib import Path
import redis_save_stops

DATA_FOLDER = Path("data")

# --------------------------------- GET DATA --------------------------------- #

BASE_URL = "http://m.oasth.gr/#index.php"
PARAMS = {"md": 4}
HEADERS = {"X-Requested-With": "XMLHttpRequest"}

session = requests.Session()
response = session.get(BASE_URL, params=PARAMS, headers=HEADERS)
session.close()


# ------------------------------ BEAUTIFUL SOUP ------------------------------ #

soup = BeautifulSoup(response.text, 'html5lib')

# Menu div contains all the lines listed in the page.
soup = soup.find('div', attrs={'class': 'menu'})

# Get all the individual lines with their attributes
lines = soup.find_all('h3')


# ---------------------------------- PARSING --------------------------------- #

# Extract all the information from each individual line, using Line objects
parsed_lines = []
for line in lines:
    parsed_lines.append(Line.Line(html_payload=line))


# ---------------------------- SAVE DATA TO REDIS ---------------------------- #

def save_to_redis():
    redis_save_stops.save(lines=parsed_lines)


# -------------------------- SAVE DATA TO JSON FILE -------------------------- #


def save_to_json():

    with open(DATA_FOLDER / "lines.json", "a") as of:

        to_json = []

        for line in parsed_lines:
            p_line = {'line_id': line.line_id,
                      'line_number': line.line_number,
                      'line_description': line.line_description,
                      'generated_url': line.generated_url}
            to_json.append(p_line)

        json.dump(to_json, of, indent=2, ensure_ascii=False)

        of.close()


save_to_redis()
