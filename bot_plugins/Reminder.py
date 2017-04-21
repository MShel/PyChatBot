from bot_plugins import AbstractPlugin
from storage import Celery

class Reminder(AbstractPlugin.AbstractPlugin):

    storage = None

    sender_id = None

    def __init__(self, storage, sender_id):
        self.storage = storage
        self.sender_id = sender_id

    def get_help_message(self):
        return 'Type for how long to delay in seconds split by | with message you want to receive after delay\n' \
               'your message after delay.\n'\
               'Ex. 3600 | call mom'

    def get_response(self, message):
        if self.validate_message(message):
            countdown, what_to_remind = message.split('|')
            Celery.task_to_background.apply_async(args=[self.sender_id, what_to_remind], countdown=int(countdown))
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
