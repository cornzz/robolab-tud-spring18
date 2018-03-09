from .Direction import Direction
from .Vertex import Vertex


class Path:
    def __init__(self, _id, source: Vertex, direction: Direction):
        self.id = _id
        self.source = source
        self.direction = direction
        pass

    def __str__(self):
        return str(self.source.x) + ',' + str(self.source.y) + ',' + Direction.str(self.direction, True)
