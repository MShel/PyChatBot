from bot_plugins import AbstractPlugin
import subprocess


class Fortune(AbstractPlugin.AbstractPlugin):

    FORTUNE_COMMAND = 'fortune -a'

    def get_help_message(self):
        return self.get_response(None)

    def get_response(self, message):
        fortune_command = self.FORTUNE_COMMAND
        output, err = subprocess.Popen(fortune_command, stdout=subprocess.PIPE, shell=True).communicate()
        result = self.format_output(output)
        return result

    def format_output(self, request_result):
        return request_result.decode('utf-8')

    def validate_message(self, message):
        return True
