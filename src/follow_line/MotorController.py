from pid_controller import Controller


class MotorController(Controller.AbstractController):
    def __init__(self, k_p, k_i, k_d, i_max, setpoint):
        super().__init__(k_p, k_i, k_d, i_max)
        self.setpoint = setpoint

    def calc_error(self, value, setpoint):
        #           R         G          B
        grey_scale = (value[0] + value[1] + value[2]) / 3  # grey scale color
        return self.setpoint - grey_scale

    def run(self, color_value):
        error = self.calc_error(color_value, self.setpoint)
        return max(-100, min(100, self.main(error)))
