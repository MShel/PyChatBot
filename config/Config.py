import json
from collections import OrderedDict
import os


class Config:
    config_file_path = './config.json'

    _instance = None

    def __init__(self):
        self.config = self.load_configs()

    def load_configs(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path+'/config.json') as conf_file:
            config = json.load(conf_file, object_pairs_hook = OrderedDict)
        return config

    def get_transports(self):
        return self.config['transports']

    def get_redis_conf(self):
        return self.config['redis_host'], self.config['redis_port']

    def get_static_path(self):
        return self.config['static_path']

    # singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(
                cls, *args, **kwargs)
        return cls._instance
