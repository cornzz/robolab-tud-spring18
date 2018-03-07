from events.EventRegistry import EventRegistry
from .Direction import Direction
from .Edge import Edge
from .Graph import Graph
from .Path import Path
from .Vertex import Vertex
from typing import Tuple


class Planet(Graph):
    def __init__(self, vertexes, edges):
        super().__init__(vertexes, edges)
        self.paths = []
        EventRegistry.instance().register_event_handler(self.new_path)
        pass

    def new_path(self, value):
        print(value)
        return self

    def combine_paths(self, start: Path, end: Path, length: float):
        edge = Edge(self.edges.__len__(), start.source, end.source, start.direction, end.direction, length)
        if edge not in self.edges:
            self.edges.append(edge)
            return edge
        else:
            return None

    def add_vertex(self, position: Tuple[int, int]):
        vertex = Vertex(self.vertexes.__len__(), position[0], position[1])
        if vertex not in self.vertexes:
            self.vertexes.append(vertex)
            return vertex
        else:
            return None

    def add_path(self, position: Vertex, direction: Direction):
        path = Path(self.paths.__len__(), position, direction)
        if path not in self.edges:
            self.paths.append(path)
            return path
        else:
            return None

    def get_shortest_path(self, start: Vertex, end: Vertex):
        # calculate shortest path
        pass
