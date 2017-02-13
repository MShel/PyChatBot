import redis


class RedisAdapter:

    storage = None

    def __init__(self):
        if not self.storage:
            self.storage = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    def get_storage(self):
        return self.storage