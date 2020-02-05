import re
import bs4 as beautifulSoup
import parser


class Line:

    # TODO: Check params initialization to a None type, maybe change back to dict. Also check initialization through the parser with self.
    def __init__(self, uid=None, name=None, number=None, html_payload=None, base_url=None, stops=None, params=None):
        self.uid = uid
        self.name = name
        self.number = number
        self.stops = stops
        self.params = params

        if html_payload is not None:
            parser.parse_line(self, payload=html_payload)

        if base_url is not None:
            self.generate_url(base_url)

    def generate_url(self, base_url):
        """
        Generates the url OASTH uses for the next page of requests.

        Arguments:
            base_url {String} -- The OASTH base string used to make all the requests.
        """

        args = '?md=4&sn={}&line={}&dhm='.format(self.sn, self.line_id)
        self.generated_url = base_url + args
        return self.generated_url
