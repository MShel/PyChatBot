import unittest
import Router
from bot_plugins import Weather


class DummyStorage:
    to_return = None

    def get(self, *args):
        return self.to_return

    def set(self, *args):
        pass

    def setex(self, *args):
        pass


class RouterTest(unittest.TestCase):

    def test_success(self):
        storage = DummyStorage()
        test_router = Router.Router(storage)
        weather_plug = Weather.Weather()
        weather_plug.storage = storage
        weather_plug.sender_id = 1
        self.assertEqual(test_router.get_plugin('weather', 1, 'facebook'), (weather_plug, False))

    def test_success_initialised_plugin(self):
        storage = DummyStorage()
        storage.to_return = b'weather'
        test_router = Router.Router(storage)
        weather_plug = Weather.Weather()
        weather_plug.storage = storage
        weather_plug.sender_id = 1
        self.assertEqual(test_router.get_plugin('trash', 1, 'facebook'), (weather_plug, True))

    def test_invalid_plugin(self):
        storage = DummyStorage()
        test_router = Router.Router(storage)
        self.assertEqual(test_router.get_plugin('InvalidPlugin', 1, 'facebook'), (None, False))

    def test_get_available_plugins(self):
        storage = DummyStorage()
        test_router = Router.Router(storage)
        print(test_router.get_available_plugins())


if __name__ == '__main__':
    unittest.main()
