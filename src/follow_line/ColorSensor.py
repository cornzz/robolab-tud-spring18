import ev3dev.ev3 as ev3
import colorsys
import sys

# console color constants
RED = "\033[1;31m"
BLUE = "\033[1;34m"
GREY = "\033[1;90m"
RESET = "\033[0;0m"
WHITE = "\033[;1m"


class ColorSensor:
    def __init__(self):
        self.cs = ev3.ColorSensor('in1')
        self.cs.mode = 'RGB-RAW'

    def get_rgb(self):
        return self.cs.bin_data('hhh')

    def get_hsv(self):
        value = self.get_rgb()
        r = map_to_range(value[0], 0, 480, 0, 1)
        g = map_to_range(value[1], 0, 480, 0, 1)
        b = map_to_range(value[2], 0, 480, 0, 1)
        return colorsys.rgb_to_hsv(r, g, b)

    def get_all(self):
        rgb = self.get_rgb()
        hsv = self.get_hsv()
        # color     s > 0.68
        # blue      h > 0.3
        # red       h <= 0.1
        # black     v < 0.2
        # white     v >= 0.9
        h = hsv[0]
        s = hsv[1]
        v = hsv[2]
        if s > 0.68:
            if h > 0.3:
                sys.stdout.write(BLUE)
            elif h <= 0.1:
                sys.stdout.write(RED)
        else:
            if v < 0.2:
                sys.stdout.write(GREY)
            elif v >= 0.9:
                sys.stdout.write(WHITE)

        print(rgb, hsv, (rgb[0] + rgb[1] + rgb[2]) / 3)
        sys.stdout.write(RESET)
        return rgb, hsv


def map_to_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
