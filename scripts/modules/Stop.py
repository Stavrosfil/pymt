import oasth_parsing as oasth_parser


class Stop:

    def __init__(self, payload=None, stop_id=-1, description='', buses=[], lines=[]):

        if payload is not None:
            """
            Initialize a stop object with a beautifulSoup html one.

            Arguments:
                stop_html {BeautifulSoup} -- [the payload received from the server]
            """

            stop = oasth_parser.parse_stop(self, payload, stop_id)

        else:
            self.stop_id = stop_id
            self.description = description
            self.buses = buses
            self.lines = lines

    def add_bus(self, bus):
        self.buses.append(bus)
