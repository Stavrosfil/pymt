import oasth_parsing as oasth_parser


class Stop:

    def __init__(self, payload=None, url=None, uid=None, name='', buses=[], lines=[], params={}):
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

        if payload is not None:

            stop = oasth_parser.parse_stop(self, payload, uid)

        else:
            self.params = params
            self.url = url
            self.uid = uid
            self.name = name
            self.buses = buses
            self.lines = lines

    def add_bus(self, bus):
        self.buses.append(bus)
