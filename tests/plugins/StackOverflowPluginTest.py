from bot_plugins.StackOverflow import StackOverflow
import unittest

class StackOverflowPluginTest(unittest.TestCase):

    def test_success(self):
        stack_plugin = StackOverflow()
        response = stack_plugin.get_response('pip install')
        self.assertEqual(True, 'pip install git' in response)

    def test_invalid_payload(self):
        stack_plugin = StackOverflow()
        response = stack_plugin.get_response('YOYO 111')
        self.assertEqual(True, 'Nothing found for your question:(' in response)

if __name__ == '__main__':
    unittest.main()