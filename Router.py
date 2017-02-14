from bot_plugins import YahooWeather
from bot_plugins import Recipy
from storage import Redis


class Router:
    # key to store which plugin user is using
    REDIS_KEY_ACTIVE_PLUGIN = 'pychatbot:active_plugin:%senderid%'

    # how long do we have plugin activated thats ms
    PLUGIN_EXPIRATION = 60000

    storage = None

    def __init__(self):
        self.storage = Redis.RedisAdapter().get_storage()

    def get_plugin(self, plugin_type, sender_id):
        initiated = False
        plugin = None
        if plugin_type == 'weather':
            plugin = YahooWeather.Weather(self.storage, sender_id)
        elif plugin_type == 'recipe':
            plugin = Recipy.Recipy(self.storage, sender_id)
        if not plugin and plugin_type != 'exit':
            plugin_type = self.storage.get(self.get_redis_key(sender_id))
            if plugin_type:
                initiated = True
                plugin, false_init = self.get_plugin(plugin_type, sender_id)
            else:
                plugin = None
        if plugin:
            self.storage.setex(self.get_redis_key(sender_id), self.PLUGIN_EXPIRATION, plugin_type)
        return plugin, initiated

    def get_redis_key(self, sender_id):
        return self.REDIS_KEY_ACTIVE_PLUGIN.replace('%senderid%', sender_id)

    def get_available_plugins(self):
        return ['recipe', 'weather']
