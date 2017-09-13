import redis


class RedisAdapter:

    storage = None

    host = '127.0.0.1'

    port = 6379

    def __init__(self):
        if not self.storage:
            self.storage = redis.StrictRedis(host=self.host, port=self.port, db=0)

    def get_storage(self):
        return self.storage