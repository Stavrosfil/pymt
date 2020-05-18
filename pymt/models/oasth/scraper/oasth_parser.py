from pymt.models.oasth import Bus as Bus
from pymt.models.oasth import Stop as Stop
from bs4 import BeautifulSoup
import re
import time


# ---------------------------------------------------------------------------- #
#                                 STOP PARSING                                 #
# ---------------------------------------------------------------------------- #

def parse_stop_buses(payload):
    soup = BeautifulSoup(payload, 'html5lib')
    buses = []

    # If we got buses in this stop
    if soup.find('div', attrs={'class': 'err'}) is None:
        payload_arrivals = soup.find('div', attrs={'class': 'menu'})
        parsed_buses = parse_buses(payload_arrivals)
        buses = parsed_buses

    return buses


def parse_stop(self, payload, uid):
    soup = BeautifulSoup(payload, 'html5lib')

    name = soup.find('div', attrs={'class': 'title'}).text[:-1]

    self.buses = []

    # If we got buses in this stop
    if soup.find('div', attrs={'class': 'err'}) is None:
        payload_arrivals = soup.find('div', attrs={'class': 'menu'})
        parsed_buses = parse_buses(payload_arrivals)
        self.buses = parsed_buses

    self.uid = uid
    self.name = name


# ---------------------------------------------------------------------------- #
#                                  BUS PARSING                                 #
# ---------------------------------------------------------------------------- #

# TODO: use bs4 for every parsing inside the file


def parse_buses(bus_arrivals_html):
    """
    Parses a given OASTH based HTML string containing the incoming buses and timings from a specific Stop.
    Returns: A list of bus objects.
    """

    buses_html = [b for b in bus_arrivals_html.find_all('h3')]

    return [parse_bus(b) for b in buses_html]


"""
Example of a bus details payload we receive in HTML:
----------------------------------------------------
  <h3>
      <span class="sp1">
          01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
      </span>
      <span class="sp2">
          ΑΦΙΞΗ ΣΕ
          <span class="sptime">
              52'
          </span>
      </span>
 </h3>
-----------------------------------------------------
"""


def parse_bus(bus_html):
    """
    Parses a given OASTH based HTML string containing the incoming bus info and timing from a specific Stop.
    Returns: A bus object.
    """

    # extract text from:
    # <span class="sp1">
    #    01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
    # </span>
    bus_payload = bus_html.find('span', attrs={'class': 'sp1'}).text

    # extract timing from:
    # <span class="sptime">
    #    52'
    # </span>
    # Delete all the spaces trimming the first and two last characters. ' 5' '
    # arrival = re.search(r'\d+', bus_time).group()
    arrival = int(bus_html.find('span', attrs={'class': 'sptime'}).text[1:-2])

    # Split in : and get the bus number (01X).
    # 01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
    line_number, line_description = bus_payload.split(':')

    # Get the second split item and extract the bus description
    # "Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ "
    # Then delete the trailing space
    # Get the second split item and extract the bus id (0861)
    line_description, bus_id = line_description.split(' ΟΧΗΜΑ ')

    bus_id = int(bus_id)

    # Use the current time to correctly input the bus to the database
    timestamp = time.time_ns()

    return Bus.Bus(bus_id, arrival, line_description, line_number, timestamp)


# ---------------------------------------------------------------------------- #
#                                 LINE PARSING                                 #
# ---------------------------------------------------------------------------- #

def parse_line_stops(payload):
    soup = BeautifulSoup(payload, 'html5lib')
    # print(soup.prettify())

    # We get two menu divisions: start  -> dest
    #                            dest   -> start
    # This time the importand info is loaded with js, and is found under the 'menu' tag
    # The only difference is that we discard the first menu division, because it belongs to the unloaded page.
    line_directions = soup.find_all('div', attrs={'class': 'menu'})[1:]

    parsed_stops = []

    # Get all the individual stops for each direction.
    for direction in line_directions:
        stops = direction.find_all('h3')
        for stop in stops:
            # !: We must remove '#' from the url or the urlparse lib will not work properly.
            href = stop.find('a', href=True).get('href').replace('#', '')
            index = stop.find('span', attrs={'class': 'sp2'}).text
            name = stop.find('span', attrs={'class': 'spt'}).text

            print(href, index, name)
            parsed_stops.append(Stop.Stop(url=href, name=name))

    return parsed_stops


def parse_line(self, payload):
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

    self.href = payload.find('a', href=True).get('href')
    self.uid = int(re.search(r'line=\d+', self.href).group()[5:])
    self.params = {}
    self.params['sn'] = re.search(r'sn=\d+', self.href).group()[3:]
    self.params['md'] = re.search(r'md=\d+', self.href).group()[3:]
    self.params['line'] = re.search(r'line=\d+', self.href).group()[5:]
    self.number = payload.find('span', attrs={'class': 'sp1'}).text
    self.name = payload.find('span', attrs={'class': 'sp2'}).text
