from celery import Celery
from celery import Task
from transport import AbstractTransport


class Scheduler(object):
    _instance = None

    QUEUE_NAME = 'bot_reminder'

    __initialized = None

    def __init__(self, host=None, port=None):
        self.celery = Celery(self.QUEUE_NAME,
                             broker='redis://' + str(host) + ':' + str(port) + '/0')

    def add_delayed_message(self, delayFor: int, transport: AbstractTransport, message: str):
        task = TaskToSchedue()
        task.delay(delayFor, transport, message)

    def __new__(cls, *args, **kwargs):
        if not cls.__initialized:
            cls.__init__(cls, *args, **kwargs)
            cls.__initialized = True
        return cls


class TaskToSchedue(Task):
    ignore_result = True

    def run(self, transport, recipient_id, message):
        transport.send_message(recipient_id, message)
