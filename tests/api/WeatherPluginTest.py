from bot_plugins.Weather import Weather
import unittest


class WeatherPluginTest(unittest.TestCase):

    def test_success(self):
        weather_plugin = Weather()
        response = weather_plugin.get_response('Cambridge MA | now')
        self.assertEqual(True, 'high temp' in response)
        self.assertEqual(True, 'low temp' in response)
        self.assertEqual(True, 'description' in response)


    def test_success_invalid_payload(self):
        weather_plugin = Weather()
        response = weather_plugin.get_response('Cambridge')
        self.assertEqual(True, 'Type location name and time of interest' in response)

    def test_invalid_plugin(self):
        weather_plugin = Weather()
        response = weather_plugin.get_response('ddddYOyOQA1 | now')
        self.assertEqual(True, 'No weather found for your location' in response)

if __name__ == '__main__':
    unittest.main()