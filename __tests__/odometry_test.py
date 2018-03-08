from src.pilot.Odometry import Odometry
import unittest


class OdometryTestCase(unittest.TestCase):
    def setUp(self):
        self.odometry = Odometry()
        self.motor_position = (-259, 259)
        pass

    def test_calc_pos(self):
        position = self.odometry.read_in(self.motor_position)
        print(position)
        pass


if __name__ == '__main__':
    unittest.main()
