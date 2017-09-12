from bot_plugins.Recipe import Recipe
import unittest

recipe_plugin = Recipe()
response = recipe_plugin.get_response('chicken,eggs,potatos')
print(response)

class RecipePluginTest(unittest.TestCase):

    def test_success(self):
        recipe_plugin = Recipe()
        response = recipe_plugin.get_response('chicken,eggs,potatos')
        self.assertEqual(True, 'Crunchy Onion Chicken' in response)
        self.assertEqual(True, 'Stuffed Tomatoes Salad' in response)
        self.assertEqual(True, 'Chicken Tikka Burger' in response)


    def test_success_invalid_payload(self):
        recipe_plugin = Recipe()
        response = recipe_plugin.get_response('chickien')
        self.assertEqual(True, 'Nothing found for your ingredients :( Please try something else' in response)

if __name__ == '__main__':
    unittest.main()