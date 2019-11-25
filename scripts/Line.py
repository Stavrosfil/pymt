import re
import bs4 as beautifulSoup


class Line:

    def __init__(self, line=None, base_url=None):
        self.line_id = 0
        self.href = ""
        self.sn = 0
        self.generated_url = ""
        self.line_number = ""

        if line is not None:
            self.parse_line(line)

        if base_url is not None:
            self.generate_url(base_url)

    def parse_line(self, line):
        """
        Parses the given soup object and extracts line details.

        Arguments:
            line {soup object} -- A soup object parsed from the website response containing the tag <h3>

        Example object:
            <h3>
                <a href = "http://m.oasth.gr/#index.php?md=4&amp;sn=2&amp;line=250&amp;dhm=">
                    <span class = "sp1">
                        92R
                    </span>
                    <span class = "sp2">
                        ΚΟΥΦΑΛΙΑ - ΡΑΧΩΝΑ
                    </span>
                </a>
            </h3>
        """

        self.href = line.find('a', href=True).get('href')
        self.line_id = int(re.search(r'line=\d+', self.href).group()[5:])
        self.sn = re.search(r'sn=\d+', self.href).group()[3:]
        self.line_number = line.find('span', attrs={'class': 'sp1'}).text
        self.line_description = line.find('span', attrs={'class': 'sp2'}).text

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
