from . import PathingAlgorithm
from events.EventList import EventList
from events.EventNames import EventNames
import time


class ShortestPath(PathingAlgorithm.PathingAlgorithm):
    def __init__(self, graph, start, target):
        super().__init__(graph)
        self.start = start
        self.target = target
        self.unSettledNodes = []
        self.predecessors = {}
        self.events = EventList()
        self.events.add(EventNames.SHORTEST_PATH)
        self.start_time = time.time()
        pass

    def execute(self):
        self.distance[self.start.position] = 0
        self.unSettledNodes.append(self.start)

        while self.unSettledNodes.__len__() > 0:
            node = self.get_minimum(self.unSettledNodes)
            self.settledNodes.append(node)
            self.unSettledNodes.remove(node)
            self.find_minimal_distances(node)
            if time.time() - self.start_time >= 10:
                break
        return self

    def find_minimal_distances(self, node):
        adjacent_nodes = self.get_neighbors(node)
        for target in adjacent_nodes:
            if (
                self.get_shortest_distance(target)
                > self.get_shortest_distance(node) + self.get_distance(node, target)
            ):
                self.distance[target.position] = self.get_shortest_distance(node) + self.get_distance(node, target)
                self.predecessors[target.position] = node
                self.unSettledNodes.append(target)
        pass

    def get_path(self):
        vertexes = []
        step = self.target
        # check if a vertexes exists
        if self.predecessors.get(step.position) is None:
            return None
        vertexes.append(step)
        while self.predecessors.get(step.position):
            step = self.predecessors.get(step.position)
            vertexes.append(step)
        vertexes.append(self.start)
        vertexes.pop()
        vertexes.reverse()
        path = []
        length = vertexes.__len__() - 2
        if length > 0:
            for i in range(vertexes.__len__() - 1):
                if i >= 0:
                    for e in self.edges.values():
                        if vertexes[i].equals(e.start) and vertexes[i + 1].equals(e.end):
                            path.append(e)

        return path

    def run(self):
        print('ShortestPath Thread started!')

        path = self.execute().get_path()
        self.events.set(EventNames.SHORTEST_PATH, path)
        print('ShortestPath Thread finished!')
        pass
