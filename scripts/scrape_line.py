import requests
from bs4 import BeautifulSoup
import re
from modules import Line as Line
import json
from pathlib import Path
from selenium import webdriver
import selenium as se
import time


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
print(driver.page_source)


# print(response.html.html)
# ------------------------------ BEAUTIFUL SOUP ------------------------------ #

# soup = BeautifulSoup(response.html.html, 'html5lib')
# # print(soup.prettify())

# # We get two menu divisions: start  -> dest
# #                            dest   -> start
# line_directions = soup.find_all('div', attrs={'class': 'menu'})

# d1, d2 = [], []

# # Get all the individual stops for each direction.
# for direction in line_directions:
#     stops = direction.find_all('h3')
#     for stop in stops:
#         href = stop.find('a', href=True).get('href')
#         index = stop.find('span', attrs={'class': 'sp2'})
#         title = stop.find('span', attrs={'class': 'spt'})
#         print(href, index, title)


# -------------------------- SAVE DATA TO JSON FILE -------------------------- #


# def save_to_json():

#     with open(DATA_FOLDER / "lines.json", "a") as of:

#         to_json = []

#         for line in parsed_lines:
#             p_line = {'line_id': line.line_id,
#                       'line_number': line.line_number,
#                       'line_description': line.line_description,
#                       'generated_url': line.generated_url}
#             to_json.append(p_line)

#         json.dump(to_json, of, indent=2, ensure_ascii=False)

#         of.close()


# save_to_json()
