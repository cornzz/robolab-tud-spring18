from src.shortest_path import ShortestPath
from src.planet import Edge, Vertex, Graph
from src.planet.Direction import Direction
import unittest


def add_edge(edges, vertexes, i, a, b, sd, ed, weight):
    edges.append(Edge.Edge(i, vertexes[a], vertexes[b], sd, ed, weight))
    pass


def add_vertex(vertexes, i, x, y):
    vertexes.append(Vertex.Vertex(i, x, y))
    pass


class ShortestPathTest(unittest.TestCase):
    def setUp(self):
        self.edges = []
        self.vertexes = []
        add_vertex(self.vertexes, 0, 0, 0)
        add_vertex(self.vertexes, 1, 1, 2)
        add_vertex(self.vertexes, 2, 0, 4)
        add_vertex(self.vertexes, 3, 5, 2)
        add_vertex(self.vertexes, 4, 5, 6)
        add_vertex(self.vertexes, 5, 7, 6)
        add_vertex(self.vertexes, 6, 2, 4)
        add_vertex(self.vertexes, 7, 1, 1)
        add_vertex(self.vertexes, 8, 10, 1)
        add_vertex(self.vertexes, 9, 3, 5)
        add_vertex(self.vertexes, 10, 5, 5)
        add_edge(self.edges, self.vertexes, 0, 0, 1, Direction.NORTH, Direction.WEST, 2)
        add_edge(self.edges, self.vertexes, 1, 0, 2, Direction.WEST, Direction.SOUTH, 4)
        add_edge(self.edges, self.vertexes, 2, 0, 4, Direction.EAST, Direction.SOUTH, 9)
        add_edge(self.edges, self.vertexes, 3, 2, 6, Direction.NORTH, Direction.WEST, 1.5)
        add_edge(self.edges, self.vertexes, 4, 2, 7, Direction.EAST, Direction.NORTH, 3)
        add_edge(self.edges, self.vertexes, 5, 3, 7, Direction.SOUTH, Direction.EAST, 5)
        add_edge(self.edges, self.vertexes, 6, 5, 8, Direction.EAST, Direction.NORTH, 6)
        add_edge(self.edges, self.vertexes, 7, 8, 9, Direction.WEST, Direction.SOUTH, 8)
        add_edge(self.edges, self.vertexes, 8, 4, 9, Direction.NORTH, Direction.WEST, 2)
        add_edge(self.edges, self.vertexes, 9, 9, 10, Direction.EAST, Direction.WEST, 6)
        add_edge(self.edges, self.vertexes, 10, 1, 3, Direction.EAST, Direction.SOUTH, 2)
        add_edge(self.edges, self.vertexes, 11, 3, 9, Direction.NORTH, Direction.SOUTH, 2)
        self.graph = Graph.Graph(self.vertexes, self.edges)
        self.sp = ShortestPath.ShortestPath(self.graph)

    def test_shortest_path(self):
        start = self.vertexes[0]
        end = self.vertexes[9]
        path = self.sp.execute(start).get_path(end)
        excepted_path = [self.edges[10], self.edges[11]]
        length = 0
        self.assertEqual(path, excepted_path)
        print('Path is ')
        for edge in path:
            print(edge.tostring())
            length += edge.weight
        print(length)
        pass


if __name__ == '__main__':
    unittest.main()
