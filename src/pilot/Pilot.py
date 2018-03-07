from events.EventNames import EventNames
from events.EventRegistry import EventRegistry
from events.EventList import EventList
from .ColorSensor import ColorSensor
from .MotorController import MotorController
from .MotorMixer import MotorMixer
from .PilotModes import PilotModes
from planet import Planet
from ev3dev import ev3
from typing import Tuple
import time

# constants
K_P = 0.62
K_I = 0.05
K_D = 0.3
I_MAX = 40
SETPOINT = 330
SPEED_MAX = 100
SPEED_MIN = -100
BASE_SPEED = 30


class Pilot:
    # this is the main driving class
    # simple or complex maneuvers (follow line, turn, stop, ...) are defined as methods
    # PILOT_MODE decides which maneuver is called in the main loop

    def __init__(self, lm, rm, cs: ColorSensor):
        self.current_vertex = None
        self.position = (0, 0)
        self.planet = Planet.Planet([], [])
        self.lm = lm
        self.rm = rm
        self.cs = cs
        self.color = None
        self.rbd = None
        self.touch = False
        self.mode = PilotModes.FOLLOW_LINE
        self.mixer = MotorMixer(BASE_SPEED, SPEED_MIN, SPEED_MAX)
        self.mc = MotorController(K_P, K_I, K_D, I_MAX, SETPOINT)
        self.events = EventList()
        self.events.add('NEW_PATH')
        EventRegistry.instance().register_event_handler(EventNames.PILOT_MODE, self.set_mode)
        EventRegistry.instance().register_event_handler(EventNames.COLOR, self.set_color)
        EventRegistry.instance().register_event_handler(EventNames.TOUCH, self.set_touch)
        pass

    def run(self):
        if self.mode is PilotModes.FOLLOW_LINE:
            self.follow_line()
        elif self.mode is PilotModes.HOVER_PATCH:
            self.hover_patch()
        elif self.mode is PilotModes.CHECK_ISC:
            self.check_isc()
        pass

    # ---------
    # MANEUVERS
    # ---------
    def stop_motors(self):
        self.set_speed((0, 0))
        pass

    def follow_line(self):
        if self.color is not None:
            self.lm.command = 'run-direct'
            self.rm.command = 'run-direct'
            # calculate rudder from rgb mean
            rudder = self.mc.run(self.color)
            # divide the rudder speed on the motors
            speed = self.mixer.run(rudder)
            self.set_speed(speed)
            # print(speed)
        pass

    def hover_patch(self):
        self.stop_motors()
        ev3.Sound.beep()
        time.sleep(1)
        # save calculated position as vertex if it not already exists
        self.set_position()
        vertex = self.planet.add_vertex(self.position)
        # save vertex for later use
        self.current_vertex = vertex
        self.mode = PilotModes.CHECK_ISC

        #  TODO: überdrehen kompensieren

    def turn_motor(self, motor, degrees):
        self.stop_motors()
        self.rm.position = 0
        # turn by degrees
        p_sp = 5.7361 * degrees
        if motor is 'lm':
            self.lm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")
        if motor is 'rm':
            self.rm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")

        print('Turned ' + str(degrees) + ' degrees.')
        return p_sp

    def turn(self, degrees):
        self.stop_motors()
        # turn by degrees
        p_sp = 2.88 * degrees
        self.lm.run_to_rel_pos(position_sp=-p_sp, speed_sp=200, stop_action="hold")
        self.rm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")
        print('Turned ' + str(degrees) + ' degrees.')
        pass

    def check_isc(self):
        #  TODO: Intersection checken (turn(deg))
        self.stop_motors()
        time.sleep(0.5)
        self.turn(-90)
        time.sleep(3)
        p_sp = self.turn_motor('rm', 360)
        while self.rm.position < p_sp - 10:
            gs = self.cs.get_greyscale()
            if gs < 100:
                print(gs)
                self.events.set('NEW_PATH', self.rm.position)
                time.sleep(0.75)
        self.turn(90)
        time.sleep(3)
        self.lm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
        self.rm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
        time.sleep(1)
        self.mode = PilotModes.FOLLOW_LINE
        return self

    # ---------
    # SETTER
    # ---------
    def set_position(self):
        # TODO: implement odometry
        self.position = (0, 0)
        return 0, 0

    def set_color(self, value):
        self.color = value
        self.rbd = value[0] - value[2]
        # gs = (value[0] + value[1] + value[2]) / 3
        # print('RBD: ' + str(self.rbd) + '  GS: ' + str(gs))
        if 90 <= self.rbd:       # red patch
            self.mode = PilotModes.CHECK_ISC
            print('red')
        elif self.rbd <= -65:    # blue patch
            self.mode = PilotModes.CHECK_ISC
            print('blue')
        pass

    def set_mode(self, mode):
        self.mode = mode
        pass

    def set_touch(self, value):
        self.touch = value
        pass

    def set_speed(self, speed: Tuple[int, int]):
        self.lm.duty_cycle_sp = speed[0]
        self.rm.duty_cycle_sp = speed[1]
        pass

    # ---------
    # GETTER
    # ---------
    def get_position(self):
        return self.position

    def get_mode(self):
        return self.mode
