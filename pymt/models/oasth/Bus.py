import time


class Bus(object):
    def __init__(self, d):
        # self.__dict__ = d
        self.lon = float(d.get('CS_LNG'))
        self.lat = float(d.get('CS_LAT'))
        self.uuid = d.get('VEH_NO')
        self.route_code = d.get('ROUTE_CODE')
        self.timestamp = time.time_ns()
