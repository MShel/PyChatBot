from Router import Router

test = Router()

weather, new = test.get_plugin('weather', '22')
print(weather.get_response('cambridge MA | now'))

recipe, new = test.get_plugin('recipe', '11')
result = recipe.get_response('cool,   egddd  g, potdasfdatoes')
print(result)

