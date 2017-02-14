import requests
import urllib


class Weather:
    welcome_message = 'Type where and when now \n'

    storage = None

    sender_id = None

    def __init__(self, storage, sender_id):
        self.storage = storage
        self.sender_id = sender_id

    def get_help_message(self):
        return 'Type location name and time of interest(now, tomorrow, day after tomorrow) splitted by | \n' \
               'Ex: Cambridge MA | now'

    def get_response(self, message):
        if message.find('|') != -1:
            address, when = message.split('|');
            query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="' + \
                    address.strip() + '")'

            http_query = 'https://query.yahooapis.com/v1/public/yql?q=' + urllib.quote(
                query) + '&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
            request_weather = requests.get(http_query)
            reply = request_weather.json()['query']['results']['channel']['item']['forecast']
            i = 0
            result = ''
            for forecast_item in reply:
                if when.strip() == 'now' and i == 0:
                    result = self.get_forecast_output(forecast_item)
                    break
                elif when.strip() == 'tomorrow' and i == 1:
                    result = self.get_forecast_output(forecast_item)
                    break
                elif when.strip() == 'day after tomorrow)' and i == 2:
                    result = self.get_forecast_output(forecast_item)
                    break
                i += 1
        else:
            result = self.get_help_message()
        return result

    def get_forecast_output(self, item):
        result = ''
        result += 'description: ' + item['text'] + '\n'
        result += 'high temp: ' + item['high'] + '\n'
        result += 'low temp: ' + item['low'] + '\n'
        return result;
