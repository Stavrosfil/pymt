class Line(object):
    def __init__(self, d):
        self.__dict__ = d
        self.stops = []
        self.days = d.get('days')

    def get_telematics_url(self, day=0):
        if self.days:
            return "http://oasth.gr/el/api/getBusLocation/{}/?a=1".format(self.days[day])
        else:
            return None
