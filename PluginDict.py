from bot_plugins.Weather import Weather
from bot_plugins.Recipe import Recipe
from bot_plugins.Reminder import Reminder
from bot_plugins.Fortune import Fortune
from bot_plugins.Exit import Exit
from bot_plugins.StackOverflow import StackOverflow

#all plugins are singletones so we dont need to worry about multiply intialisation
pluginDict = {
    'weather': Weather(),
    'погода': Weather(),
    'weath': Weather(),

    'recipe': Recipe(),
    'рецепты': Recipe(),
    'rcp': Recipe(),

    'reminder': Reminder(),
    'напоминание': Reminder(),
    'remind': Reminder(),

    'шутка': Fortune(),
    'joke': Fortune(),
    'fortune': Fortune(),
    'sad': Fortune(),

    'stack':StackOverflow(),
    'stackoverflow': StackOverflow(),
    'so': StackOverflow(),

    'exit': Exit(),
    'выход': Exit()
}