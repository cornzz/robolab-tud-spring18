from src.events.EventHandler import EventHandler
from src.events.Singleton import Singleton


@Singleton
class EventRegistry:
    def __init__(self):
        self.handlers = []
        pass

    def register_event_handler(self, name, listener):
        handler = EventHandler(name, listener)
        if handler in self.handlers:
            return
        self.handlers.append(handler)
        return lambda: self.remove_event_handler(handler)

    def notify_all_handlers(self, event):
        for handler in self.handlers:
            if handler.name is event.name:
                handler.listener(event.value)

    def remove_event_handler(self, handler):
        self.handlers.remove(handler)
        pass
