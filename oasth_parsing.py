import re

# Example of a bus details payload we receive in HTML.
# ------------------------------------------------
#   <h3>
#       <span class="sp1">
#           01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
#       </span>
#       <span class="sp2">
#           ΑΦΙΞΗ ΣΕ
#           <span class="sptime">
#               52'
#           </span>
#       </span>
#  </h3>
# ------------------------------------------------


def parse_buses(payload_arivals):

    bus_descriptions = [bus.text for bus in payload_arivals.find_all(
        'span', attrs={'class': 'sp1'})]
    bus_times = [arival.text for arival in payload_arivals.find_all(
        'span', attrs={'class': 'sptime'})]

    dic = dict([])

    for bus_description, bus_time in zip(bus_descriptions, bus_times):

        # Split in : and get the bus number (01X).
        # 01X:Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ ΟΧΗΜΑ 0861
        bus_number, bus_name = bus_description.split(':')

        # Get the second split item and extract the bus description
        # "Κ.Τ.Ε.Λ.-ΑΕΡΟΔΡΟΜΙΟ "
        # Then delete the trailing space
        # Get the second split item and extract the bus id (0861)
        bus_name, bus_id = bus_name.split(' ΟΧΗΜΑ ')

        # Delete all the spaces
        bus_arival = re.search(r'\d+', bus_time).group()

        dic_key = bus_number + ':' + bus_name

        if dic_key in dic:
            dic[dic_key].append((bus_id, bus_arival))
        else:
            dic[dic_key] = [(bus_id, bus_arival)]

    return dic
