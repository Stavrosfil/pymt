import Stop as Stop
import requests
import json
sys.path.append('/home/stavrosfil/repos/pymt/scripts/modules')


of = open("oasth_stops.json", "a")

# http://m.oasth.gr/index.php?md=4&sn=3&start=819&sorder=1&rc=2282&line=620&dir=1&ref=1
url = "http://m.oasth.gr/index.php"
# reqdata = {"md": 4, "sn": 3, "start": 820,
#            "sorder": 1, "rc": 2282, "line": 620, "dir": 1}

stop_id = 1

session = requests.Session()

while True:

    reqdata = {"md": 4, "sn": 3, "start": stop_id}

    response = session.get(url, params=reqdata, headers={
                           "X-Requested-With": "XMLHttpRequest"})

    # print(soup.prettify())

    stop = Stop.Stop(payload=response.text, stop_id=stop_id)

    print(str(stop_id) + " \"" + stop.description + "\"")

    if(stop.description != ''):
        json.dump({'stop_id': stop_id, 'stop_description': stop.description},
                  of, indent=2, ensure_ascii=False)
        of.write(',\n')

    stop_id += 1

of.close()
