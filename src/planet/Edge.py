from .Direction import Direction
from .Vertex import Vertex


class Edge:
    def __init__(self, start: Vertex, end: Vertex, start_direction, end_direction, weight: float):
        self.id = ((start.position, start_direction), (end.position, end_direction))
        self.start = start
        self.end = end
        self.start_direction = start_direction
        self.end_direction = end_direction
        self.weight = weight
        pass

    def set_weight(self, weight):
        self.weight = weight
        pass

    def equals(self, edge):
        if self.id is edge.id \
                and self.start.equals(edge.start) \
                and self.end.equals(edge.end) \
                and self.start_direction == edge.start_direction \
                and self.end_direction == edge.end_direction:
            return True
        else:
            return False

    def __str__(self):
        return 'Edge(' + str(self.start) + '-' + str(self.end) + '|' + str(self.weight) + ')'
