from os import listdir
from os.path import isfile, join
import configparser
import pyCalNotifier

configPath = 'config'

allConfigFiles = [f for f in listdir(
    configPath) if (isfile(join(configPath, f)) and f.endswith('.ini'))]

for f in allConfigFiles:
    configFilePath = join(configPath, f)
    print("正在处理 ", configFilePath)
    events = pyCalNotifier.getTodoItems(configFilePath)
    print("目标日历中存在%d个项目" % len(events))

    config = configparser.ConfigParser()
    config.read(configFilePath)

    outputType = pyCalNotifier.OutputTarget.fromString(
        config['output']['type'])

    if outputType == pyCalNotifier.OutputTarget.SCREEN:
        print(pyCalNotifier.events2PlainText(events))
    elif outputType == pyCalNotifier.OutputTarget.EMAIL:
        pyCalNotifier.emailBySMTP(
            host=config['output']['em_host'],
            port=int(config['output']['em_port']),
            user=config['output']['em_user'],
            pw=config['output']['em_pw'],
            sender=config['output']['em_sender'],
            receivers=config['output']['em_receivers'].split('!'),
            content=pyCalNotifier.events2PlainText(events))
    elif outputType == pyCalNotifier.OutputTarget.FILE:
        with open(config['output']['fileTarget'], "w") as outputFile:
            outputFile.write(pyCalNotifier.events2PlainText(events))
