from .Edge import Edge
from .Vertex import Vertex
from typing import List


class Graph:
    def __init__(self, vertexes: List[Vertex], edges: List[Edge]):
        self.vertexes = vertexes or []
        self.edges = edges or []
    pass

    def with_edges(self, edges: List[Edge]):
        self.edges = edges
        return self
