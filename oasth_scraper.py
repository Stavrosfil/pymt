import requests
from bs4 import BeautifulSoup
import time
import re

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

    arivals = soup.find_all('div', attrs={'class': 'menu'})
    print(arivals[0].prettify())
    bus_names = arivals[0].find_all('span', attrs={'class': 'sp1'})
    bus_time = arivals[0].find_all('span', attrs={'class': 'sptime'})

    dic = dict([])

    for i in range(len(bus_names)):
        bus_number = bus_names[i].text.split(':')[0]
        bus_name = bus_names[i].text.split(':')[1].split('ΟΧΗΜΑ')[0][:-1]
        bus_id = bus_names[i].text.split(':')[1].split('ΟΧΗΜΑ')[1]
        bus_id = re.search(r'\d+', bus_id).group()
        bus_arival = re.search(r'\d+', bus_time[i].text).group()

        dic_key = bus_number + ':' + bus_name

        if dic_key in dic:
            dic[dic_key].append(bus_arival)
        else:
            dic[dic_key] = [bus_arival]

    for bus in dic:
        for arival_time in dic[bus]:
            print(bus + ' ' + bus_id + ' ' + arival_time + '\'')

    counter += 1
    time.sleep(1)
    print(counter)
