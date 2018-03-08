from typing import Tuple
from planet.Direction import Direction
from events.EventList import EventList
from events.EventNames import EventNames
import math

# constants
TRACK = 15.8
WHEEL_DIAMETER = 5.6


class Odometry:
    def __init__(self):
        self.prev_pos = None
        self.curr_pos = None
        self.direction = None
        self.x = 0
        self.y = 0
        self.heading = 0
        self.events = EventList()
        self.events.add(EventNames.POSITION)
        pass

    def calc_pos2(self):
        lec = self.curr_pos[0] - self.prev_pos[0]
        rec = self.curr_pos[1] - self.prev_pos[1]
        rl = TRACK / (rec - lec) * lec
        rm = rl + TRACK / 2
        alpha = rec / (TRACK + rl)
        rotation = alpha / 2
        m = 2 * rm * math.sin(rotation)
        self.heading = self.heading + rotation
        self.x = self.x + m * math.cos(rotation)
        self.y = self.y + m * math.sin(rotation)
        x = round(self.x)
        y = round(self.y)
        self.events.set(EventNames.POSITION, (x, y, self.heading))
        return x, y, self.heading

    def calc_pos1(self):
        lec = self.curr_pos[0] - self.prev_pos[0]
        rec = self.curr_pos[1] - self.prev_pos[1]
        ecf = math.pi * WHEEL_DIAMETER / 360
        displacement = (lec + rec) * ecf / 2
        rotation = (lec - rec) * ecf / TRACK

        self.x = self.x + displacement * math.cos(self.heading + rotation / 2)
        self.y = self.y + displacement * math.sin(self.heading + rotation / 2)
        self.heading = self.heading + rotation
        x = round(self.x)
        y = round(self.y)
        heading = Direction.to_deg(self.heading)
        self.events.set(EventNames.POSITION, (x, y, heading))
        return x, y, heading

    # ---------
    # SETTER
    # ---------
    def set_position(self, position: Tuple[int, int]):
        self.prev_pos = self.curr_pos
        self.curr_pos = position

    def set_direction(self, lm, rm):
        pass

    def set_vertex(self, position):
        # self.vertex = Planet
        pass

    # ---------
    # GETTER
    # ---------
    def read_in(self):
        return self.calc_pos()

    def get_direction(self):
        return self.direction

    def get_vertex(self):
        return self.vertex
