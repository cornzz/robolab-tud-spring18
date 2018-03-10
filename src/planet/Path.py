from .Direction import Direction
from .Vertex import Vertex


class Path:
    def __init__(self, _id, source: Vertex, direction: Direction):
        self.id = _id
        self.source = source
        self.direction = direction
        pass

    def __str__(self):
        return 'Path(' + str(self.source) + ',' + Direction.str(self.direction, True) + ')'
