import requests
from bs4 import BeautifulSoup
import re
import Line as Line

# --------------------------------- GET DATA --------------------------------- #

base_url = "http://m.oasth.gr/index.php"
reqdata = {"md": 4}

session = requests.Session()

response = session.get(base_url, params=reqdata, headers={
    "X-Requested-With": "XMLHttpRequest"})


# ------------------------------ BEAUTIFUL SOUP ------------------------------ #

soup = BeautifulSoup(response.text, 'html5lib')

# Menu div contains all the lines listed in the page.
soup = soup.find('div', attrs={'class': 'menu'})

# Get all the individual lines with their attributes
lines = soup.find_all('h3')


# ---------------------------------- PARSING --------------------------------- #

parsed_lines = []

# Extract all the information from each individual line, using Line objects
for line in lines:

    parsed_lines.append(Line.Line(line=line, base_url=base_url))


for i in parsed_lines:
    print(i.line_id)

session.close()
