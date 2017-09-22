import requests
import urllib
from bot_plugins import AbstractPlugin
import bleach


class StackOverflow(AbstractPlugin.AbstractPlugin):
    SEARCH_API_URL = 'https://api.stackexchange.com/2.2/search/advanced?pagesize=1&order=desc&sort=relevance&body={}&wiki=False&site=stackoverflow'

    ANSWER_API_URL = 'https://api.stackexchange.com/2.2/answers/{}?order=desc&sort=votes&site=stackoverflow&filter=withbody'

    KEY = None

    def get_help_message(self):
        return 'Type your question \n' \
               'And smartPython will get you an answer and link to an answer back'

    def get_response(self, message):
        if self.validate_message(message):
            request_result = self.get_stack_overflow_answer(message)
            result = self.format_output(request_result)
        else:
            result = self.get_help_message()
        return result

    def get_stack_overflow_answer(self, url):
        search_api_response = {'items': None}
        search_api_response = {**search_api_response,**requests.get(self.build_url(url, self.SEARCH_API_URL)).json()}
        answer = ''
        if search_api_response['items'] and search_api_response['items'][0]['is_answered'] == True:
            answer += search_api_response['items'][0]['title'] + '\n'
            answer += self._get_an_answer(search_api_response['items'][0]['accepted_answer_id']) + '\n'
            answer += search_api_response['items'][0]['link']
        else:
            answer = 'Nothing found for your question:('
        return answer

    def _get_an_answer(self, id):
        answer_api_response = requests.get(self.build_url(id, self.ANSWER_API_URL)).json()
        return answer_api_response['items'][0]['body']

    def format_output(self, request_result):
        formatted_output = bleach.clean(request_result, tags=[], attributes={}, styles=[], strip=True)
        return formatted_output

    def build_url(self, message, url_to_format):
        message = str(message)
        message = urllib.parse.quote(message)
        url = url_to_format.format(message)
        if self.KEY:
            url += '&key=' + self.KEY
        return url

    def validate_message(self, message):
        return True
