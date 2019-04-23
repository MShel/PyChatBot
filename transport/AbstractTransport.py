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
    max_message_size = 600

    @abstractmethod
    def get_help_message(self):
        pass

    @abstractmethod
    def get_response(self, message):
        pass

    @abstractmethod
    def send_message(self, sender_id, message):
        pass

    @abstractmethod
    def get_end_points_to_add(self):
        pass

    ##
    # returns generator over the message to reply paginated by self.max_message_size
    ##
    def get_reply_message(self, sender_id: str, message: str) -> Generator[str, None, None]:
        reply = 'Try one of those:\n ' + '\n'.join(self.router.get_available_plugins())
        try:
            plugin, initiated = self.router.get_plugin(message, sender_id, self.__class__.__name__)
            if plugin:
                plugin.transport = self
                if not initiated:
                    reply = plugin.get_help_message()
                else:
                    reply = plugin.get_response(message)
        except KeyError:
            reply = 'Something went wrong... nothing can be done with your request, Try something else.'
        except ValueError:
            reply = 'This plugin is not available on this platform'
        except:
            reply = 'This plugin do not want to play nice. Try something else'


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
