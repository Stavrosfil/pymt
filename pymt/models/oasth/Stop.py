class Stop(object):
    def __init__(self, d):
        self.__dict__ = d
        self._id = d.get('_id')
        self.telematics_url = self.get_telematics_url()

    def get_telematics_url(self):
        if self._id:
            return "http://oasth.gr/el/api/getStopArrivals/{}/?a=1".format(self._id)
        else:
            return None
