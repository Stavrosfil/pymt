import zlib
from ast import literal_eval as make_tuple

import requests
from pymongo import MongoClient

lines = {}
routes = {}
stops = {}
route_stops = {}

reqs = [
    ("https://oasth.gr/el/api/getUVersions/?a=1", 0),
    ("https://oasth.gr/el/api/getLines/?a=1", 1),
    ("https://oasth.gr/el/api/getRoutes/?a=1", 1),
    ("https://oasth.gr/el/api/getStopsB/?a=1", 1),
    ("https://oasth.gr/el/api/getRouteStops/?a=1", 1),
    ("https://oasth.gr/el/api/getMasterlines/?a=1", 1),
    ("https://oasth.gr/el/api/getMasterlinesDetails/?a=1", 1),
    ("https://oasth.gr/el/api/getSched_Cats/?a=1", 1),
    ("https://oasth.gr/el/api/getSched_line_cats/?a=1", 1),
    ("https://oasth.gr/el/api/getSched_series/?a=1", 1),
    ("https://oasth.gr/el/api/getSched_entries/?a=1", 1),
    ("https://oasth.gr/el/api/getRouteDetailPerRoute/2306/?a=1", 0),
    ("https://oasth.gr/el/api/getBusLocation/2306/?a=1", 0),
]


def decompress(response):
    decompressed_data = zlib.decompress(response, 16 + zlib.MAX_WBITS)
    return decompressed_data.decode("utf-8")


def req_all():
    for req in reqs:
        response = requests.get(req[0])
        # print(response.request.headers)

        if req[1] == 0:
            print(response.text)
        else:
            resp = decompress(response.content)
            tuples = make_tuple(resp)
            for t in tuples:
                print(t)

        input("Here is next")


# --------------------------------------------------------------------------------------

class Line:
    def __init__(self, args):
        self._id = args[0]
        self.name = args[1]
        self.desc_el = args[2]
        self.desc_en = args[3]
        self.days = args[4:]


def get_lines():
    response = decompress(requests.get(reqs[1][0]).content)
    tuples = make_tuple(response)

    for t in tuples:
        lines[t[0]] = Line(t)

    # for line in lines.values():
    #     print(line.__dict__)


# --------------------------------------------------------------------------------------

class Route:
    def __init__(self, args):
        self._id = args[0]
        self.line_index = args[1]
        self.dir1 = args[2]
        self.dir2 = args[3]
        self.dir = args[4]
        self.magic_float = args[5]


def get_routes():
    response = decompress(requests.get(reqs[2][0]).content)
    tuples = make_tuple(response)
    for t in tuples:
        routes[t[0]] = Route(t)
    # for route in routes.values():
    #     print(route.__dict__)


# --------------------------------------------------------------------------------------

class Stop:
    def __init__(self, args):
        self._id = args[0]
        self.uid = args[1]
        self.desc_el = args[2]
        self.desc_en = args[3]
        self.desc = args[4]  # , args[5]
        self.magic1 = args[6]
        # self.lon_lat = args[7], args[8]
        self.lon = args[7]
        self.lat = args[8]
        # self.magic2 = args[9], args[10]
        self.stop_routes_el = args[11]
        self.stop_routes_en = args[12]

        self.location = {
            "type": "Point",
            "coordinates": [
                self.lon,
                self.lat
            ]
        }


def get_stops():
    response = decompress(requests.get(reqs[3][0]).content)
    tuples = make_tuple(response)
    for t in tuples:
        stops[t[0]] = Stop(t)
        # print(stop.__dict__)


# --------------------------------------------------------------------------------------

class RouteStop:
    def __init__(self, args):
        self._id = args[0]
        self.route_id = args[1]
        self.stop_id = args[2]
        self.index = args[3]


def get_route_stops():
    response = decompress(requests.get(reqs[4][0]).content)
    tuples = make_tuple(response)
    for t in tuples:
        route_stops[t[0]] = RouteStop(t)
        # print(stop.__dict__)


# --------------------------------------------------------------------------------------

client = MongoClient('localhost', 27017)

db = client['pymt']

lines_db = db['lines']
routes_db = db['routes']
stops_db = db['stops']
route_stops_db = db['route_stops']


# req_all()

def to_mongo():
    client.drop_database("pymt")

    get_lines()
    get_routes()
    get_stops()
    get_route_stops()

    lines_db.insert_many([line.__dict__ for line in lines.values()])
    routes_db.insert_many([route.__dict__ for route in routes.values()])
    stops_db.insert_many([stop.__dict__ for stop in stops.values()])
    route_stops_db.insert_many([route_stop.__dict__ for route_stop in route_stops.values()])


# to_mongo()


# ----------------------------------------------------------------------------------


def organize():
    for index, line in lines.items():
        print(line.name + ': \t' + line.desc_en + '')
        print("\t", line.__dict__)

        for day in line.days:
            print(day, end=': \t')
            print("Null" if not routes.get(day) else routes.get(day).__dict__)
        # day = line.days[1]
        # print(day)
        # print("Null" if not routes.get(day) else routes.get(day).__dict__)
        print("-" * 150)
        pass

# organize()
