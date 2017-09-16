from bot_plugins.Fortune import Fortune
import unittest

class FortunePluginTest(unittest.TestCase):

    def test_success(self):
        recipe_plugin = Fortune()
        response = recipe_plugin.get_response('test')
        print(response)

if __name__ == '__main__':
    unittest.main()