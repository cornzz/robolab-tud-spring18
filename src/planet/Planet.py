from shortest_path.ShortestPath import ShortestPath
from events.EventRegistry import EventRegistry
from events.EventNames import EventNames
from .Direction import Direction
from .Edge import Edge
from .Graph import Graph
from .Path import Path
from .Vertex import Vertex
from typing import Tuple


class Planet(Graph):
    def __init__(self):
        super().__init__({}, {})
        self.curr_vertex = None
        self.curr_path = None
        self.paths = {}
        EventRegistry.instance().register_event_handler(EventNames.NEW_PATH, self.new_path)
        EventRegistry.instance().register_event_handler(EventNames.CURR_VERTEX, self.set_curr_vertex)
        pass

    def new_path(self, direction):
        path = self.add_path(self.curr_vertex, direction)
        print('new path: ', path)
        return self

    def combine_paths(self, start: Path, end: Path, length: float):
        _id_to = (start.source.position, end.source.position)
        _id_from = (end.source.position, start.source.position)
        edge_to = Edge(_id_to, start.source, end.source, start.direction, end.direction, length)
        edge_from = Edge(_id_from, end.source, start.source, end.direction, start.direction, length)
        if _id_from not in self.edges and _id_to not in self.edges:
            del self.paths[start.id]
            del self.paths[end.id]
            self.edges[_id_from] = edge_from
            self.edges[_id_to] = edge_to
            return edge_from, edge_to
        else:
            return None

    def add_vertex(self, position: Tuple[int, int]):
        _id = position
        vertex = Vertex(position)
        if _id not in self.vertexes:
            self.vertexes[_id] = vertex
            return vertex
        else:
            return None

    def add_path(self, source: Vertex, direction: Direction):
        _id = (source.position, direction)
        path = Path(_id, source, direction)
        if _id not in self.paths:
            self.paths[_id] = path
            return path
        else:
            return None

    def get_shortest_path(self, end: Vertex):

        pass

    def get_next_path(self):
        # depth first
        if self.curr_vertex:
            for path in self.paths.values():
                if self.curr_vertex == path.source:
                    self.curr_path = path
                    print('next path: ', path)
                    return path

    def set_curr_vertex(self, vertex):
        self.curr_vertex = vertex
        pass

    def get_paths(self):
        return self.paths
