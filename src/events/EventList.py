from .Event import Event


class EventList:
    def __init__(self, registry):
        self.registry = registry
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
                    self.registry.notify_all_handlers(event)
