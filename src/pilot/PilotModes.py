from enum import unique, IntEnum


@unique
class PilotModes(IntEnum):
    FOLLOW_LINE = 0
    CHECK_ISC = 1
    CHOOSE_PATH = 2

    EXPLORE = 3
    TARGET = 4
