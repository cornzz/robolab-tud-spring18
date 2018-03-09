from events.EventRegistry import EventRegistry
from events.EventNames import EventNames
from .Direction import Direction
from .Edge import Edge
from .Graph import Graph
from .Path import Path
from .Vertex import Vertex
from typing import Tuple


class Planet(Graph):
    def __init__(self, vertexes, edges):
        super().__init__(vertexes, edges)
        self.curr_vertex = None
        self.curr_path = None
        self.paths = []
        EventRegistry.instance().register_event_handler(EventNames.NEW_PATH, self.new_path)
        EventRegistry.instance().register_event_handler(EventNames.CURR_VERTEX, self.set_curr_vertex)
        pass

    def new_path(self, direction):
        path = self.add_path(self.curr_vertex, direction)

        print('new path: ', path)
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
        self.paths.append(path)
        return path
        # if path not in self.paths:
        #     return path
        # else:
        #     return None

    def get_shortest_path(self, start: Vertex, end: Vertex):
        # calculate shortest path
        pass

    def get_next_path(self):
        # depth first
        print('curr_vertex: ', self.curr_vertex)
        if self.curr_vertex:
            for path in self.paths:
                if self.curr_vertex == path.source:
                    self.curr_path = path
                    print('curr_path: ', path)
                    return path

    def set_curr_vertex(self, vertex):
        self.curr_vertex = vertex
        pass
