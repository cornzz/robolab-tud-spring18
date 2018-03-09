from enum import unique, IntEnum
import math


@unique
class Direction(IntEnum):
    """ Directions in degrees """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270

    @staticmethod
    def str(value, flag):
        value = int(value)
        if value == Direction.NORTH:
            if flag:
                return 'NORTH'
            return 'N'
        elif value == Direction.EAST:
            if flag:
                return 'EAST'
            return 'E'
        elif value == Direction.SOUTH:
            if flag:
                return 'SOUTH'
            return 'S'
        elif value == Direction.WEST:
            if flag:
                return 'WEST'
            return 'W'
        else:
            raise ParseDirectionException(value)

    @staticmethod
    def format(value):
        if 315 <= value <= 360 or 0 <= value <= 45:
            value = 0
        elif 45 <= value <= 135:
            value = 90
        elif 135 <= value <= 225:
            value = 180
        elif 225 <= value <= 315:
            value = 270
        else:
            raise DirectionOutOfBoundException(value)
        return value

    @staticmethod
    def to_deg(value):
        return (value / math.pi * 180) % 360


class ParseDirectionException(Exception):
    def __init__(self, value):
        self.message = 'Can not parse ' + str(value) + ' to Direction string'


class DirectionOutOfBoundException(Exception):
    def __init__(self, value):
        pass


def map_to_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
