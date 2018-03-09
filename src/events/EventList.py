from .Event import Event
from .EventRegistry import EventRegistry


class EventList:
    def __init__(self):
        self.events = []

    def add(self, name):
        event = Event(name, None)
        for e in self.events:
            if e.name is event.name:
                return
        self.events.append(event)
        return self

    def set(self, name, value):
        for event in self.events:
            if event.name == name:
                if event.value != value:
                    event.value = value
                    EventRegistry.instance().notify_all_handlers(event)

    def reset(self, name):
        for event in self.events:
            if event.name == name:
                event.value = None
