from enum import unique, Enum


@unique
class EventNames(Enum):
    PILOT_MODE = 'PILOT_MODE'
    COLOR = 'COLOR'
    TOUCH = 'TOUCH'
