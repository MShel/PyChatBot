from bot_plugins.Weather import Weather
from bot_plugins.Recipe import Recipe
from bot_plugins.Fortune import Fortune
from bot_plugins.DogPlugin import DogPlugin
from bot_plugins.Exit import Exit
from bot_plugins.ApiCaller import ApiCaller
from bot_plugins.StackOverflow import StackOverflow

# all plugins are singletones so we dont need to worry about multiply intialisation,
# you can specify aliases here
pluginDict = {
    'weather': Weather(),
    'recipe': Recipe(),
    'joke': Fortune(),
    'dog': DogPlugin(),
    'stackoverflow': StackOverflow(),
    'exit': Exit(),
    # 'apicaller': ApiCaller()
}
