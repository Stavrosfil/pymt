import requests
from bs4 import BeautifulSoup
import time


# http://m.oasth.gr/index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1&ref=1
url = "http://m.oasth.gr/index.php"
# reqdata = {"md": 4, "sn": 3, "start": 820,
#            "sorder": 1, "rc": 2282, "line": 620, "dir": 1}

arivals = None
counter = 819

session = requests.Session()

while True:

    reqdata = {"md": 4, "sn": 3, "start": counter}

    response = session.get(url, params=reqdata, headers={
                           "X-Requested-With": "XMLHttpRequest"})

    soup = BeautifulSoup(response.text, 'html5lib')
    # print(soup.prettify())

    bus_stop = soup.find('div', attrs={'class': 'title'}).text
    print(bus_stop)

    counter += 1
    # time.sleep(1)
