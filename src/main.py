from events.EventRegistry import EventRegistry
from events.EventNames import EventNames
from pilot.ColorSensor import ColorSensor
from pilot.TouchSensor import TouchSensor
from pilot.PilotModes import PilotModes
from pilot.Odometry import Odometry
from pilot.Pilot import Pilot
from planet.Planet import Planet
from planet.Communication import Communication
from pilot.MotorMixer import MotorMixer
from pilot.MotorController import MotorController
import ev3dev.ev3 as ev3
import time

# constants
i_max = 100
color_setpoint = 330
speed_max = 50
speed_min = -50
base_speed = 30

btn = ev3.Button()
lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')
cs = ColorSensor()
ts = TouchSensor()
odometry = Odometry()
planet = Planet()
communication = Communication(planet, odometry)
pilot = Pilot(lm, rm, cs, odometry, communication)


class Main:
    def __init__(self):
        self.stop = False
        EventRegistry.instance().register_event_handler(EventNames.TARGET_REACHED, self.set_target_reached)
        EventRegistry.instance().register_event_handler(EventNames.EXPLORATION_FINISHED, self.set_exploration_finished)

    def set_target_reached(self, value):
        time.sleep(1)
        communication.send_target_reached()
        pass

    def set_exploration_finished(self, value):
        time.sleep(1)
        communication.send_exploration_completed()
        pass


def run():
    main = Main()
    # communication.hallo_kilian()
    lm.position = 0
    rm.position = 0
    i = 0
    # this is the main loop
    while not btn.any() or main.stop:
        # read from sensors
        # sensor classes emit events with fresh input
        # classes that depend on should register to those events
        ts.read_in()
        if i == 5 and pilot.mode == PilotModes.FOLLOW_LINE_ODO or pilot.mode == PilotModes.BLOCKED:
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
    communication.stop()
    pass


def learn():
    # use this loop to tune PID factors
    mixer = MotorMixer(base_speed, speed_min, speed_max)
    mc = MotorController(0, 0, 0, i_max, color_setpoint)
    # counter
    step = 5e-4
    i = 0
    while i < 6:
        if ts.read_in():
            i += 1
            stop_motors()
            time.sleep(2)
        if i == 0 or i == 2:
            mc.k_p += step
            print('KP: ', mc.k_p)
        elif i == 1 or i == 3:
            mc.k_d += step
            print('KD: ', mc.k_d)
        elif i == 4:
            mc.k_i += step
            print('KI: ', mc.k_i)
        rgb = cs.get_rgb()              # get rgb values from color sensor
        rudder = mc.run(rgb)            # calculate rudder from color values
        speed = mixer.run(rudder)       # divide the rudder speed on the motors
        lm.duty_cycle_sp = speed[0]
        rm.duty_cycle_sp = speed[1]
        # print('speed: ', speed)
    lm.duty_cycle_sp = 0
    rm.duty_cycle_sp = 0
    print(mc.k_p, mc.k_i, mc.k_d)
    pass


if __name__ == '__main__':
    run()
