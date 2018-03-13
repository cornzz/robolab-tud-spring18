from src.planet.Communication import Communication
from src.planet.Planet import Planet
from src.planet.Path import Path
from src.planet.Vertex import Vertex
import time

if __name__ == '__main__':
    comm = Communication(Planet())
    comm.start()
    time.sleep(2)
    comm.send_test_planet()
    # comm.send_ready()
    # time.sleep(2)
    #
    # dirs = [0, 90, 180, 270]
    # for d1 in dirs:
    #     for d2 in dirs:
    #         print('TEST: ', d1, d2)
    #         path1 = Path(Vertex((0, 0)), d1)
    #         path2 = Path(Vertex((1, 0)), d2)
    #         edge = comm.planet.add_edge(path1, path2, 0)
    #         comm.send_edge(edge, 'free')
    #         time.sleep(1)

    while True:
        pass
