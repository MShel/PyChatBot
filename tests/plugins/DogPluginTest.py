from bot_plugins.DogPlugin import DogPlugin
import unittest

class DogPluginTest(unittest.TestCase):

    def test_success(self):
        dog_plugin = DogPlugin()
        response = dog_plugin.get_response('beagle')
        self.assertEqual(True, 'breeds/beagle' in response)

    def test_failure(self):
        dog_plugin = DogPlugin()
        response = dog_plugin.get_response('1beagle')
        self.assertEqual("Nothing found for that dog breed :( Please try something else",response)


if __name__ == '__main__':
    unittest.main()