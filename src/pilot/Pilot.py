from src.events.EventNames import EventNames
from src.events.EventRegistry import EventRegistry
from .MotorController import MotorController
from .MotorMixer import MotorMixer
from .PilotModes import PilotModes
from src.planet import Planet
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

    def __init__(self, lm, rm):
        self.current_vertex = None
        self.position = (0, 0)
        self.planet = Planet.Planet([], [])
        self.lm = lm
        self.rm = rm
        self.color = None
        self.mode = PilotModes.FOLLOW_LINE
        self.mixer = MotorMixer(BASE_SPEED, SPEED_MIN, SPEED_MAX)
        self.mc = MotorController(K_P, K_I, K_D, I_MAX, SETPOINT)
        EventRegistry.instance().register_event_handler(EventNames.PILOT_MODE, self.set_mode)
        EventRegistry.instance().register_event_handler(EventNames.COLORS, self.set_color)
        pass

    def run(self):
        if self.mode is PilotModes.FOLLOW_LINE:
            self.follow_line()
        elif self.mode is PilotModes.HOVER_PATH:
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
        self.lm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
        self.rm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
        time.sleep(1)
        #  TODO: überdrehen kompensieren

    def turn(self, degrees):
        self.stop_motors()
        # turn by degrees
        p_sp = 2.88 * degrees
        self.lm.run_to_rel_pos(position_sp=-p_sp, speed_sp=200, stop_action="hold")
        self.rm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")
        # print('Turned ' + str(degrees) + ' degrees.')
        pass

    def check_isc(self):
        #  TODO: Intersection checken (turn(deg))
        time.sleep(5)
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
        rbd = value[0] - value[2]
        # gs = (value[0] + value[1] + value[2]) / 3
        # print('RBD: ' + str(rbd) + '  GS: ' + str(gs))
        if 90 <= rbd:       # red patch
            self.mode = PilotModes.HOVER_PATH
            print('red')
        elif rbd <= -65:    # blue patch
            self.mode = PilotModes.HOVER_PATH
            print('blue')
        pass

    def set_mode(self, mode):
        self.mode = mode
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
