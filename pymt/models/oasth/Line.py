class Line(object):
    def __init__(self, d):
        self.__dict__ = d
        self.stops = [None for _ in range(14)]
        self.days = d.get('days')

    def get_telematics_url(self, day=0):
        if self.days:
            if self.days[day] != 0:
                return "http://oasth.gr/el/api/getBusLocation/{}/?a=1".format(self.days[day])
        return None
