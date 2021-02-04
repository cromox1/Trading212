from datetime import datetime
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Forex_CFD.utilities.util import Util
from Forex_CFD.features.read_datatext_main import FxReadDataText_Main

class FxMainPage(FxReadDataText_Main):

    def __init__(self, driver):
        super(FxMainPage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

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

    def main_collect_data(self, currency, value_EMA, time_period, grph_div_start, dict_fx):
        arini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.from_search_goto_specific_currency(currency)
        self.change_graph_to_candlestick()
        self.set_graph_EMA_value(value_EMA)
        self.change_graph_time_period(time_period)
        # collect data from graph
        collectdata = self.collecting_data_on_graph(grph_div_start)
        datalist = collectdata[0]
        emalist = collectdata[-1]
        # gradient1 = float(datalist[-2]) - ((float(datalist[-3]) + float(datalist[-4])) / 2)
        # gradient2 = float(datalist[-3]) - ((float(datalist[-4]) + float(datalist[-5])) / 2)
        # gradient3 = float(datalist[-4]) - ((float(datalist[-5]) + float(datalist[-6])) / 2)
        gradient1 = float(datalist[-2]) - float(datalist[-3])
        gradient2 = float(datalist[-3]) - float(datalist[-4])
        gradient3 = float(datalist[-4]) - float(datalist[-5])
        ### convert to GBP
        gradient1x = 5000 * gradient1 / float(dict_fx[currency.split('/')[-1]])
        gradient2x = 5000 * gradient2 / float(dict_fx[currency.split('/')[-1]])
        gradient3x = 5000 * gradient3 / float(dict_fx[currency.split('/')[-1]])
        text1 = ''
        # if gradient3x < gradient2x < gradient1x and float(datalist[-5]) <= float(emalist[-5]) and \
        #         abs(gradient1x) > float(0.7) and float(datalist[-1]) >= float(datalist[-2]):
        #     text1 = text1 + ' BUY/LONG1'
        # if gradient3x > gradient2x > gradient1x and float(datalist[-2]) > float(emalist[-2]) + float(0.0001) \
        #         and abs(gradient1x) > float(0.7) and float(datalist[-1]) < float(datalist[-2]):
        #     text1 = text1 + ' SELL/SHORT1'
        # if float(datalist[-4]) < float(datalist[-3]) < float(datalist[-2]) and float(datalist[-5]) <= float(emalist[-5]) \
        #         and abs(gradient1x) > float(0.7) and float(datalist[-1]) >= float(datalist[-2]):
        #     text1 = text1 + ' BUY/LONG2'
        # if float(datalist[-4]) > float(datalist[-3]) > float(datalist[-2]) and float(datalist[-2]) > float(emalist[-2]) \
        #         + float(0.0001) and abs(gradient1x) > float(0.7) and float(datalist[-1]) < float(datalist[-2]):
        #     text1 = text1 + ' SELL/SHORT2'
        # if float(datalist[-5]) <= float(emalist[-5]) and float(datalist[-2]) > float(emalist[-2]) \
        #         and float(datalist[-1]) >= float(datalist[-2]):
        #     text1 = text1 + ' BUY/LONG3'
        # if float(datalist[-5]) > float(emalist[-5]) + float(0.00075) and abs(float(datalist[-2]) - float(emalist[-2])) \
        #         < float(0.00025) and float(datalist[-1]) < float(datalist[-2]):
        #     text1 = text1 + ' SELL/SHORT3'
        if gradient3x < gradient2x < gradient1x and abs(gradient1x) > float(0.7) and \
                float(datalist[-1]) >= float(datalist[-2]):
            text1 = text1 + ' BUY/LONG1 @' + str(datalist[-2]) + '<' + str(datalist[-1])
        if gradient3x > gradient2x > gradient1x and abs(gradient1x) > float(0.7) and \
                float(datalist[-1]) < float(datalist[-2]):
            text1 = text1 + ' SELL/SHORT1 @' + str(datalist[-2]) + '>' + str(datalist[-1])
        if float(datalist[-4]) < float(datalist[-3]) < float(datalist[-2]) and abs(gradient1x) > float(0.7) \
                and float(datalist[-1]) >= float(datalist[-2]):
            text1 = text1 + ' BUY/LONG2 @' + str(datalist[-2]) + '<' + str(datalist[-1])
        if float(datalist[-4]) > float(datalist[-3]) > float(datalist[-2]) and abs(gradient1x) > float(0.7) \
                and float(datalist[-1]) < float(datalist[-2]):
            text1 = text1 + ' SELL/SHORT2 @' + str(datalist[-2]) + '>' + str(datalist[-1])
        if float(datalist[-5]) <= float(emalist[-5]) and float(datalist[-2]) > float(emalist[-2]) \
                and float(datalist[-1]) >= float(datalist[-2]):
            text1 = text1 + ' BUY/LONG3 @' + str(datalist[-2]) + '<' + str(datalist[-1])
        if float(datalist[-5]) > float(emalist[-5]) + float(0.00075) and abs(float(datalist[-2]) - float(emalist[-2])) \
                < float(0.00025) and float(datalist[-1]) < float(datalist[-2]):
            text1 = text1 + ' SELL/SHORT3 @' + str(datalist[-2]) + '>' + str(datalist[-1])
        print('TIME ' + str(arini) + ' # GRADIENT for ' + currency + ' =', str("%.5f" % round(gradient3, 5)), '/',
              str("%.6f" % round(gradient3x, 6)),
              '//', str("%.5f" % round(gradient2, 5)), '/', str("%.6f" % round(gradient2x, 6)),
              '//', str("%.5f" % round(gradient1, 5)), '/', str("%.6f" % round(gradient1x, 6)), '#', text1)