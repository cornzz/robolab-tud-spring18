class Graph:
    def __init__(self, vertexes, edges):
        self.vertexes = vertexes or []
        self.edges = edges or []
    pass

    def with_edges(self, edges):
        self.edges = edges
        return self
