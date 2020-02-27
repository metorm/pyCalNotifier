from os import listdir
from os.path import isfile, join
import os
import configparser
import pyCalNotifier
import datetime
import sys
from PIL import Image, ImageDraw, ImageFont

appDIR = os.path.dirname(__file__)
configPath = join(appDIR, 'config')

allConfigFiles = [f for f in listdir(
    configPath) if (isfile(join(configPath, f)) and f.endswith('.ini'))]

print("程序启动于", datetime.datetime.now())

for f in allConfigFiles:
    configFilePath = join(configPath, f)
    print("正在处理 ", configFilePath)
    events = pyCalNotifier.getTodoItems(configFilePath)
    print("目标日历中存在%d个项目" % len(events))

    config = configparser.ConfigParser()
    config.read(configFilePath, encoding='utf-8')

    outputType = pyCalNotifier.OutputTarget.fromString(
        config['output']['type'])
    print("输出配置：", outputType)

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
            content=pyCalNotifier.events2PlainText(events),
            retries=int(config['output']['em_retry']),
            retryInterval=int(config['output']['em_retry_interval']))

    elif outputType == pyCalNotifier.OutputTarget.PLAINTEXTFILE:
        with open(config['output']['fileTarget'], "w") as outputFile:
            outputFile.write(pyCalNotifier.events2PlainText(events))

    elif outputType == pyCalNotifier.OutputTarget.KDETODOLIST:
        with open(config['output']['fileTarget'], "w") as outputFile:
            # TODO: check current file to avoid unnecessary write
            outputFile.write(pyCalNotifier.events2KDETodoList(
                events, config["server"]["calendar"]))

    elif outputType == pyCalNotifier.OutputTarget.WINWALLPAPER:
        # get original wall paper
        inputImgPath = config['output']['wwp_path']
        with Image.open(inputImgPath) as img:
            imgWidth, imgHeight = img.size
            textToRender = pyCalNotifier.events2PlainText(events)

            tempDIR = os.environ['TEMP']
            tempImgPath = os.path.join(tempDIR, 'pyCalNotifier.png')
            tempLogPath = os.path.join(tempDIR, "pyCalNotifier.log")

            # check current file to avoid unnecessary write
            cacheOK = (os.path.exists(tempLogPath)
                       and os.path.exists(tempImgPath))
            if cacheOK:  # more check
                print("找到缓存文件 %s" % tempLogPath)
                with open(tempLogPath, 'r') as f:
                    logFileContent = f.read()
                    if not logFileContent == textToRender:
                        cacheOK = False

            if cacheOK:
                print("缓存匹配，未执行文件写入.")
            else:
                print("缓存不匹配，继续执行 ...")

                with open(tempLogPath, 'w') as f:
                    f.write(textToRender)

                draw = ImageDraw.Draw(img)
                ttfront = ImageFont.truetype(
                    'simhei.ttf', int(config['output']['wwp_font_size']))

                # compute the required space width
                textLines = textToRender.split('\n')
                textWidth = max([ttfront.getsize(s)[0] for s in textLines])

                # color
                hexTextColor = config['output']['wwp_text_color']
                textColor = tuple(
                    int(hexTextColor[i:i+2], 16) for i in (0, 2, 4))

                # the shadow block
                hexShadowColor = config['output']['wwp_shadow_color']
                shadowColor = tuple(
                    int(hexShadowColor[i:i+2], 16) for i in (0, 2, 4))
                overlay = Image.new('RGBA', img.size, shadowColor+(0,))
                # Create a context for drawing things on it.
                draw = ImageDraw.Draw(overlay)
                opacity = int(
                    255 * float(config['output']['wwp_shadow_opacity']))
                draw.rectangle(((imgWidth - textWidth - 10 - 10, 0),
                                (imgWidth, imgHeight)), fill=shadowColor+(opacity,))

                img = img.convert("RGBA")
                img = Image.alpha_composite(img, overlay)

                draw = ImageDraw.Draw(img)
                draw.text((imgWidth - textWidth - 10, 10),
                          textToRender, fill=textColor, font=ttfront)
                img.save(tempImgPath)
                import ctypes
                # SPI_... : fetched from winuser.h
                SPI_SETDESKWALLPAPER = 0x0014
                SPIF_UPDATEINIFILE = 0x0001
                ctypes.windll.user32.SystemParametersInfoW(
                    SPI_SETDESKWALLPAPER, 0, tempImgPath, SPIF_UPDATEINIFILE)
