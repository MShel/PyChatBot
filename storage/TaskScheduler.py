from celery import Celery
from celery import Task
from transport import AbstractTransport


class TaskScheduler():
    _instance = None

    QUEUE_NAME = 'bot_reminder'

    __initialized = None

    def __init__(self, host=None, port=None):
        self.celery = None
        #self.celery = Celery(self.QUEUE_NAME,
        #                     broker='redis://' + str(host) + ':' + str(port) + '/0')

    def add_delayed_message(self, delay_for, transport, what_to_remind):
        task = TaskToSchedue()
        task.transport = transport
        task.delay(delay_for, what_to_remind)



class TaskToSchedue(Task):
    ignore_result = True

    transport = None

    def run(self,  recipient_id, message):
        self.transport.send_message(recipient_id, message)
