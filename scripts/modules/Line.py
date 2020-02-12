import parser


class Line:

    # TODO: Check params initialization to a None type, maybe change back to dict. Also check initialization through the parser with self.
    def __init__(self, uid=None, name=None, number=None, html_payload=None, stops=None, params=None):
        self.uid = uid
        self.name = name
        self.number = number
        self.stops = stops
        self.params = params

        if html_payload is not None:
            parser.parse_line(self, payload=html_payload)
