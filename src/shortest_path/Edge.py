class Edge:
    def __init__(self, _id, source, destination, start_direction, end_direction, weight):
        self.id = _id
        self.source = source
        self.destination = destination
        self.start_direction = start_direction
        self.end_direction = end_direction
        self.weight = weight
        pass

    def set_weight(self, weight):
        self.weight = weight
        pass

    def tostring(self):
        return self.source.tostring() + ' ' + self.destination.tostring()
