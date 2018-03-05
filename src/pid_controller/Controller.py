from abc import ABC, abstractmethod


class AbstractController(ABC):
    def __init__(self, k_p, k_i, k_d, i_max):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.i_max = i_max
        self.previous_error = 0
        self.i_error = 0
    pass

    def main(self, error):
        # set derivative error
        d_error = error - self.previous_error
        print('error: ', error)
        result = (self.k_p * error) + (self.k_i * self.i_error) + (self.k_d * d_error)
        print('ctrl: ', result)
        self.previous_error = error
        self.i_error = min(self.i_max, self.i_error + error)
        return result

    @abstractmethod
    def calc_error(self, value, setpoint):
        pass
