import requests
from bs4 import BeautifulSoup
import json
import re
import oasth_parsing as oasth_parser
# import time

of = open("stop_info.txt", "a")

# http://m.oasth.gr/index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1&ref=1
url = "http://m.oasth.gr/index.php"
# reqdata = {"md": 4, "sn": 3, "start": 820,
#            "sorder": 1, "rc": 2282, "line": 620, "dir": 1}

session = requests.Session()

with open("oasth_stops.txt", "r") as f:
    for line in f:

        stop_id = re.search(r'\d+', line).group()

        print(f'Stop ID: { str(stop_id) }')

        reqdata = {"md": 4, "sn": 3, "start": stop_id}

        response = session.get(url, params=reqdata, headers={
                               "X-Requested-With": "XMLHttpRequest"})

        soup = BeautifulSoup(response.text, 'html5lib')
        # print(soup.prettify())
        payload_arivals = soup.find('div', attrs={'class': 'menu'})

        if (soup.find('div', attrs={'class': 'err'}) is None):
            to_dump = {stop_id: oasth_parser.parse_buses(payload_arivals)}
            json.dump(to_dump, of, indent=2, ensure_ascii=False)
            of.write('\n')

        print(json.dumps(oasth_parser.parse_buses(
            payload_arivals), ensure_ascii=False))

        # if (soup.find('div', attrs={'class': 'err'}) is None):
        #     dic = oasth_parser.parse_buses(payload_arivals)
        #     for bus in dic:
        #         for bus_details in dic[bus]:
        #             print(bus + ' ' + bus_details[0] +
        #                   ' ' + bus_details[1] + '\'')
        # else:
        #     print("No buses")

        # bus_stop = soup.find('div', attrs={'class': 'title'}).text
        # print(str(stop_id) + " \"" + bus_stop + "\"")

        # if(bus_stop != " "):
        #     f.write(str(stop_id) + " " + bus_stop + '\n')

        # time.sleep(1)

f.close()
