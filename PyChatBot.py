import sys
import json
import requests
from flask import Flask, request, url_for
import os
from storage import Redis
from config.config import Config
from Router import Router
import importlib

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

for transport_to_init in Config['transports']:
    module = __import__('transport.'+transport_to_init)
    transport_class = getattr(getattr(module, transport_to_init), transport_to_init)
    transport_instance = transport_class(app,router,*(Config['transports'][transport_to_init]).values())

if __name__ == '__main__':
    app.run(debug=True)
