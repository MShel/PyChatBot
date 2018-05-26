import PluginDict


class Router:
    REDIS_KEY_ACTIVE_PLUGIN = 'pychatbot:active_plugin:%s'

    PLUGIN_EXPIRATION = 60000

    storage = None

    def __init__(self, storage):
        self.storage = storage

    def get_plugin(self, plugin_type, sender_id, transport_name):
        initiated = False
        plugin = None
        try:
            plugin = PluginDict.pluginDict[plugin_type]
        except KeyError:
            plugin_type = self.storage.get(self.get_redis_key(sender_id))
            if plugin_type:
                initiated = True
                plugin_type = plugin_type.decode('utf-8')
                plugin = PluginDict.pluginDict[plugin_type]
                if transport_name.title() not in plugin.get_supported_transports():
                    raise ValueError("This plugin is not supported for " + transport_name)
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