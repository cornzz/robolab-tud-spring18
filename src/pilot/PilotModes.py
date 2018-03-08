from enum import unique, IntEnum


@unique
class PilotModes(IntEnum):
    FOLLOW_LINE = 0
    FOLLOW_LINE_ODO = 1
    CHECK_ISC = 2
