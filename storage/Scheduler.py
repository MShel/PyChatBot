from celery import Celery
from storage.Redis import RedisAdapter
from celery import Task
from transport import AbstractTransport


class Scheduler:
    _instance = None

    QUEUE_NAME = 'bot_reminder'

    def __init__(self):
        self.celery = Celery(self.QUEUE_NAME,
                             broker='redis://' + RedisAdapter.host + ':' + str(RedisAdapter.port) + '/0')

    def add_delayed_message(self, delayFor: int, transport: AbstractTransport, message: str):
        task = TaskToSchedue()
        task.delay(delayFor, transport, message)

    # singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(
                cls, *args, **kwargs)
        return cls._instance


class TaskToSchedue(Task):
    ignore_result = True

    def run(self, transport, recipient_id, message):
        transport.send_message(recipient_id, message)
