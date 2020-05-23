from pymongo import MongoClient

import pymt.helpers.metadata
from pymt import config, selected_lines, default_logger, logger
import pymt.models.oasth as model

c = config['mongodb']

client = MongoClient(c['uri'])

db = client[c['db']]

lines_db = db[c['lines_db']]
routes_db = db[c['routes_db']]
stops_db = db[c['stops_db']]
route_stops_db = db[c['route_stops_db']]


# TODO: fix encoding in route names
def get_route_stops(route_id):
    # line = lines_db.find_one(dict(name=name))
    # route = line.get('days')[0]
    # stops = route_stops_db.find(dict(route_id=route))
    stop_ids = [s.get('stop_id') for s in route_stops_db.find(dict(route_id=route_id))]
    stops = [model.Stop(stops_db.find_one(dict(_id=s))) for s in stop_ids]
    return stops


def get_line_by_name(name):
    line = model.Line(lines_db.find_one(dict(name=name)))
    return line


def get_all_lines():
    return [model.Line(l) for l in lines_db.find()]


@pymt.helpers.metadata.timer("Loading selected lines from MongoDB")
def load_lines(days, lines=selected_lines):
    _lines = []
    if not lines:
        _lines = get_all_lines()
    else:
        _lines = [get_line_by_name(line_name) for line_name in lines]
    [logger.debug(f"Selected lines: {l.__dict__}") for l in _lines]
    for d in days:
        for line in _lines:
            line.stops[d] = get_route_stops(route_id=line.days[d])
    return _lines
