from bot_plugins.Fortune import Fortune
import unittest

class FortunePluginTest(unittest.TestCase):

    def test_success(self):
        fortune_plugin = Fortune()
        response = fortune_plugin.get_response('test')
        print(response)

if __name__ == '__main__':
    unittest.main()