#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from follow_line import ColorSensor
from color_net import CSVWriter


def run():
    writer = CSVWriter.CSVWriter('training')
    cs = ColorSensor.ColorSensor()
    ts1 = ev3.TouchSensor('in2')
    ts2 = ev3.TouchSensor('in4')
    values = []

    while not ts1.value() and not ts2.value():
        value = cs.get_rgb()
        values.append('0,' + str(value[0]) + ',' + str(value[1]) + ',' + str(value[2]))
        pass

    writer.write(values)

    #  0 - blue
    #  1 - red


if __name__ == '__main__':
    run()
