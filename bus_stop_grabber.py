import requests
import bs4

# This script grabs all bus lines from the arrivals page, finds
# the parameters (md, sn, start) passed on every one of them to link to the stops,
# and converts them into a dict containing the bus line name as key and the tuple
# of parameters as a value.

# Constants for grabbing
BASE_URL = "http://m.oasth.gr/index.php"
REQUEST_DATA = {"md": 4}  # 4th menu choice (line arrivals)
# OASTH site responds to XHR requests
HEADERS = {"X-Requested-With": "XMLHttpRequest"}

# Data request
session = requests.Session()
response = session.get(BASE_URL, params=REQUEST_DATA, headers=HEADERS)

# Parsing
soup = bs4.BeautifulSoup(response.text, 'html.parser')

# main_doc: the menu only, we don't care about any other links
main_doc = soup.find("div", {"class": "menu"})

# filter line names and corresponding links
# for line names: we want the content of all spans of sp1 class which are children of main_doc (i.e. exist in the menu)
# for line links: the href attribute of all anchors which are children of main_doc
line_names = [i.text for i in main_doc.findChildren('span', {"class": "sp1"})]
line_links = [j['href'] for j in main_doc.findChildren('a')]

for link in line_links:
    # initial form: http://m.oasth.gr/#index.php?md=4&sn=2&line=432&dhm=
    # first split on '?' gets rid of the URL before the parameters
    # second split breaks on '&'s to isolate the parameters
    # third split breaks on '=' to keep the numbers only, then the list
    # comprehension zips the numbers up into a new list and tosses out the
    # last element which is empty

    temp = [i.split('=')[1] for i in link.split('?')[1].split('&')][:-1]

    # convert the list of strings into a tuple of ints and replace the original link
    line_links[line_links.index(link)] = tuple(int(j) for j in temp)

# make a dict with keys the line names and values the parameters passed on their request
lines = dict(zip(line_names, line_links))
print(len(lines))
