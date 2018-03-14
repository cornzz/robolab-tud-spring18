import threading


class PathingAlgorithm(threading.Thread):
    # nodes;
    # edges;
    # settledNodes;
    # unSettledNodes;
    # predecessors;
    # distance;

    def __init__(self, graph):
        threading.Thread.__init__(self)
        self.nodes = graph.vertexes
        self.edges = graph.edges
        self.settledNodes = []
        self.distance = {}

    def get_distance(self, node, target):
        for edge in self.edges.values():
            if edge.weight == -1 or edge.start.equals(edge.end):
                return 1000000
            if edge.start.equals(node) and edge.end.equals(target):
                print('distance '
                      '', edge)
                return edge.weight

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges.values():
            if edge.start.equals(node) and not self.is_settled(edge.end):
                neighbors.append(edge.end)
        return neighbors
    pass

    def get_minimum(self, vertexes):
        minimum = None
        for vertex in vertexes:
            if minimum is None:
                minimum = vertex
            else:
                if self.get_shortest_distance(vertex) < self.get_shortest_distance(minimum):
                    minimum = vertex
        return minimum

    def get_shortest_distance(self, end):
        d = self.distance.get(end.position)
        if d is None:
            return 1000000
        else:
            return d

    def is_settled(self, vertex):
        return vertex in self.settledNodes
