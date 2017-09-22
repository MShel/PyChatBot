from bot_plugins.Reminder import Reminder
import unittest
from transport.AbstractTransport import AbstractTransport

class ReminderPluginTest(unittest.TestCase):

    def test_success(self):
        reminder_plugin = Reminder()
        transport = AbstractTransport()
        reminder_plugin.transport = transport
        response = reminder_plugin.get_response('5|test')

if __name__ == '__main__':
    unittest.main()