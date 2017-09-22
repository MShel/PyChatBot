import PluginDict


class Router:
    # key to store which plugin user is using
    REDIS_KEY_ACTIVE_PLUGIN = 'pychatbot:active_plugin:%s'

    # how long do we have plugin activated thats ms
    PLUGIN_EXPIRATION = 60000

    storage = None

    def __init__(self, storage):
        self.storage = storage

    def get_plugin(self, plugin_type, sender_id):
        initiated = False
        plugin = None
        plugin_type = plugin_type
        sender_id = sender_id
        try:
            plugin = PluginDict.pluginDict[plugin_type]
        except KeyError:
            plugin_type = self.storage.get(self.get_redis_key(sender_id))
            if plugin_type:
                initiated = True
                plugin_type = plugin_type.decode('utf-8')
                plugin = PluginDict.pluginDict[plugin_type]
        if plugin:
            self.storage.setex(self.get_redis_key(sender_id), self.PLUGIN_EXPIRATION, plugin_type)
            plugin.storage = self.storage
            plugin.sender_id = sender_id

        return plugin, initiated

    @staticmethod
    def get_redis_key(sender_id):
        return Router.REDIS_KEY_ACTIVE_PLUGIN % str(sender_id)

    @staticmethod
    def get_available_plugins():
        return PluginDict.pluginDict.keys()