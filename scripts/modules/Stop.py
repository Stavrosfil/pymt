import oasth_parsing as oasth_parser


class Stop:

    def __init__(self, payload=None, url=None, stop_id=-1, name='', buses=[], lines=[], params={}):

        if payload is not None:
            """
            Initialize a stop object with a beautifulSoup html one, using the telematics data received.

            Arguments:
                payload {BeautifulSoup} -- [the payload received from the xhr request]
            """

            stop = oasth_parser.parse_stop(self, payload, stop_id)

        else:
            self.params = params
            self.url = url
            self.stop_id = stop_id
            self.name = name
            self.buses = buses
            self.lines = lines

    def add_bus(self, bus):
        self.buses.append(bus)
