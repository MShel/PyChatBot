import unittest
import Router
from bot_plugins import Weather
from mock import Mock

class DummyStorage:
    def get(self, *args):
        pass
    def set(self, *args):
        pass
    def setex(self, *args):
        pass


class RouterTest(unittest.TestCase):

    def test_success(self):
        storage = DummyStorage()
        testRouter = Router.Router(storage)
        weatherPlug = Weather.Weather()
        weatherPlug.storage = storage
        weatherPlug.sender_id = 1
        self.assertEqual(testRouter.get_plugin('weather', 1), (weatherPlug,False))

    def test_success_initialised_plugin(self):
        storage = DummyStorage()
        storage.get = Mock()
        storage.get.return_value = 'weather'
        testRouter = Router.Router(storage)
        weatherPlug = Weather.Weather()
        weatherPlug.storage = storage
        weatherPlug.sender_id = 1
        self.assertEqual(testRouter.get_plugin('trash', 1), (weatherPlug, True))

    def test_invalid_plugin(self):
        storage = DummyStorage()
        testRouter = Router.Router(storage)
        self.assertEqual(testRouter.get_plugin('InvalidPlugin', 1), (None,False))

    def test_get_available_plugins(self):
        storage = DummyStorage()
        testRouter = Router.Router(storage)
        print(testRouter.get_available_plugins())

if __name__ == '__main__':
    unittest.main()
