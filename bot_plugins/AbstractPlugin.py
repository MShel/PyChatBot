from abc import ABCMeta, abstractmethod
from config.Config import Config

'''
all plugins should extend this class
and implement missing methods
'''


class AbstractPlugin:
    __metaclass__ = ABCMeta

    _instance = None

    storage = None

    sender_id = None

    @abstractmethod
    def get_help_message(self): pass

    @abstractmethod
    def get_response(self, message): pass

    @abstractmethod
    def format_output(self, request_result): pass

    @abstractmethod
    def validate_message(self, message): pass

    def get_supported_transports(self) -> set:
        return set(Config().get_transports().keys())
    #
    # singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(
                cls, *args, **kwargs)
        return cls._instance
