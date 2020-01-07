

class Bus:

    def __init__(self, bus_id, arival, line_description, line_number, timestamp):
        self.bus_id = bus_id
        self.line_description = line_description
        self.line_number = line_number
        self.arival = arival
        self.timestamp = timestamp

    # Not really needed.
    def to_json(self):
        return {'bus_id': self.bus_id,
                'line_description': self.line_description,
                'line_number': self.line_number,
                'arival': self.arival,
                'timestamp': timestamp}
