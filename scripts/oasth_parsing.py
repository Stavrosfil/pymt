from Bus import Bus
import Stop as Stop
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------- #
#                                 STOP PARSING                                 #
# ---------------------------------------------------------------------------- #

def parse_stop(payload, stop_id):

    soup = BeautifulSoup(payload, 'html5lib')

    description = soup.find('div', attrs={'class': 'title'}).text

    if (soup.find('div', attrs={'class': 'err'}) is None):
        payload_arivals = soup.find('div', attrs={'class': 'menu'})
        parsed_buses = parse_buses(payload_arivals)
        return Stop.Stop(stop_id=stop_id, buses=parsed_buses, description=description)
    else:
        # We got no buses in this stop
        return Stop.Stop(stop_id=stop_id)


# ---------------------------------------------------------------------------- #
#                                  BUS PARSING                                 #
# ---------------------------------------------------------------------------- #

# TODO: use bs4 for every parsing inside the file
def parse_buses(bus_arivals_html):
    """
    Parses a given OASTH based HTML string containing the incoming buses and timings from a specific Stop.
    Returns: A list of bus objects.
    """

    buses_html = [b for b in bus_arivals_html.find_all('h3')]

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
    # arival = re.search(r'\d+', bus_time).group()
    arival = int(bus_html.find('span', attrs={'class': 'sptime'}).text[1:-2])

    # Split in : and get the bus number (01X).
    # 01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
    line_number, line_description = bus_payload.split(':')

    # Get the second split item and extract the bus description
    # "Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ "
    # Then delete the trailing space
    # Get the second split item and extract the bus id (0861)
    line_description, bus_id = line_description.split(' ΟΧΗΜΑ ')

    bus_id = int(bus_id)

    return Bus(bus_id, arival, line_description, line_number)
