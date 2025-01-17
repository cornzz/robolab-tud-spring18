#!/usr/bin/env python3

import unittest
from src.events.EventNames import EventNames
from src.events.EventRegistry import EventRegistry
from src.planet.Planet import Planet
from src.planet.Direction import Direction
from src.planet.Vertex import Vertex
from src.shortest_path.ShortestPath import ShortestPath


class TestPlanet(unittest.TestCase):
    # test planet is Terrabyte
    def setUp(self):
        self.planet = Planet()
        EventRegistry.instance().register_event_handler(EventNames.SHORTEST_PATH, self.set_sp)
        self.expected = None
        pass

    def test_integrity(self):
        planet = create_planet()
        paths = planet.get_paths()
        self.assertIsNotNone(paths)

    def test_empty_planet(self):
        self.assertEqual(self.planet.vertexes, {})
        self.assertEqual(self.planet.edges, {})
        self.assertEqual(self.planet.paths, {})
        pass

    # def test_target_not_reachable(self):
    #     time.sleep(5)
    #     self.planet = create_planet()
    #     start = self.planet.vertexes[(0, -1)]
    #     target = Vertex((2, 5))
    #     sp = ShortestPath(self.planet, start, target)
    #     sp.run()
    #     pass

    def test_shortest_path(self):
        self.planet = create_planet()
        start = self.planet.vertexes[(0, -1)]
        target = self.planet.vertexes[(2, 2)]

        sp = ShortestPath(self.planet, start, target)
        sp.run()
        pass

    def set_sp(self, sp):
        expected = [
            self.planet.edges[(((0, -1), 0), ((0, 0), 180))],
            self.planet.edges[(((0, 0), 90), ((1, 0), 270))],
            self.planet.edges[(((1, 0), 0), ((2, 2), 180))]
        ]
        i = 0
        for edge in sp:
            # self.assertEqual(edge, expected[i])
            print(edge)
            i += 1
        pass


if __name__ == "__main__":
    unittest.main()


def create_planet():
    planet = Planet()
    planet.add_vertex((0, 0))
    planet.add_vertex((2, 0))
    planet.add_vertex((-1, 2))
    planet.add_vertex((-2, 2))
    planet.add_vertex((-2, 1))
    planet.add_path(planet.vertexes[(0, 0)], Direction.WEST)
    planet.add_path(planet.vertexes[(0, 0)], Direction.EAST)

    planet.add_path(planet.vertexes[(2, 0)], Direction.WEST)
    planet.add_path(planet.vertexes[(2, 0)], Direction.SOUTH)
    planet.add_path(planet.vertexes[(2, 0)], Direction.EAST)

    planet.add_path(planet.vertexes[(-1, 2)], Direction.NORTH)
    planet.add_path(planet.vertexes[(-1, 2)], Direction.SOUTH)
    planet.add_path(planet.vertexes[(-1, 2)], Direction.WEST)
    planet.add_path(planet.vertexes[(-1, 2)], Direction.EAST)

    planet.add_path(planet.vertexes[(-2, 2)], Direction.SOUTH)
    planet.add_path(planet.vertexes[(-2, 2)], Direction.EAST)

    planet.add_path(planet.vertexes[(-2, 1)], Direction.NORTH)
    planet.add_path(planet.vertexes[(-2, 1)], Direction.WEST)
    planet.add_path(planet.vertexes[(-2, 1)], Direction.SOUTH)
    planet.add_path(planet.vertexes[(-2, 1)], Direction.EAST)

    planet.add_edge(
        planet.paths[((0, 0), Direction.EAST)], planet.paths[((0, 2), Direction.EAST)], 1)
    planet.add_edge(
        planet.paths[((0, 2), Direction.WEST)], planet.paths[((-1, 2), Direction.EAST)], 1)
    planet.add_edge(
        planet.paths[((-1, 2), Direction.NORTH)], planet.paths[((-1, 2), Direction.NORTH)], -1)
    planet.add_edge(
        planet.paths[((-1, 2), Direction.WEST)], planet.paths[((-2, 2), Direction.EAST)], 1)
    planet.add_edge(
        planet.paths[((-2, 2), Direction.SOUTH)], planet.paths[((-2, 1), Direction.NORTH)], 1)
    planet.add_edge(
        planet.paths[((-2, 1), Direction.WEST)], planet.paths[((-2, 1), Direction.SOUTH)], 1)
    planet.add_edge(
        planet.paths[((-2, 1), Direction.WEST)], planet.paths[((0, 2), Direction.WEST)], 0)
    return planet
