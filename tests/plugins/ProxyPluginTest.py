from bot_plugins.proxy.ProxyPlugin import ProxyPlugin
from bot_plugins.proxy.Add import Add
from storage.Redis import RedisAdapter
def setup_plug(plug):
    plug.storage = storage
    plug.sender_id = 's123rfw1'

# storage = RedisAdapter('127.0.0.1', 6379).get_storage()
# test_plug = ProxyPlugin()
# add_plug = Add()
# setup_plug(test_plug)
# setup_plug(add_plug)
#
# add_plug.set_name('testing')
# add_plug.set_url('testing', 'http://testing')
# print(test_plug.get_user_api_proxies())



