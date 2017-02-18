import requests
import urllib
import re
from bot_plugins import AbstractPlugin


class Weather(AbstractPlugin.AbstractPlugin):
    API_URL = 'https://query.yahooapis.com/v1/public/yql?q={}&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'

    storage = None

    sender_id = None

    def __init__(self, storage, sender_id):
        self.storage = storage
        self.sender_id = sender_id

    def get_help_message(self):
        return 'Type location name and time of interest(now, tomorrow, day after tomorrow) splitted by | \n' \
               'Ex: Cambridge MA | now'

    def get_response(self, message):
        if self.validate_message(message):
            address, when = message.split('|')
            request_result = requests.get(self.build_url(address))
            result = self.format_output(request_result, when)
        else:
            result = self.get_help_message()
        return result

    def format_output(self, request_result, when):
        try:
            json_res = request_result.json()['query']['results']['channel']['item']['forecast']
            i = 0
            template = 'description: {text} \n' \
                       'high temp: {high} \n' \
                       'low temp: {low} \n'

            for forecast_item in json_res:
                if when.strip() == 'now' and i == 0:
                    formatted_output = template.format(**forecast_item)
                    break
                elif when.strip() == 'tomorrow' and i == 1:
                    formatted_output = template.format(**forecast_item)
                    break
                elif when.strip() == 'day after tomorrow' and i == 2:
                    formatted_output = template.format(**forecast_item)
                    break
                i += 1
        except Exception:
            formatted_output = 'No weather found for your location'
        return formatted_output

    def validate_message(self, message):
        # making sure we got 1 and only 1 pipe in message
        all_pipes = [m.start() for m in re.finditer('\|', message)]
        if len(all_pipes) == 1:
            return True
        return False

    def build_url(self, address):
        query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="' + \
                address.strip() + '")'
        url = self.API_URL.format(query)
        return url
