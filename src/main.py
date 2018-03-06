from .events.EventRegistry import EventRegistry
from .pilot.ColorSensor import ColorSensor
from src.pilot.Pilot import Pilot
import ev3dev.ev3 as ev3

# init ev3
ts1 = ev3.TouchSensor('in2')
ts2 = ev3.TouchSensor('in3')
lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')
# init classes
registry = EventRegistry()
cs = ColorSensor(registry)
pilot = Pilot(lm, rm, registry)


def run():
    # this is the main loop
    while not ts1.value() and not ts2.value():
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
