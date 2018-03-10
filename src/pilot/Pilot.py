from .ColorSensor import ColorSensor
from .MotorController import MotorController
from .MotorMixer import MotorMixer
from .PilotModes import PilotModes
from .Odometry import Odometry
from events.EventNames import EventNames
from events.EventRegistry import EventRegistry
from events.EventList import EventList
from planet.Direction import Direction
from planet.Planet import Planet
from ev3dev import ev3
from typing import Tuple
import time

# constants
K_P = 0.62
K_I = 0.05
K_D = 0.3
I_MAX = 100
SETPOINT = 330
SPEED_MAX = 100
SPEED_MIN = -100
BASE_SPEED = 30


class Pilot:
    # this is the main driving class
    # simple or complex maneuvers (follow line, turn, stop, ...) are defined as methods
    # PILOT_MODE decides which maneuver is called in the main loop

    def __init__(self, lm, rm, cs: ColorSensor, odometry):
        #  values
        self.mode = PilotModes.FOLLOW_LINE
        self.vertex = None
        self.path = None
        self.position = (0, 0, 0)
        self.color = None
        self.rbd = None
        self.touch = False
        # motors
        self.lm = lm
        self.rm = rm
        # controllers, classes
        self.cs = cs
        self.odometry = odometry
        self.planet = Planet()
        self.mixer = MotorMixer(BASE_SPEED, SPEED_MIN, SPEED_MAX)
        self.mc = MotorController(K_P, K_I, K_D, I_MAX, SETPOINT)

        # IPC
        self.events = EventList()
        self.events\
            .add(EventNames.NEW_PATH)\
            .add(EventNames.CURR_VERTEX)
        EventRegistry.instance().register_event_handler(EventNames.PILOT_MODE, self.set_mode)
        EventRegistry.instance().register_event_handler(EventNames.COLOR, self.set_color)
        EventRegistry.instance().register_event_handler(EventNames.TOUCH, self.set_touch)
        EventRegistry.instance().register_event_handler(EventNames.POSITION, self.set_position)
        pass

    def run(self):
        if self.mode is PilotModes.FOLLOW_LINE:
            self.follow_line()
        elif self.mode is PilotModes.CHECK_ISC:
            self.check_isc()
        elif self.mode is PilotModes.CHOOSE_PATH:
            self.choose_path()
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

    def turn_motor(self, motor, degrees):
        # turn by degrees
        p_sp = 5.7361 * degrees
        if motor is 'lm':
            self.lm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")
        if motor is 'rm':
            self.rm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")
        return p_sp

    def turn(self, degrees):
        # turn by degrees
        p_sp = 2.88 * degrees
        self.lm.run_to_rel_pos(position_sp=-p_sp, speed_sp=200, stop_action="hold")
        self.rm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")
        print('Turning: ' + str(degrees) + ' degrees.')
        duration = abs(degrees) / 90 * 1.3
        time.sleep(duration)
        pass

    def check_isc(self):
        print('check_isc()')
        self.stop_motors()
        print(self.position)
        vertex = self.planet.add_vertex((self.position[0], self.position[1]))
        self.events.set(EventNames.CURR_VERTEX, vertex)

        self.turn(-90)
        print('Turning: 362 degrees.')

        self.rm.position = 0
        target_pos = self.turn_motor('rm', 362)
        eigth = target_pos / 8
        three_quarters = target_pos * 3 / 4
        while self.rm.position < target_pos - 10:
            # print(self.rm.position)
            gs = self.cs.get_greyscale()
            if gs < 100:
                direction = self.position[2]
                if target_pos - 7 * eigth <= self.rm.position <= target_pos - 5 * eigth:
                    direction += Direction.EAST
                    # print('right path detected: ' + str(direction))
                elif target_pos - 5 * eigth <= self.rm.position <= target_pos - 3 * eigth:
                    direction += Direction.NORTH
                    # print('straight path detected: ' + str(direction))
                elif target_pos - 3 * eigth <= self.rm.position <= target_pos - 1 * eigth:
                    direction += Direction.WEST
                    # print('left path detected: ' + str(direction))
                else:
                    continue
                direction = direction % 360
                # print('path detected: ' + str(direction))
                self.events.set(EventNames.NEW_PATH, direction)
                time.sleep(0.5)
        self.events.set(EventNames.NEW_PATH, (self.position[2] + Direction.SOUTH) % 360)

        self.turn(90)

        self.events.reset(EventNames.NEW_PATH)
        self.mode = PilotModes.CHOOSE_PATH
        pass

    def choose_path(self):
        print('choose_path()')
        self.stop_motors()
        path = self.planet.get_next_path()
        turn_direction = self.position[2] - path.direction
        if turn_direction == 270:
            turn_direction = -90
        if turn_direction == -270:
            turn_direction = 90

        if turn_direction == -90:  # East (relative)
            self.lm.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
            self.rm.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
            time.sleep(1)
            self.turn(turn_direction)
        elif turn_direction == 0:  # North (relative)
            self.lm.run_to_rel_pos(position_sp=120, speed_sp=200, stop_action="hold")
            self.rm.run_to_rel_pos(position_sp=120, speed_sp=200, stop_action="hold")
        elif turn_direction == 90:  # West (relative)
            turn_direction = 90
            self.lm.run_to_rel_pos(position_sp=120, speed_sp=200, stop_action="hold")
            self.rm.run_to_rel_pos(position_sp=120, speed_sp=200, stop_action="hold")
            time.sleep(1)
            self.turn(turn_direction)
            self.lm.run_to_rel_pos(position_sp=100, speed_sp=200, stop_action="hold")
            self.rm.run_to_rel_pos(position_sp=100, speed_sp=200, stop_action="hold")
        elif turn_direction == 180 or turn_direction == -180:  # South (relative)
            self.lm.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
            self.rm.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
            time.sleep(1)
            self.turn(90)
            self.lm.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
            self.rm.run_to_rel_pos(position_sp=60, speed_sp=200, stop_action="hold")
            time.sleep(1)
            self.turn(90)
            self.lm.run_to_rel_pos(position_sp=100, speed_sp=200, stop_action="hold")
            self.rm.run_to_rel_pos(position_sp=100, speed_sp=200, stop_action="hold")

        time.sleep(2)

        self.mode = PilotModes.FOLLOW_LINE
        pass

    def test(self, value, value2):
        print('test()')
        self.lm.run_to_rel_pos(position_sp=value, speed_sp=200, stop_action="hold")
        self.rm.run_to_rel_pos(position_sp=value, speed_sp=200, stop_action="hold")
        time.sleep(0.5)
        self.turn(value2)
        pass

    # ---------
    # SETTER
    # ---------
    def set_position(self, value):
        # print(value)
        self.position = value

    def set_color(self, value):
        self.color = value
        self.rbd = value[0] - value[2]
        # gs = (value[0] + value[1] + value[2]) / 3
        # print('RBD: ' + str(self.rbd) + '  GS: ' + str(gs))
        if 90 <= self.rbd:       # red patch
            print('Patch: red')
            self.stop_motors()
            self.mode = PilotModes.CHECK_ISC
        elif self.rbd <= -65:    # blue patch
            print('Patch: blue')
            self.stop_motors()
            time.sleep(0.4)
            self.lm.run_to_rel_pos(position_sp=-35, speed_sp=180, stop_action="hold")
            time.sleep(0.1)
            self.mode = PilotModes.CHECK_ISC
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
