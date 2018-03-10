from .Edge import Edge
from .Vertex import Vertex
from typing import Dict, Tuple


class Graph:
    def __init__(self,
                 vertexes: Dict[Tuple[int, int], Vertex],
                 edges: Dict[Tuple[Tuple[int, int], Tuple[int, int]], Edge]):
        self.vertexes = vertexes or {}
        self.edges = edges or {}
    pass

    def with_edges(self, edges: Dict[str, Edge]):
        self.edges = edges
        return self
