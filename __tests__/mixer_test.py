from src.pilot import MotorMixer
import unittest


class TestMixer(unittest.TestCase):
    mixer1 = MotorMixer.MotorMixer(50, -100, 100)
    mixer2 = MotorMixer.MotorMixer(100, -250, 250)

    def test_run(self):
        self.assertEqual(self.mixer1.run(75), (100, -50))
        self.assertEqual(self.mixer2.run(-200), (-150, 250))


if __name__ == '__main__':
    unittest.main()
