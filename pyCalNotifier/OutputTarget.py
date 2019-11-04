from enum import Enum, unique


@unique
class OutputTarget(Enum):
    SCREEN = 'screen'
    EMAIL = 'email'
    FILE = 'file'

    @staticmethod
    def fromString(str):
        if str.lower() == 'screen':
            return OutputTarget.SCREEN
        elif str.lower() == 'email':
            return OutputTarget.EMAIL
        elif str.lower() == 'file':
            return OutputTarget.FILE
        else:
            raise NotImplementedError
