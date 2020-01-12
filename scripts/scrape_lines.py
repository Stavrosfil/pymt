import requests
from bs4 import BeautifulSoup
from modules import Line as Line
import redis_operations

"""
Retrieve all the available lines from OASTH and save them (prefferably to Redis).
"""


def scrape_lines():

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

    save_to_redis(parsed_lines)


# ---------------------------- SAVE DATA TO REDIS ---------------------------- #

def save_to_redis(lines):
    redis_operations.save(lines=lines)
