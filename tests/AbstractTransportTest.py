import unittest
import Router
from pprint import pprint
from tests.RouterTest import DummyStorage
from mock import Mock
from transport.AbstractTransport import AbstractTransport
class Plugin:
    def get_help_message(self, *args):
        return('test')
    def get_response(self, *args):
        return('SPLIT EVERY FIVE WORDS')


class AbstractTransportTest(unittest.TestCase):

    def test_success_get_reply_message(self):
        abstract_transport  =  AbstractTransport()

        plugin = Plugin()
        storage = DummyStorage()
        abstract_transport.router = Router.Router(storage)
        abstract_transport.router.get_plugin = Mock(return_value = (plugin, True))
        abstract_transport.max_message_size = 5
        testResponse = abstract_transport.get_reply_message(1,'test')
        listToAssert = [];
        for char in testResponse:
            listToAssert.append(char)
        self.assertEqual(listToAssert,['SPLIT', ' EVER', 'Y FIV', 'E WOR', 'DS'])
if __name__ == '__main__':
    unittest.main()
