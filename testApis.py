try:
    from Router import Router
    test = Router()
except ImportError:
    pass

weather, new = test.get_plugin('weather', '22')
print(weather.get_response('cambridge MA | now'))

recipe, new = test.get_plugin('recipe', '11')
result = recipe.get_response('egg,potatos,vodka')
print(result)

joke, new = test.get_plugin('joke', '11')
result = joke.get_response('1')
print(result)

reminder, new = test.get_plugin('reminder', '22')
print(reminder.get_response('2 | whatsUP!!!'))
