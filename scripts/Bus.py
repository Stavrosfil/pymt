

class Bus:

    bus_id = 0
    line_description = ''
    line_number = ''
    arival = 0

    def __init__(self, bus_id, arival, line_description, line_number):
        self.bus_id = bus_id
        self.line_description = line_description
        self.line_number = line_number
        self.arival = arival
