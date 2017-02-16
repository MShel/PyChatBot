import requests
import urllib


class Recipy:
    welcome_message = 'Type where and when now \n'

    storage = None

    sender_id = None

    def __init__(self, storage, sender_id):
        self.storage = storage
        self.sender_id = sender_id

    def get_help_message(self):
        return 'Type comma separated ingredients(meat,egg,potatos)\n' \
               'and get list of links in response'

    def get_response(self, message):
        url = 'http://www.recipepuppy.com/api/?i=' + urllib.quote(message.replace(' ','')) + '&p=1'
        request_recipe = requests.get('http://www.recipepuppy.com/api/?i=' + urllib.quote(message) + '&p=1')
        result = ''
        try:
       	    i = 0
            for result_recipe in request_recipe.json()['results']:
                result += '\n'
                result += result_recipe['title'].encode('utf-8') + ' - '
                result += result_recipe['href']
                i += 1
                if i > 3:
                    break
        except Exception:
	          result += 'Nothing found your ingredients :( Please try something else' 
        return result
