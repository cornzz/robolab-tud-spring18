from src.shortest_path.Vertex import Vertex


class Path:
    def __init__(self, _id, source: Vertex, direction):
        self.id = _id
        self.source = source
        self.direction = direction
        pass
