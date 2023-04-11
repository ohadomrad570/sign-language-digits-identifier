import utils
import consts

class PathNotValid(Exception):
    def __init__(self, msg):
        self.message = utils.wrapper_message_brackets(consts.ERROR) + consts.SPACE + msg
    def __str__(self):
        return self.message