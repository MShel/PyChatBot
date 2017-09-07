import requests
import urllib
from bot_plugins import AbstractPlugin
import subprocess


class Fortune(AbstractPlugin.AbstractPlugin):

    #command to run to get fortune %s stays for max amount of characters that fortune should have
    FORTUNE_COMMAND = 'fortune -a -n %s'

    def get_help_message(self):
        return self.get_response(None)

    def get_response(self, message):
        fortune_command = self.FORTUNE_COMMAND % str(self.MESSAGE_MAX_TEXT_LEN)
        output, err = subprocess.Popen(fortune_command, stdout=subprocess.PIPE, shell=True).communicate()
        result = self.format_output(output)
        return result

    def format_output(self, request_result):
        return request_result

    def validate_message(self, message):
        return True
