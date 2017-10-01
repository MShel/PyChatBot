import requests
import urllib
from bot_plugins import AbstractPlugin


class DogPlugin(AbstractPlugin.AbstractPlugin):
    API_URL = 'https://dog.ceo/api/breed/{}/list'

    def get_help_message(self):
        return 'Type the name of a dog breed to get a list of sub-breeds.'

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
                    print('Error getting dog breed: %s' % request_result.request.url)
                    print('Error code: %s' % resp_data.get('code', 'None'))
                    print('Error message: %s' % resp_data.get('message', 'None'))
                raise ValueError('Not found')
            
            # Get the list of sub-breeds
            sub_breeds = resp_data.get('message', [])
            if not len(sub_breeds):
                raise ValueError('Not found')
            formatted_output += 'I found %s sub-breeds:\n' % len(sub_breeds)
            formatted_output += '\n'.join(sub_breeds)
        except ValueError:
            formatted_output += 'Nothing found for that dog breed :( Please try something else'
        return formatted_output

    def build_url(self, message):
        message = urllib.parse.quote(message.replace(' ', ''))
        url = self.API_URL.format(message)
        return url

    def validate_message(self, message):
        return True
