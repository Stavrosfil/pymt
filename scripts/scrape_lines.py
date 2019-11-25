import requests
from bs4 import BeautifulSoup
import re
import Line as Line
import json

# --------------------------------- GET DATA --------------------------------- #

base_url = "http://m.oasth.gr/#index.php"
reqdata = {"md": 4}

session = requests.Session()

response = session.get(base_url, params=reqdata, headers={
    "X-Requested-With": "XMLHttpRequest"})

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
    parsed_lines.append(Line.Line(line=line, base_url=base_url))


# -------------------------- SAVE DATA TO JSON FILE -------------------------- #


def save_to_json():

    of = open("lines.json", "a")

    to_json = []

    for line in parsed_lines:
        p_line = {'line_id': line.line_id,
                  'line_number': line.line_number,
                  'line_description': line.line_description,
                  'generated_url': line.generated_url}
        to_json.append(p_line)

    json.dump(to_json, of, indent=2, ensure_ascii=False)

    of.close()


save_to_json()
