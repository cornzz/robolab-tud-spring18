class PathingAlgorithm:
    # nodes;
    # edges;
    # settledNodes;
    # unSettledNodes;
    # predecessors;
    # distance;

    def __init__(self, graph):
        self.nodes = graph.vertexes
        self.edges = graph.edges
        self.settledNodes = []
        self.distance = {}

    def get_distance(self, node, target):
        i = 0
        while i < self.edges.__len__():
            edge = self.edges[i]
            if edge.source.equals(node) and edge.destination.equals(target):
                return edge.weight
            i += 1
    pass

    def get_neighbors(self, node):
        neighbors = []
        i = 0
        while i < self.edges.__len__():
            edge = self.edges[i]
            if edge.source.equals(node) and not self.is_settled(edge.destination):
                neighbors.append(edge.destination)
            i += 1
        return neighbors
    pass

    def get_minimum(self, vertexes):
        minimum = None
        i = 0
        while i < vertexes.__len__():
            vertex = vertexes[i]
            if minimum is None:
                minimum = vertex
            else:
                if self.get_shortest_distance(vertex) < self.get_shortest_distance(minimum):
                    minimum = vertex
            i += 1
        return minimum

    def get_shortest_distance(self, destination):
        d = self.distance.get(destination.id)
        if d is None:
            return 1000000000
        else:
            return d

    def is_settled(self, vertex):
        return vertex in self.settledNodes
