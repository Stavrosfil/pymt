from Bus import Bus


def parse_buses(bus_arivals_html):
    """
    Parses a given OASTH based HTML string containing the incoming buses and timings.
    Returns: A list of bus objects.
    """

    buses_html = [b for b in bus_arivals_html.find_all('h3')]

    parsed_buses = [parse_bus(b) for b in buses_html]

    return parsed_buses


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
    Parses a given OASTH based HTML string containing the incoming bus info and timing.
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

    b = Bus(bus_id, arival, line_description, line_number)

    return b
