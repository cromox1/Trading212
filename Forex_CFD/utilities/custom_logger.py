__author__ = 'cromox'

import inspect
import logging
import datetime

def customLogger(logLevel=logging.DEBUG):
    # Gets the name of the class / method from where this method is called
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)
    # By default, log all messages
    logger.setLevel(logging.DEBUG)

    minitni = datetime.datetime.now().strftime("%M")
    if int(minitni) < 5:
        minitni = '00'
    elif  int(minitni) > 4 and int(minitni) < 10:
        minitni = '05'
    else:
        minitni = int(int(minitni) / 5 ) * 5

    masani = datetime.datetime.now().strftime("%Y%m%d_%H")
    fileHandler = logging.FileHandler("logs\\automation_" + masani + str(minitni) + "00.log", mode='a')
    fileHandler.setLevel(logLevel)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger
