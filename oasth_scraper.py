import requests
from bs4 import BeautifulSoup
import time
import oasth_parsing as oasth_parser
from Stop import Stop

# http://m.oasth.gr/index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1&ref=1
url = "http://m.oasth.gr/index.php"

reqdata = {"md": 4, "sn": 3, "start": 820,
           "sorder": 1, "rc": 2282, "line": 620, "dir": 1}

reqdata2 = {"md": 4, "sn": 3, "start": 819}

arivals = None
counter = 0

session = requests.Session()

while True:

    response = session.get(url, params=reqdata, headers={
                           "X-Requested-With": "XMLHttpRequest"})
    response = session.get(url, params=reqdata2, headers={
                           "X-Requested-With": "XMLHttpRequest"})

    soup = BeautifulSoup(response.text, 'html5lib')
    print(soup.prettify())

    bus_stop = Stop(name=soup.find('div', attrs={'class': 'title'}).text)

    print(bus_stop.name)

    bus_arivals_html = soup.find('div', attrs={'class': 'menu'})
    # print(payload_arivals.prettify())

    if (soup.find('div', attrs={'class': 'err'}) is None):
        parsed_buses = oasth_parser.parse_buses(bus_arivals_html)
        for bus in parsed_buses:
            print(bus.line_number)
        # for bus in dic:
        #     for bus_details in dic[bus]:
        #         print(bus + ' ' + bus_details[0] + ' ' + bus_details[1] + '\'')
    else:
        print("No buses")

    counter += 1
    time.sleep(1)
    print(counter)

session.close()
