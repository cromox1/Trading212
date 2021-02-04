__author__ = 'cromox'

#### NOT USE/IMPLEMENT YET ######

from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import Forex_CFD.utilities.custom_logger as cl
import logging
# import time
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

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element found - locator (" + locator + ") + locatorType (" + locatorType + ")")
            self.log.info('Element = ' + str(element))
        except:
            self.log.info("Element not found - locator (" + locator + ") + locatorType (" + locatorType + ")")
        return element

    def getElementList(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("ElementList found - locator (" + locator + ") + locatorType (" + locatorType + ")")
            self.log.info('ElementList count = ' + str(len(element)))
        except:
            self.log.info("ElementList NOT found - locator (" + locator + ") + locatorType (" + locatorType + ")")
        return element

    def elementClick(self, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element - locator (" + locator + ") + locatorType (" + locatorType + ")")
        except:
            self.log.info("Cannot click on the element - locator (" + locator + ") + locatorType (" + locatorType + ")")
            print_stack()

    def sendKeys(self, data, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent data (" + str(data.encode("utf-7")) + ") on element - locator (" + locator + ") + locatorType (" + locatorType + ")")
        except:
            self.log.info("Cannot send data (" + str(data.encode("utf-7")) + ") on the element - locator (" + locator + ") + locatorType (" + locatorType + ")")
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator: # This means if locator is not empty
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding element.text, size = 0")
            text = element.text
            self.log.debug("After finding element.text, size = " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            elif len(text) != 0:
                self.log.info("Text is on the element - locator (" + locator + ") + locatorType (" + locatorType + ")")
                self.log.info("The text = '" + text + "'")
                if info != "":
                    self.log.info("Info text on element =  " +  info)
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def getValueSend(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator: # This means if locator is not empty
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding value, size = 0")
            value = element.get_attribute('value')
            self.log.debug("After finding element value, size = " + str(len(value)))
            if len(value) == 0:
                value = element.get_attribute("innerText")
            elif len(value) != 0:
                self.log.info("Text is on the element - locator (" + locator + ") + locatorType (" + locatorType + ")")
                self.log.info("The value = '" + value + "'")
                value = value.strip()
        except:
            self.log.error("Failed to get value on element " + info)
            print_stack()
            value = None
        return value

    def isElementPresent(self, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element present - locator (" + locator + ") + locatorType (" + locatorType + ")")
                return True
            else:
                self.log.info("Element not present - locator (" + locator + ") + locatorType (" + locatorType + ")")
                return False
        except:
            print("Element not found")
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        isDisplayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed - locator (" + locator + ") + locatorType (" + locatorType + ")")
            else:
                self.log.info("Element not displayed - locator (" + locator + ") + locatorType (" + locatorType + ")")
            return isDisplayed
        except:
            print("Element not found")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element present - locator (" + locator + ") + locatorType (" + str(byType) + ")")
                return True
            else:
                self.log.info("Element not present - locator (" + locator + ") + locatorType (" + str(byType) + ")")
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum / " + str(timeout) + " / seconds for element - locator (" + locator + ") + locatorType (" + str(byType) + ")")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency, ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def webScroll(self, direction="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")