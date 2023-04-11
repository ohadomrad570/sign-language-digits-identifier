import logging
ZIP_EXTENTION = 'zip'
LOG_FILE_PATH = '../../../logs/system.log'
LOGGING_LEVEL = logging.DEBUG
INFO = 'INFO'
ERROR = 'ERRPR'
DEBUG = 'DEBUG'
SPACE = ' '
LOGS_PREFIX = {
    INFO: '[{0}]'.format(INFO),
    ERROR: '[{0}]'.format(ERROR),
    DEBUG: '[{0}]'.format(DEBUG),
}