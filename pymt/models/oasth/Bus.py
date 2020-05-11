import json
import time


class Bus:

    def __init__(self, payload=None, bus_dict=None):

        self.uuid = ""

        self.route_description = ""
        self.route_code = ""

        self.arrival = ""
        self.timestamp = ""

        if bus_dict is None:
            self.bus_dict = {}

        self.parse(payload)
        self.init_from_dict(bus_dict)

    def parse(self, payload):
        self.timestamp = time.time_ns()
        if payload:
            self.route_code = payload["route_code"]
            self.uuid = payload["veh_code"]
            self.arrival = int(payload["btime2"])

    def init_from_dict(self, user_dict):
        if user_dict is not None:
            _vars = vars(self)
            for var in _vars:
                parsed = user_dict.get(var)
                if parsed is not None and isinstance(_vars[var], type(parsed)):
                    _vars[var] = parsed
