import time

from src.pid_controller import Controller
import random


class MotorController(Controller.AbstractController):
    def __init__(self, k_p, k_i, k_d, i_max, setpoint):
        super().__init__(k_p, k_i, k_d, i_max)
        self.setpoint = setpoint

    def calc_error(self, value, setpoint):
        return self.setpoint - value


def test_motor_controller():
    value = 1500
    setpoint = 1000
    mc = MotorController(0.5, 0.2, 0.05, 20, setpoint)
    while True:
        value += random.random() * 5 - 2.5 # fuegt etwas rauschen hinzu
        print('input: ', value)
        error = mc.calc_error(value)
        value += mc.main(error)
        print('output: ', value)
        time.sleep(0.25)


test_motor_controller()
