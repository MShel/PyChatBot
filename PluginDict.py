from bot_plugins.Weather import Weather
from bot_plugins.Recipe import Recipe
from bot_plugins.Reminder import Reminder
from bot_plugins.Fortune import Fortune
from bot_plugins.Exit import Exit
from bot_plugins.StackOverflow import StackOverflow

# all plugins are singletones so we dont need to worry about multiply intialisation
pluginDict = {
    'weather': Weather(),

    'recipe': Recipe(),

    'reminder': Reminder(),

    'joke': Fortune(),

    'stackoverflow': StackOverflow(),

    'exit': Exit(),
}
