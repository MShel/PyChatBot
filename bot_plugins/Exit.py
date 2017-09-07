from bot_plugins import AbstractPlugin
import Router

class Exit(AbstractPlugin.AbstractPlugin):

    EXIT_MESSAGE = 'See you soon'

    def get_help_message(self):
        return self.get_response(None)

    def get_response(self, message):
        #later perhaps there will more stuff to cleanup..
        #TODO not a fan of calling Router even statically here
        self.storage.delete(Router.Router.get_redis_key(self.sender_id))
        return self.EXIT_MESSAGE

    def format_output(self, request_result):
        return request_result

    def validate_message(self, message):
        return True
