from bot_plugins import Weather
from bot_plugins import Recipe
from bot_plugins import Reminder
from bot_plugins import Fortune
from bot_plugins import Exit
from pprint import pprint

#all plugins are singletones so we dont need to worry about multiply intialisation
pluginDict = {
    'weather': Weather.Weather(),
    'погода': Weather.Weather(),
    'weath': Weather.Weather(),

    'recipe': Recipe.Recipe(),
    'рецепты': Recipe.Recipe(),
    'rcp': Recipe.Recipe(),

    'reminder': Reminder.Reminder(),
    'напоминание': Reminder.Reminder(),
    'remind': Reminder.Reminder(),

    'шутка': Reminder.Reminder(),
    'joke': Reminder.Reminder(),
    'fortune': Reminder.Reminder(),
    'sad': Fortune.Fortune(),

    'exit': Exit.Exit(),
    'выход': Exit.Exit()
}

pprint(pluginDict)
