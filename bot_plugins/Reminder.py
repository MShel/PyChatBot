from bot_plugins import AbstractPlugin
from storage.Scheduler import Scheduler


class Reminder(AbstractPlugin.AbstractPlugin):
    def get_help_message(self):
        return 'Type for how long to delay in seconds split by | with message you want to receive after delay\n' \
               'your message after delay.\n' \
               'Ex. 3600 | call mom'

    def get_response(self, message):
        if self.validate_message(message):
            countdown, what_to_remind = message.split('|')
            scheduler = Scheduler()
            scheduler.add_delayed_message(int(countdown), self.transport, what_to_remind)
            result = 'Message scheduled'
        else:
            result = self.get_help_message()
        return result

    def format_output(self):
        pass

    def validate_message(self, message):
        result = True
        if "|" not in message:
            result = False
        return result
