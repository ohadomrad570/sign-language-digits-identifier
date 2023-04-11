import logging
import consts
logging.basicConfig(filename=consts.LOG_FILE_PATH,
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(consts.LOGGING_LEVEL)