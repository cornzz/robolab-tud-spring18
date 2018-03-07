from src.events.EventRegistry import EventRegistry
from src.events.EventList import EventList
import unittest


class Emitter:
    def __init__(self):
        self.list = EventList()
        self.list.add('message')


class Receiver:
    def __init__(self):
        self.message = None
        EventRegistry.instance().register_event_handler('message', self.set_message)

    def set_message(self, value):
        self.message = value
        pass


class EventsTestCase(unittest.TestCase):
    def setUp(self):
        self.emitter = Emitter()
        self.receiver = Receiver()
        pass

    def test_message_to_receiver(self):
        message = 'Hello receiver!'
        # make sure receivers message is none
        self.assertIsNone(self.receiver.message)
        # fire event!
        self.emitter.list.set('message', message)
        # did message receive?
        self.assertEqual(self.receiver.message, message)
        print(self.receiver.message)
        pass


if __name__ == '__main__':
    unittest.main()
