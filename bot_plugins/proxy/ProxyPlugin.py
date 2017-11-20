from bot_plugins.AbstractPlugin import AbstractPlugin


class ProxyPlugin(AbstractPlugin):

    PROXIES_HASH_KEY = 'api_proxies_user_id_{}'
    initiated_action = None

    def get_help_message(self):
        return self.initiated_action.get_help_message()

    def get_user_api_proxies(self):
        return self.storage.hkeys(self.get_proxy_commands_key())

    def get_proxy_commands_key(self):
        return self.PROXIES_HASH_KEY.format(self.sender_id)