from shortest_path.ShortestPath import ShortestPath
from events.EventRegistry import EventRegistry
from events.EventNames import EventNames
from events.EventList import EventList
from pilot.PilotModes import PilotModes
from .Direction import Direction
from .Edge import Edge
from .Graph import Graph
from .Path import Path
from .Vertex import Vertex
from typing import Tuple


class Planet(Graph):
    def __init__(self):
        super().__init__({}, {})
        self.shortest_path = None
        self.shortest_path_counter = 0
        self.shortest_path_running = False
        self.curr_vertex = None
        self.curr_path = None
        self.target = None
        self.mode = PilotModes.EXPLORE
        self.paths = {}
        self.events = EventList()
        self.events.add(EventNames.EXPLORATION_FINISHED)
        EventRegistry.instance().register_event_handler(EventNames.SHORTEST_PATH, self.set_shortest_path)
        pass

    # ---------
    # GRAPH MANIPULATION
    # ---------
    def add_edge(self, start: Path, end: Path, length: float, flag):
        edge_to = Edge(start.source, end.source, start.direction, end.direction, length)
        edge_from = Edge(end.source, start.source, end.direction, start.direction, length)
        if flag or (edge_from.id not in self.edges and edge_to.id not in self.edges):
            if start.id in self.paths:
                print('deleting path: ', self.paths[start.id])
                del self.paths[start.id]
            if end.id in self.paths:
                print('deleting path: ', self.paths[end.id])
                del self.paths[end.id]
            self.edges[edge_from.id] = edge_from
            self.edges[edge_to.id] = edge_to
            return edge_to
        else:
            return None

    def add_vertex(self, position: Tuple[int, int]):
        vertex = Vertex(position)
        # if vertex.id not in self.vertexes:
        self.vertexes[vertex.id] = vertex
        return vertex
        # else:
        #     return None

    def add_path(self, source: Vertex, direction: Direction):
        path = Path(source, direction)
        if path.id not in self.paths:
            self.paths[path.id] = path
            print('new path: ' + str(path))
            return path
        else:
            return None

    def vertex_exists(self, position):
        for vertex in self.vertexes.values():
            if vertex.position == position:
                return vertex
        return False

    # ---------
    # SETTER
    # ---------
    def set_shortest_path(self, sp):
        self.shortest_path = sp
        self.shortest_path_counter = 0
        pass

    def set_curr_vertex(self, vertex):
        self.curr_vertex = vertex
        pass

    def set_target_mode(self):
        print('TARGET MODE')
        self.mode = PilotModes.TARGET
        pass

    def set_target(self, target):
        self.target = target
        print('target saved!')
        pass

    # ---------
    # GETTER
    # ---------
    def get_paths(self):
        return self.paths

    def get_shortest_path(self, end: Vertex):
        self.shortest_path_counter = 0
        sp = ShortestPath(self, self.curr_vertex, end)
        sp.run()
        pass

    def get_next_path(self):
        print(self.mode, self.mode == PilotModes.TARGET)
        if self.mode == PilotModes.EXPLORE:
            # depth first
            if self.curr_vertex:
                paths = list(self.paths.values())
                print('paths left:')
                for path in paths:
                    print(path)
                for path in self.paths.values():
                    if self.curr_vertex.equals(path.source):
                        self.curr_path = path
                        print('next path: ', self.curr_path)
                        return self.curr_path
                if paths.__len__() > 0:
                    path = paths[0]
                    if not self.shortest_path_running:
                        self.get_shortest_path(path.source)
                        self.shortest_path_running = True
                    if self.shortest_path \
                            and self.shortest_path.__len__() > 0 \
                            and self.shortest_path_counter < self.shortest_path.__len__():
                        edge = self.shortest_path[self.shortest_path_counter]
                        self.shortest_path_counter += 1
                        self.curr_path = Path(edge.start, edge.start_direction)
                        print('next path: ', self.curr_path, ' sp_counter = ' + str(self.shortest_path_counter))
                        return self.curr_path
                else:
                    self.events.set(EventNames.EXPLORATION_FINISHED, True)
                    return False
        if self.mode == PilotModes.TARGET:
            print('shortest path is:')
            if self.shortest_path.__len__() > 0:
                for edge in self.shortest_path:
                    print(edge)
                edge = self.shortest_path[self.shortest_path_counter]
                self.shortest_path_counter += 1
                self.curr_path = Path(edge.start, edge.start_direction)
                print('next path: ', self.curr_path, ' sp_counter = ' + str(self.shortest_path_counter))
                return self.curr_path
            else:
                print('shortest path not working or target not reachable!')
                return False
        else:
            return False
