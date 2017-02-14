import sys
import json
import urllib
import requests
from bot_plugins import YahooWeather
from Router import Router
from flask import Flask, request

'''
'''


def get_reply_message(user_message):
    weather = YahooWeather.Weather()
    if user_message["message"]["text"].lower() == 'random recipe':
        request_recipe = requests.get('http://www.recipepuppy.com/api/?i=onions,garlic,meat,eggs&q=omelet&p=3')
        reply = request_recipe.json()['results'][0]['title']
    elif user_message["message"]["text"].lower().find('weather at') != -1:
        query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="' + \
                user_message["message"]["text"].lower().replace('weather at',
                                                                '') + '")'
        http_query = 'https://query.yahooapis.com/v1/public/yql?q=' + urllib.quote(
            query) + '&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
        print(http_query)
        request_weather = requests.get(http_query)
        reply = request_weather.json()['query']['results']['channel']['item']['forecast'][0]["text"]
    else:
        reply = 'atata'
    return reply


test = Router()
weather, new = test.get_plugin('weather', '22')
print(weather.get_response('cambridge MA | now'))
#print(recipe.get_response('weather at cambridge'))
