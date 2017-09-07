import unittest
import Router
from bot_plugins import Weather


class DummyStorage:
    def get(self):
        pass

    def set(self):
        pass

    def setex(self,*args):
        pass


class RouterTest(unittest.TestCase):
    def test_success(self):
        storage = DummyStorage()
        testRouter = Router.Router(storage)
        weatherPlug = Weather.Weather()
        weatherPlug.storage = storage
        weatherPlug.sender_id = 1
        self.assertEqual(testRouter.get_plugin('weather', 1), (weatherPlug,False))


if __name__ == '__main__':
    unittest.main()
