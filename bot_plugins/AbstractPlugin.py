from abc import ABCMeta, abstractmethod

'''
all plugins should extend this class
and implement missing methods
'''
class AbstractPlugin:

    __metaclass__ = ABCMeta

    MESSAGE_MAX_TEXT_LEN = 640

    @abstractmethod
    def get_help_message(self): pass


    @abstractmethod
    def get_response(self, message): pass


    @abstractmethod
    def format_output(self): pass

    @abstractmethod
    def validate_message(self):pass