from enum import unique, IntEnum


@unique
class PilotModes(IntEnum):
    # low-level modes
    FOLLOW_LINE = 0
    CHECK_ISC = 1
    CHOOSE_PATH = 2
    FOLLOW_LINE_ODO = 5
    BLOCKED = 6

    # top-level modes
    EXPLORE = 3
    TARGET = 4
