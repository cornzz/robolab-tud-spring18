import ev3dev.ev3 as ev3


class ColorSensor:
    def __init__(self):
        self.cs = ev3.ColorSensor('in1')
        self.cs.mode = 'RGB-RAW'

    def get_rgb(self):
        return self.cs.bin_data('hhh')
