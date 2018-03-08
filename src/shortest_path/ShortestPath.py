from shortest_path import PathingAlgorithm


class ShortestPath(PathingAlgorithm.PathingAlgorithm):
    def __init__(self, graph):
        super().__init__(graph)
        self.unSettledNodes = []
        self.predecessors = {}
    pass

    def execute(self, source):
        self.distance[source.id] = 0
        self.unSettledNodes.append(source)

        while self.unSettledNodes.__len__() > 0:
            node = self.get_minimum(self.unSettledNodes)
            self.settledNodes.append(node)
            self.unSettledNodes.remove(node)
            self.find_minimal_distances(node)

        return self

    def find_minimal_distances(self, node):
        adjacent_nodes = self.get_neighbors(node)
        i = 0
        while i < adjacent_nodes.__len__():
            target = adjacent_nodes[i]
            if (
                self.get_shortest_distance(target)
                > self.get_shortest_distance(node) + self.get_distance(node, target)
            ):
                self.distance[target.id] = self.get_shortest_distance(node) + self.get_distance(node, target)
                self.predecessors[target.id] = node
                self.unSettledNodes.append(target)
            i += 1
    pass

    def get_path(self, target):
        path = []
        step = target
        # check if a path exists
        if self.predecessors.get(step.id) is None:
            return None
        path.append(step)
        while self.predecessors.get(step.id):
            step = self.predecessors.get(step.id)
            path.append(step)
        path.pop()
        path.reverse()
        return path
