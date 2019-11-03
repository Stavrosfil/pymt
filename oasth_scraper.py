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

    # Example of a bus details payload we receive in HTML.
    # ------------------------------------------------
    #   <h3>
    #       <span class="sp1">
    #           01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
    #       </span>
    #       <span class="sp2">
    #           ΑΦΙΞΗ ΣΕ
    #           <span class="sptime">
    #               52'
    #           </span>
    #       </span>
    #  </h3>
    # ------------------------------------------------

    arivals = soup.find('div', attrs={'class': 'menu'})
    print(arivals.prettify())
    bus_names = [bus.text for bus in arivals.find_all(
        'span', attrs={'class': 'sp1'})]
    bus_times = [arival.text for arival in arivals.find_all(
        'span', attrs={'class': 'sptime'})]

    dic = dict([])

    for bus_description, bus_time in zip(bus_names, bus_times):

        # Split in : and get the bus number (01X).
        # 01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
        bus_number, bus_name = bus_description.split(':')

        # Get the second split item and extract the bus description
        # "Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ "
        # Then delete the trailing space
        # Get the second split item and extract the bus id (0861)
        bus_name, bus_id = bus_name.split(' ΟΧΗΜΑ ')

        # Delete all the spaces
        bus_arival = re.search(r'\d+', bus_time).group()

        dic_key = bus_number + ':' + bus_name

        if dic_key in dic:
            dic[dic_key].append((bus_id, bus_arival))
        else:
            dic[dic_key] = [(bus_id, bus_arival)]

    for bus in dic:
        for bus_details in dic[bus]:
            print(bus + ' ' + bus_details[0] + ' ' + bus_details[1] + '\'')

    counter += 1
    time.sleep(1)
    print(counter)
