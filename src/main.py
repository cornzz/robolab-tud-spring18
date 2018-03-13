from pilot.ColorSensor import ColorSensor
from pilot.TouchSensor import TouchSensor
from pilot.PilotModes import PilotModes
from pilot.Odometry import Odometry
from pilot.Pilot import Pilot
from planet.Planet import Planet
from planet.Communication import Communication
import ev3dev.ev3 as ev3

# init ev3

lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')
cs = ColorSensor()
ts = TouchSensor()
odometry = Odometry()
planet = Planet()
communication = Communication(planet)
pilot = Pilot(lm, rm, cs, odometry, communication)


def init(lm, rm, cs, ts, odometry, pilot):
    lm = ev3.LargeMotor('outA')
    rm = ev3.LargeMotor('outD')
    cs = ColorSensor()
    ts = TouchSensor()
    odometry = Odometry()
    pilot = Pilot(lm, rm, cs, odometry)
    print('initialized.')


def run():
    # init classes
    lm.position = 0
    rm.position = 0
    i = 0
    # this is the main loop
    while not ts.read_in():
        # read from sensors
        # sensor classes emit events with fresh input
        # classes that depend on should register to those events
        if i == 5 and pilot.mode == PilotModes.FOLLOW_LINE_ODO:
            odometry.read_in((lm.position, rm.position))
            i = 0
        if pilot.mode == PilotModes.FOLLOW_LINE or pilot.mode == PilotModes.FOLLOW_LINE_ODO:
            cs.read_in()
        # switch PILOT_MODE and run corresponding maneuver
        pilot.run()
        if i == 5:
            i = 0
        i += 1
    # pilot.test(40, -90)
    pilot.stop_motors()
    pass


if __name__ == '__main__':
    run()
