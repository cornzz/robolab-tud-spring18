from enum import unique, IntEnum


@unique
class Direction(IntEnum):
    """ Directions in degrees """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270
