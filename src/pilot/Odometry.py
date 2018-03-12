from typing import Tuple
from planet.Direction import Direction
from events.EventList import EventList
from events.EventNames import EventNames
import math

# constants
TRACK = 15.8
WHEEL_DIAMETER = 5.6
ECF = math.pi * WHEEL_DIAMETER / 360


class Odometry:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0
        self.heading = 0
        self.events = EventList()
        self.events.add(EventNames.POSITION)
        self.prev_mpos = (0, 0)
        pass

    def calc_pos1(self, motor_position: Tuple[int, int]):
        # print(motor_position)
        lec = motor_position[0] - self.prev_mpos[0]
        rec = motor_position[1] - self.prev_mpos[1]
        displacement = (lec + rec) * ECF / 2
        rotation = (lec - rec) * ECF / TRACK
        # print(rotation)
        self.prev_mpos = motor_position
        self.dx = self.dx + displacement * math.sin(self.heading + rotation / 2)
        self.dy = self.dy + displacement * math.cos(self.heading + rotation / 2)
        self.heading = self.heading + rotation
        heading = Direction.format(Direction.to_deg(self.heading))
        # print(self.dx, self.dy, heading, Direction.str(heading, True))
        return self.x, self.y, self.heading

    def add_pos(self):
        self.x += round(self.dx / 50)
        self.y += round(self.dy / 50)
        heading = Direction.format(Direction.to_deg(self.heading))
        self.events.set(EventNames.POSITION, (self.x, self.y, heading, Direction.str(heading, True)))
        self.dx = 0
        self.dy = 0


    # ---------
    # SETTER
    # ---------
    def set_vertex(self, position):
        # self.vertex = Planet
        pass


    # ---------
    # GETTER
    # ---------
    def read_in(self, motor_position):
        # print('odometry calculated')
        return self.calc_pos1(motor_position)

    def get_direction(self):
        return self.heading

    def get_position(self):
        return self.x, self.y

    def get_vertex(self):
        return self.vertex
