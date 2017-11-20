from bot_plugins.proxy.ProxyPlugin import ProxyPlugin


class Add(ProxyPlugin):

    IN_PROGRESS_STATUS = 'need_setup'

    INSTALLED_STATUS = 'installed'

    storage = None

    _instance = None

    def set_name(self, api_name, status='need_setup'):
        self.storage.hset(self.get_proxy_commands_key(), api_name, status)

    def set_url(self, api_name, url):
        self.storage.set(self.get_api_url_key(api_name), url)
        self.set_name(api_name, self.INSTALLED_STATUS)

    def get_api_url_key(self, command_name):
        return self.PROXIES_HASH_KEY.format(self.sender_id) + '_' + command_name

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(
                cls, *args, **kwargs)
        return cls._instance
