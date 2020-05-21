from pymongo import MongoClient
from pymt import config
import pymt.models.oasth as model

c = config['mongodb']

client = MongoClient(c['uri'], c['port'])

db = client[c['db']]

lines_db = db[c['lines_db']]
routes_db = db[c['routes_db']]
stops_db = db[c['stops_db']]
route_stops_db = db[c['route_stops_db']]


# TODO: fix encoding in route names
def get_route_stops(name='31'):
    line = lines_db.find_one(dict(name=name))
    route = line.get('days')[0]
    # stops = route_stops_db.find(dict(route_id=route))
    stop_ids = [s.get('stop_id') for s in route_stops_db.find(dict(route_id=route))]
    stops = [model.Stop(stops_db.find_one(dict(_id=s))) for s in stop_ids]
    return stops


def get_line_by_name(name):
    line = model.Line(lines_db.find_one(dict(name=name)))
    return line


def get_all_lines():
    return [model.Line(l) for l in lines_db.find()]
