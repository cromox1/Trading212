from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Forex_CFD.features.main_page import FxMainPage

class FxBuySell(FxMainPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def buy(self, amount):
        if self.driver.find_element_by_xpath("//div[@class='visible-input']//input[contains(@id, 'uniqName')]"):
            # element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            #             (By.XPATH, "//div[@class='visible-input']//input[contains(@id, 'uniqName')]")))
            element = self.driver.find_elements_by_xpath("//div[@class='visible-input']//input[contains(@id, 'uniqName')]")[0]
            element.clear()
            for character in str(amount):
                element.send_keys(character)
                sleep(0.5)
            # Confirm Button
            if self.driver.find_element_by_xpath("//div[contains(@class,'confirm-button')]"):
                self.driver.find_elements_by_xpath("//div[contains(@class,'confirm-button')]")[0].click()
        elif self.driver.find_element_by_xpath("//*[contains(text(),'Market closed')]"):
            print('Market closed')
            self.driver.find_elements_by_xpath("//*[@class='header']//*[@class='close-icon']")[0].click()

    def sell(self, amount):
        # Switching to sell
        self.driver.find_elements_by_xpath("//div[@data-dojo-attach-event='click: setDirectionSell']")[0].click()
        # From there on it's exactly like the buy
        self.buy(amount)

    def script_click_xpath(self, xpath):
        self.driver.execute_script(f"document.evaluate(\"{xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()")

    def open_stock_dialog(self, stock):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, "//span[contains(@data-dojo-attach-event, 'onOpenDialogClick')]")))
        elem = self.driver.find_elements_by_xpath("//span[contains(@data-dojo-attach-event, 'onOpenDialogClick')]")
        # try both elements
        try:
            elem[0].click()
        except:
            elem[1].click()
        # Search the stock
        elem = self.driver.find_element_by_xpath("//input[@placeholder=\"Instrument search\"]")
        # Setting the max length to 100 so the API'll be able to enter long stocks names
        self.driver.execute_script("arguments[0].setAttribute('maxlength',arguments[1])", elem, 100)
        elem.send_keys(stock)
        # Open its dialog with JS. Selenium couldn't open the dialog itself.
        self.script_click_xpath(f"//*[@id='list-results-instruments']//span[contains(@class, 'instrument-name') and .='{stock}']")
        sleep(1)

    def buy_stock(self, stock, amount):
        self.open_stock_dialog(stock)
        self.buy(amount)
        sleep(0.5)

    def sell_stock(self, stock, amount):
        # It's just opening a stock and selling it
        self.open_stock_dialog(stock)
        self.sell(amount)
        sleep(0.5)