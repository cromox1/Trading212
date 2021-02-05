from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Forex_CFD.base.basepage import BasePage
import Forex_CFD.utilities.custom_logger as cl
import logging

class FxMainPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def autologin_maxwindows(self, base_url, username, passwd):
        self.driver.maximize_window()
        self.driver.get(base_url)
        self.driver.find_element_by_id("cookie-bar").click()
        self.driver.find_element_by_id("login-header-desktop").click()
        self.driver.find_element_by_id("username-real").send_keys(username + Keys.ENTER)
        self.driver.find_element_by_id("pass-real").send_keys(passwd + Keys.ENTER)
        sleep(3)

    def close_popup_ask_upload_docs(self):
        # //*[@id="onfido-upload"]/div[1]/div[2]
        xpath1 = '//div[@id="onfido-upload"]//div[@class="close-icon svg-icon-holder"]'
        try:
            self.driver.find_element_by_xpath(xpath1).click()
        except:
            print('no pop-up')

    def mode_live_or_demo(self, mode):
        current_url = self.driver.current_url
        urlmode = current_url.split('//')[-1].split(".")[0]  # -- > live or demo
        if urlmode == "live" and mode == "Practice":
            elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "account-menu-button")))
            elem.click()
            try:
                elem = self.driver.find_element_by_class_name("green")
                elem.click()
            except:
                print('already on Practice mode')
        elif urlmode == "demo" and mode == "Real":
            elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "account-menu-button")))
            elem.click()
            try:
                elem = self.driver.find_element_by_class_name("blue")
                elem.click()
            except:
                print('already on Real mode')