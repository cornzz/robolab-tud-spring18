import unittest
from src.events import EventRegistry, EventList


class Emitter:
    def __init__(self, registry):
        self.list = EventList.EventList(registry)
        self.list.add('message')


class Receiver:
    def __init__(self, registry):
        self.message = None
        registry.register_event_handler('message', self.set_message)

    def set_message(self, value):
        self.message = value
        pass


class EventsTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = EventRegistry.EventRegistry()
        self.emitter = Emitter(self.registry)
        self.receiver = Receiver(self.registry)
        pass

    def test_message_to_receiver(self):
        message = 'Hello receiver!'
        # make sure receivers message is none
        self.assertIsNone(self.receiver.message)
        # fire event!
        self.emitter.list.set('message', message)
        # did message receive?
        self.assertEqual(self.receiver.message, message)
        pass


if __name__ == '__main__':
    unittest.main()
