from enum import Enum, unique


@unique
class OutputTarget(Enum):
    # simply display the message
    SCREEN = 'Screen'

    # email todos to a email box via smtp
    EMAIL = 'Email'

    # write todos to a plain text file
    PLAINTEXTFILE = 'PlainTextFile'

    # write content to KDE TodoList widget
    # see https://github.com/Zren/plasma-applet-todolist
    KDETODOLIST = 'KDETodoList'

    # render text on windows desktop wallpaper
    WINWALLPAPER = 'WinWallPaper'

    @staticmethod
    def fromString(str):
        if str.lower() == 'screen':
            return OutputTarget.SCREEN
        elif str.lower() == 'email':
            return OutputTarget.EMAIL
        elif str.lower() == 'plaintextfile':
            return OutputTarget.PLAINTEXTFILE
        elif str.lower() == 'kdetodolist':
            return OutputTarget.KDETODOLIST
        elif str.lower() == 'winwallpaper':
            return OutputTarget.WINWALLPAPER
        else:
            raise NotImplementedError
