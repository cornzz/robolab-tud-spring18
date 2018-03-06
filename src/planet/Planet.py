from src.shortest_path import Graph, Edge, Vertex, Path
from enum import unique, IntEnum
from typing import Tuple


@unique
class Direction(IntEnum):
    """ Directions in degrees """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


class Planet(Graph):
    def __init__(self, vertexes, edges):
        super().__init__(vertexes, edges)
        self.paths = []
        pass

    def combine_paths(self, start: Path, end: Path, length: float):
        edge = Edge.Edge(self.edges.__len__(), start.source, end.source, start.direction, end.direction, length)
        if edge not in self.edges:
            self.edges.append(edge)
            return edge
        else:
            return None

    def add_vertex(self, position: Tuple[int, int]):
        vertex = Vertex.Vertex(self.vertexes.__len__(), position[0], position[1])
        if vertex not in self.vertexes:
            self.vertexes.append(vertex)
            return vertex
        else:
            return None

    def add_path(self, position: Vertex.Vertex, direction):
        path = Path.Path(self.paths.__len__(), position, direction)
        if path not in self.edges:
            self.paths.append(path)
            return path
        else:
            return None

    def get_shortest_path(self, start: Vertex.Vertex, destination: Vertex.Vertex):
        # calculate shortest path
        pass
