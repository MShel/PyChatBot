from abc import ABCMeta, abstractmethod

'''
all transports should extend this class
and implement missing methods
'''
from typing import Generator


class AbstractTransport:
    __metaclass__ = ABCMeta

    app = None

    router = None

    # 100 chars as max size message
    max_message_size = 100

    @abstractmethod
    def get_help_message(self):
        pass

    # we use this method to add nesesary method to flask app
    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def get_response(self, message):
        pass

    @abstractmethod
    def send_message(self, message):
        pass

    ##
    # returns generator over the message to repply paginated by self.max_message_size
    ##
    def get_reply_message(self, sender_id: str, message: str) -> Generator[str, None, None]:
        reply = 'Try one of those:\n ' + '\n'.join(self.router.get_available_plugins())
        plugin, initiated = self.router.get_plugin(message, sender_id)
        if plugin:
            if not initiated:
                reply = plugin.get_help_message()
            else:
                reply = plugin.get_response(message)

        def replySplitter(reply):
            returnYeild = ''
            for char in reply:
                if len(returnYeild) < self.max_message_size:
                    returnYeild += char
                else:
                    returnVal = returnYeild
                    returnYeild = char
                    yield returnVal
            yield returnYeild

        return replySplitter(reply)
