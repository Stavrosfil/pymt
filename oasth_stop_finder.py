import requests
from bs4 import BeautifulSoup
# import time

f = open("oasth_stops.txt", "a")

# http://m.oasth.gr/index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1&ref=1
url = "http://m.oasth.gr/index.php"
# reqdata = {"md": 4, "sn": 3, "start": 820,
#            "sorder": 1, "rc": 2282, "line": 620, "dir": 1}

counter = 0

session = requests.Session()

while True:

    reqdata = {"md": 4, "sn": 3, "start": counter}

    response = session.get(url, params=reqdata, headers={
                           "X-Requested-With": "XMLHttpRequest"})

    soup = BeautifulSoup(response.text, 'html5lib')
    # print(soup.prettify())

    bus_stop = soup.find('div', attrs={'class': 'title'}).text
    print(str(counter) + " \"" + bus_stop + "\"")

    if(bus_stop != " "):
        f.write(str(counter) + " " + bus_stop + '\n')

    counter += 1
    # time.sleep(1)

f.close()
