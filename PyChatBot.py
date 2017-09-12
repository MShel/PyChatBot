import sys
import json
import requests
from flask import Flask, request, url_for
import os
from storage import Redis
from Router import Router
import importlib
from flask_restful import Api
from collections import OrderedDict

Config = json.load(open('config/config.json'), object_pairs_hook=OrderedDict)
print(Config)
app = Flask(__name__, static_url_path=Config['static_path'])
storage = Redis.RedisAdapter().get_storage()
router = Router(storage)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))


def privacy(self, param1, param2):
    return self.app.send_static_file('privacy.html')


api = Api(app)

for transport_to_init in Config['transports']:
    module = __import__('transport.' + transport_to_init)
    transport_class = getattr(getattr(module, transport_to_init), transport_to_init)
    print((Config['transports'][transport_to_init]).values())
    transport_instance = transport_class(router, *(Config['transports'][transport_to_init]).values())
    module = __import__('transport.' + transport_to_init)
    end_point_name = transport_to_init + 'EndPoint'
    api_class = getattr(getattr(module, transport_to_init), end_point_name)
    for end_point in transport_instance.get_end_points_to_add():
        print(transport_instance.access_point_root + end_point)
        api.add_resource(api_class, transport_instance.access_point_root + end_point,
                         endpoint=transport_instance.access_point_root + end_point,
                         resource_class_kwargs={'fb': transport_instance, 'app': app})

        # print(transport_instance.access_point_root+'/<param1>')
        # app.add_url_rule('/<name>','index',view_func=transport_instance.as_view('test'), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
