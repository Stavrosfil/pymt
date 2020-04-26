

class Bus:

    def __init__(self, bus_uuid, arrival, line_description, line_number, timestamp):
        self.bus_uuid = bus_uuid
        self.line_description = line_description
        self.line_number = line_number
        self.arrival = arrival
        self.timestamp = timestamp

    # Not really needed.
    def to_json(self):
        return {'bus_id': self.bus_uuid,
                'line_description': self.line_description,
                'line_number': self.line_number,
                'arrival': self.arrival,
                'timestamp': self.timestamp}
