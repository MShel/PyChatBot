import redis


class RedisAdapter:
    storage = None

    host = None

    port = None

    def __init__(self, host, port):
        if not self.storage:
            self.storage = redis.StrictRedis(host=host, port=int(port), db=0)

    def get_storage(self):
        return self.storage
