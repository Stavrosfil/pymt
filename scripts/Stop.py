class Stop:

    def __init__(self, name='', buses=[], lines=[]):
        self.name = name
        self.buses = buses
        self.lines = lines

    def add_bus(self, bus):
        self.buses.append(bus)
