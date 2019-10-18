import requests
from bs4 import BeautifulSoup
import time

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
    if(arivals):
        print(arivals)
    else:
        print('error')
    # print(soup.find_all('ul', attrs={'class': 'arivals'}))

    # busnames = []

    # for bus in arivals:
    #     bn = bus.find_all('span', attrs={'class': 'busno'})
    #     busnames.append(bn, string)
    counter += 1
    time.sleep(1)
    print(counter)

# print(busnames)

# print(response.text)
# print(response2.text)
