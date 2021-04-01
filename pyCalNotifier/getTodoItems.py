import configparser
import time
import caldav
from ics import Calendar


def getTodoItems(configFile, maxRetry=60, retryInterval=60):
    config = configparser.ConfigParser()
    config.read(configFile, encoding='utf-8')

    config_url = config["server"]["url"]
    config_calendarName = config["server"]["calendar"]
    config_user = config["server"]["user"]
    config_pw = config["server"]["pw"]

    retryCount = 0
    while(True):
        retryCount = retryCount + 1

        if retryCount > maxRetry:
            print("重试了%d次，都出问题了，自己想办法吧……" % retryCount)
            break

        try:

            # connection
            client = caldav.DAVClient(
                url=config_url, username=config_user, password=config_pw)

            # parse
            for calendar in client.principal().calendars():
                if calendar.name != config_calendarName:
                    continue

                AllTodos = calendar.todos()
                return [todo for todoSet in AllTodos for todo in Calendar(todoSet.data).todos]
        except:
            print("网络异常，%d秒后重试……" % retryInterval)
            time.sleep(retryInterval)

    return None
