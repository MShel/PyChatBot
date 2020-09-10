import unittest
from config.Config import Config


class ConfigTest(unittest.TestCase):
    current_transports = ['Slack', 'Facebook']

    def test_singleton(self):
        self.config = Config()
        self.another_config = Config()
        self.assertEqual(self.config, self.another_config)

    def test_get_transports(self):
        self.config = Config()
        self.assertEqual(set(self.config.get_transports().keys()), set(self.current_transports))

    def test_get_redis_conf(self):
        self.config = Config()
        self.assertEqual(("127.0.0.1", "6379"), self.config.get_redis_conf())

    def test_get_static_path(self):
        self.config = Config()
        self.assertEqual("/static", self.config.get_static_path())


if __name__ == '__main__':
    unittest.main()
