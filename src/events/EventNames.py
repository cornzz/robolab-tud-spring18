from enum import unique, Enum


@unique
class EventNames(Enum):
    # sensors
    COLOR = 'COLOR'
    TOUCH = 'TOUCH'
    # odometry
    POSITION = 'POSITION'
    # pilot
    PILOT_MODE = 'PILOT_MODE'
    CURR_VERTEX = 'CURR_VERTEX'
    NEW_PATH = 'NEW_PATH'
    NEW_EDGE = 'NEW_EDGE'
    # shortest path
    SHORTEST_PATH = 'SHORTEST_PATH'
    # communication
    TARGET = 'TARGET'
