import configparser
import caldav
from ics import Calendar


def getTodoItems(configFile):
    config = configparser.ConfigParser()
    config.read(configFile, encoding='utf-8')

    config_url = config["server"]["url"]
    config_calendarName = config["server"]["calendar"]
    config_user = config["server"]["user"]
    config_pw = config["server"]["pw"]

    # connection
    client = caldav.DAVClient(
        url=config_url, username=config_user, password=config_pw)

    # parse
    for calendar in client.principal().calendars():
        if calendar.name != config_calendarName:
            continue

        AllTodos = calendar.todos()
        return [todo for todoSet in AllTodos for todo in Calendar(todoSet.data).todos]
