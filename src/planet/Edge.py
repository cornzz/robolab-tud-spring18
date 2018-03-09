from .Direction import Direction
from .Vertex import Vertex


class Edge:
    def __init__(self, _id: int,
                 start: Vertex,
                 end: Vertex,
                 start_direction: Direction,
                 end_direction: Direction,
                 weight: float,
                 status: str):
        self.id = _id
        self.start = start
        self.end = end
        self.start_direction = start_direction
        self.end_direction = end_direction
        self.status = status
        self.weight = weight
        pass

    def set_weight(self, weight):
        self.weight = weight
        pass

    def tostring(self):
        return self.start.tostring() + ' ' + self.end.tostring()
