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
        return map_to_range(value, 0, 359.9999, 0, 3) * 90

    @staticmethod
    def to_deg(value):
        return (value / math.pi * 180) % 360


class ParseDirectionException(Exception):
    def __init__(self, value):
        self.message = 'Can not parse ' + str(value) + ' to Direction string'


def map_to_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
