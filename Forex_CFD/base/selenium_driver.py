__author__ = 'cromox'

from traceback import print_stack
import Forex_CFD.utilities.custom_logger as cl
import logging
import datetime
import os

class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        masani = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        # fileName = resultMessage + "." + str(round(time.time()*1000)) + ".png"
        fileName = resultMessage.replace(" ","_").replace("/","_").replace("-","_") + "_" + masani + ".png"
        screenshotDirectory = "..\\screenshots\\"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)
        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occured when taking screenshot")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def webScroll(self, direction="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")