from pymt.models.oasth.Bus import Bus
import json


class Stop:

    def __init__(self, payload=None, url=None, uid=None, name='', buses=None, lines=None, params=None):
        """Initialize a stop object with a beautifulSoup html one, using the telematics data received or manually.

        Keyword Arguments:
            payload {BeautifulSoup} -- [the payload received from the xhr request] (default: {None})
            url {string} -- [The url to use when scraping] (default: {None})
            uid {int} -- [The unique ID of the stop. (The same as the 'start' param)] (default: {None})
            name {string} -- [The name of the stop] (default: {''})
            buses {Bus list} -- [List of incoming buses to the stop] (default: {[]})
            lines {Line list} -- [List of lines the stop supports] (default: {[]})
            params {dict} -- [The stop parameters used in the URL] (default: {{}})
        """

        # params['md']
        # params['sn']
        # params['start']
        # params['sorder']
        # params['rc']
        # params['line']
        # params['dir']

        if params is None:
            params = {}
        if lines is None:
            lines = []
        if buses is None:
            buses = []
        if payload is not None:
            self.parse_stop(payload)

        else:
            self.params = params
            self.url = url
            self.uid = uid
            self.name = name
            self.buses = buses
            self.lines = lines

    def add_bus(self, bus):
        self.buses.append(bus)

    def parse_stop(self, payload):
        self.buses = []
        if payload:
            for bus in payload:
                self.buses.append(Bus(bus))

        #
        # pass
        # self.buses = oasth_parser.parse_stop_buses(payload)
