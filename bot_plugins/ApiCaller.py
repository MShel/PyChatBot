from bot_plugins import AbstractPlugin

'''
that is cool plugin that allows you to define API's 
for your user like if you have so
'''
class ApiCaller(AbstractPlugin.AbstractPlugin):

    def get_help_message(self):
        return self.get_response(None)

    def get_response(self, message):
        pass

    def get_my_commands(self):
        pass

    def get_command(self,*params):
        pass

    def add_command(self, url):
        pass

    def format_output(self, request_result):
        return True

    def validate_message(self, message):
        return True
