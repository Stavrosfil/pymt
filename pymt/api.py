import requests


def get_stop_telematics(stop):
    response = requests.get("https://oasth.gr/el/api/getStopArrivals/{}/?a=1".format(stop._id)).json()
    return response


def get_line_telematics(line):
    response = requests.get("https://oasth.gr/el/api/getBusLocation/{}/?a=1".format(line.days[0])).json()
    return response
