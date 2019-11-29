import re
import bs4 as beautifulSoup
import oasth_parsing as oasth_parser


class Line:

    def __init__(self, line=None, base_url=None, line_id=0, href="", sn=0, generated_url="", line_number=""):
        self.line_id = line_id
        self.href = href
        self.sn = sn
        self.generated_url = generated_url
        self.line_number = line_number

        if line is not None:
            oasth_parser.parse_line(self, line=line)

        if base_url is not None:
            self.generate_url(base_url)

    def generate_url(self, base_url):
        """
        Generates the url OASTH uses for the next page of requests.

        Arguments:
            base_url {String} -- The OASTH base string used to make all the requests.
        """
        if self.line_id == 0:
            print(
                "The object is not initialized correctly, try running parse_line() first!")
        args = '?md=4&sn=%s&line=%i&dhm=' % (self.sn, self.line_id)
        self.generated_url = base_url + args
