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
        self.x = 0
        self.y = 0
        self.heading = 0
        self.events = EventList()
        self.events.add(EventNames.POSITION)
        pass

    def calc_pos2(self, motor_position):
        lec = motor_position[0]
        rec = motor_position[1]
        print(motor_position)
        rl = TRACK / (rec - lec) * lec
        rm = rl + TRACK / 2
        alpha = rec / (TRACK + rl)
        rotation = alpha / 2
        print(rotation)
        m = 2 * rm * math.sin(rotation)
        print(m)
        self.heading = self.heading + rotation
        dx = m * math.cos(rotation)
        dy = m * math.sin(rotation)
        print(dx, dy)
        self.x = self.x + round(dx / 50)
        self.y = self.y + round(dy / 50)
        self.events.set(EventNames.POSITION, (self.x, self.y, self.heading))
        return self.x, self.y, self.heading

    def calc_pos1(self, motor_position: Tuple[int, int]):
        # print(motor_position)
        lec = motor_position[0]
        rec = motor_position[1]
        displacement = (lec + rec) * ECF / 2
        rotation = (lec - rec) * ECF / TRACK
        # print(rotation)
        dx = displacement * math.cos(self.heading + rotation / 2)
        dy = displacement * math.sin(self.heading + rotation / 2)
        self.x = self.x + dx
        self.y = self.y + dy
        x = round(self.x / 50)
        y = round(self.y / 50)
        self.heading = self.heading + rotation
        heading = Direction.to_deg(self.heading)
        self.events.set(EventNames.POSITION, (x, y, heading))
        return x, y, self.heading

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
        return self.calc_pos1(motor_position)

    def get_direction(self):
        return self.heading

    def get_position(self):
        return self.x, self.y

    def get_vertex(self):
        return self.vertex
