from pilot.ColorSensor import ColorSensor
from pilot.TouchSensor import TouchSensor
from pilot.Pilot import Pilot
import ev3dev.ev3 as ev3

# init ev3
lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')
# init classes
cs = ColorSensor()
ts = TouchSensor()
pilot = Pilot(lm, rm, cs)


def run():
    # this is the main loop
    while not ts.read_in():
        # read from sensors
        # sensor classes emit events with fresh input
        # classes that depend on should register to those events
        cs.read_in()
        # switch PILOT_MODE and run corresponding maneuver
        pilot.run()
    pilot.stop_motors()
    pass


if __name__ == '__main__':
    run()
