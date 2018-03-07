from enum import unique, IntEnum


@unique
class PilotModes(IntEnum):
    FOLLOW_LINE = 0
    HOVER_PATH = 1
    CHECK_ISC = 2
