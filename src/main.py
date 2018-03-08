from pilot.ColorSensor import ColorSensor
from pilot.TouchSensor import TouchSensor
from pilot.PilotModes import PilotModes
from pilot.Odometry import Odometry
from pilot.Pilot import Pilot
import ev3dev.ev3 as ev3

# init ev3
lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')
lm.position = 0
rm.position = 0


def run():
    # init classes
    cs = ColorSensor()
    ts = TouchSensor()
    odometry = Odometry()
    pilot = Pilot(lm, rm, cs)
    i = 0
    # this is the main loop
    while not ts.read_in():
        # read from sensors
        # sensor classes emit events with fresh input
        # classes that depend on should register to those events
        if i == 5 and pilot.mode == PilotModes.FOLLOW_LINE:
            odometry.read_in((lm.position, rm.position))
            lm.position = 0
            rm.position = 0
            i = 0
        cs.read_in()
        # switch PILOT_MODE and run corresponding maneuver
        pilot.run()
        i += 1
    pilot.stop_motors()
    pass


if __name__ == '__main__':
    run()
