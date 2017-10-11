import requests
import urllib
from bot_plugins import AbstractPlugin


class DogPlugin(AbstractPlugin.AbstractPlugin):
    API_URL = 'https://dog.ceo/api/breed/{}/images/random'

    def get_help_message(self):
        return 'Type the name of a dog breed to get a random image of a dog you want to see.'

    def get_response(self, message):
        if self.validate_message(message):
            request_result = requests.get(self.build_url(message))
            result = self.format_output(request_result)
        else:
            result = self.get_help_message()
        return result

    def format_output(self, request_result):
        formatted_output = ''
        # Parse the response JSON
        try:
            resp_data = request_result.json()
        except Exception as exc:
            print('Failed to parse JSON response data. Exception: %s' % exc.message)
            return 'Oops, there was a problem looking up that dog breed. Please try something else.'

        try:
            # Check for error status
            if resp_data.get('status', '') != 'success':
                # Check for 404
                if resp_data.get('code', '') == '404':
                    print('Dog breed not found: %s' % request_result.request.url)
                else:
                    print('Error getting random dog image: %s' % request_result.request.url)
                    print('Error code: %s' % resp_data.get('code', 'None'))
                    print('Error message: %s' % resp_data.get('message', 'None'))
                raise ValueError('Not found')
            
            # Get the list of sub-breeds
            random_image_url = resp_data.get('message')
            if not random_image_url:
                raise ValueError('Not found')
            formatted_output += random_image_url
        except ValueError:
            formatted_output += 'Nothing found for that dog breed :( Please try something else'
        return formatted_output

    def build_url(self, message):
        message = urllib.parse.quote(message.replace(' ', ''))
        url = self.API_URL.format(message)
        return url

    def validate_message(self, message):
        return True
