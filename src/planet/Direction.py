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
    def str(value):
        if value == Direction.NORTH:
            return 'N'
        elif value == Direction.EAST:
            return 'E'
        elif value == Direction.SOUTH:
            return 'S'
        elif value == Direction.WEst:
            return 'W'
        else:
            raise ParseDirectionException(value)

    @staticmethod
    def format(value):
        if 315 <= value <= 45:
            value = 0
        if 45 <= value <= 135:
            value = 90
        if 135 <= value <= 225:
            value = 180
        if 225 <= value <= 315:
            value = 270
        return value

    @staticmethod
    def to_deg(value):
        return (value / math.pi * 180) % 360


class ParseDirectionException(Exception):
    def __init__(self, value):
        self.message = 'Can not parse ' + str(value) + ' to Direction string'


def map_to_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
