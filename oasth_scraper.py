import requests
from bs4 import BeautifulSoup
import time
import oasth_parsing as oasth_parser

# http://m.oasth.gr/index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1&ref=1
url = "http://m.oasth.gr/index.php"
reqdata = {"md": 4, "sn": 3, "start": 819,
           "sorder": 1, "rc": 2282, "line": 620, "dir": 1}

reqdata2 = {"md": 4, "sn": 3, "start": 922,
            "sorder": 18, "rc": 2279, "line": 146, "dir": 1}

session = requests.Session()

arivals = None
counter = 0

while True:
    response = session.get(url, params=reqdata, headers={
                           "X-Requested-With": "XMLHttpRequest"})
    # response2 = session.get(url, params=reqdata, headers={
    # "X-Requested-With": "XMLHttpRequest"})

    soup = BeautifulSoup(response.text, 'html5lib')
    # print(soup.prettify())

    arivals = soup.find('div', attrs={'class': 'menu'})
    print(arivals.prettify())

    dic = oasth_parser.parse_buses(arivals)

    for bus in dic:
        for bus_details in dic[bus]:
            print(bus + ' ' + bus_details[0] + ' ' + bus_details[1] + '\'')

    counter += 1
    time.sleep(1)
    print(counter)
