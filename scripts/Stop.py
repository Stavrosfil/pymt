class Stop:

    def __init__(self, stop_id=-1, description='', buses=[], lines=[]):
        self.stop_id = stop_id
        self.description = description
        self.buses = buses
        self.lines = lines

    def add_bus(self, bus):
        self.buses.append(bus)
