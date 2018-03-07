from events.EventNames import EventNames
from events.EventList import EventList
import ev3dev.ev3 as ev3


class TouchSensor:
    def __init__(self):
        self.ts1 = ev3.TouchSensor('in2')
        self.ts2 = ev3.TouchSensor('in3')
        self.events = EventList()
        self.events.add(EventNames.TOUCH)

    def read_in(self):
        value = self.ts1.value() or self.ts2.value()
        self.events.set(EventNames.TOUCH, value)
        return value
