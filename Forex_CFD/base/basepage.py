__author__ = 'cromox'

"""
@package base
Base Page class implementation
It implements methods which are common to all the pages throughout the application
This class needs to be inherited by all the page classes
This should not be used by creating object instances
Example:
    Class LoginPage(BasePage)
"""

#### NOT USE/IMPLEMENT YET ######

from Forex_CFD.base.selenium_driver import SeleniumDriver
from traceback import print_stack
from Forex_CFD.utilities.util import Util

class BasePage(SeleniumDriver):

    def __init__(self, driver):
        """
        Inits BasePage class
        Returns:
            None
        """
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def verifyPageTitle(self, titleToVerify):
        try:
            actualTitle = self.getTitle()
            return self.util.verifyTextContains(actualTitle, titleToVerify)
        except:
            self.log.error("Failed to get page title")
            print_stack()
            return False

    def verifyPageURL(self, expectedURL):
        currentURL = self.driver.current_url.rstrip('/')
        self.log.info("expectedURL ( " + expectedURL.rstrip('/') + " ) VS currentURL ( " + currentURL + " )")
        return currentURL == expectedURL.rstrip('/')

    def verifyPageURLlow(self, expectedURL):
        currentURL1 = self.driver.current_url
        a1 = currentURL1.split('//')[0]; a2 = currentURL1.split('//')[1]; b1 = a2.split('/')[0]
        currentURL = a1+'//'+b1
        a1 = expectedURL.split('//')[0]; a2 = expectedURL.split('//')[1]; b1 = a2.split('/')[0]
        expectedURLlow = a1+'//'+b1
        self.log.info("expectedURL ( " + expectedURLlow + " ) VS currentURL ( " + currentURL + " )")
        return currentURL == expectedURLlow

    def verifyWordExistInURL(self, word=' '):
        currentURL1 = self.driver.current_url
        countN = currentURL1.lower().split(word.lower())
        return len(countN) > 1

    def verifyLocatorText(self, locator, locatorType, expectedText):
        result = self.getText(locator, locatorType)
        self.log.info("expectedText ( " + str(expectedText) + " ) VS LocatorText ( " + str(result) + " )")
        return str(result) == str(expectedText)

    def verifyLocatorTextNotNone(self, locator, locatorType):
        result = self.getText(locator, locatorType)
        self.log.info("LocatorText = " + str(result) + " locator (" + str(locator) + ") + locatorType (" + locatorType + ")")
        return result is not None

    def verifyLocatorValueText(self, locator, locatorType, expectedText):
        element = self.getElement(locator, locatorType)
        result = element.get_attribute('value')
        self.log.info("expectedText ( " + str(expectedText) + " ) VS LocatorText ( " + str(result) + " )")
        return str(result.lower()) == str(expectedText.lower())

    def verifyActualGreaterEqualExpected(self, Actual, Expected):
        self.log.info("Actual ( " + str(Actual) + " ) >= Expected ( " + str(Expected) + " )")
        return Actual >= Expected

    def verifyActualEqualExpected(self, Actual, Expected):
        self.log.info("Actual ( " + str(Actual) + " ) == Expected ( " + str(Expected) + " )")
        return Actual == Expected

    def verifyTextEqual(self, Text, Expected):
        self.log.info("Text ( " + str(Text) + " ) == Expected ( " + str(Expected) + " )")
        return Text == Expected

    def verifyDateIsFuture(self, futureepoch):
        from time import time, strftime, localtime
        currentepoch = int(time())
        currentdate = strftime('%Y-%m-%d %H:%M:%S')
        futuredate = strftime('%Y-%m-%d %H:%M:%S', localtime(futureepoch))
        self.log.info("FutureDate ( " + str(int(futureepoch)) + " / " + str(futuredate) + " ) > CurrentDate ( " +
                      str(int(currentepoch)) + " / " + str(currentdate)+ " )")
        return int(futureepoch) > int(currentepoch)

    def verifyDateIsHistory(self, historyepoch):
        from time import time, strftime, localtime
        currentepoch = int(time())
        currentdate = strftime('%Y-%m-%d %H:%M:%S')
        historydate = strftime('%Y-%m-%d %H:%M:%S', localtime(historyepoch))
        self.log.info("HistoryDate ( " + str(int(historyepoch)) + " / " + str(historydate) + " ) < CurrentDate ( " +
                      str(int(currentepoch)) + " / " + str(currentdate) + " )")
        return int(historyepoch) < int(currentepoch)