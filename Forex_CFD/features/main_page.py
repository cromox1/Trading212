__author__ = 'cromox'

from time import sleep
from datetime import datetime
from pytz import timezone
import inspect
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

    def autologin_firstwindows(self, base_url, username, passwd):
        self.log.info("-> " + inspect.stack()[0][3] + " started")
        self.log.info("--> Trading212 user = " + str(username))
        self.driver.get(base_url)
        self.driver.find_element_by_id("cookie-bar").click()
        self.driver.find_element_by_id("login-header-desktop").click()
        self.driver.find_element_by_id("username-real").send_keys(username + Keys.ENTER)
        print('Trading212 user = ', username)
        self.driver.find_element_by_id("pass-real").send_keys(passwd + Keys.ENTER)
        sleep(2)

    def close_popup_ask_upload_docs(self):
        self.log.info("--> " + inspect.stack()[0][3] + " started")
        # CSS selector - >  #upload-popup-3 > div.popup-header > div.close-icon.svg-icon-holder
        # xpath1 = '//div[@id="onfido-upload"]//div[@class="close-icon svg-icon-holder"]'   # old one
        # xpath2 = '//div[@id="upload-popup-3"]//div[@class="close-icon svg-icon-holder"]'  # new one
        xpathx = '//div[contains(@id, "upload")]//div[@class="close-icon svg-icon-holder"]'
        try:
            self.driver.find_element_by_xpath(xpathx).click()
        except:
            print('no pop-up')

    def mode_live_or_demo(self, mode):
        self.log.info("--> " + inspect.stack()[0][3] + " started // Mode = " + str(mode))
        print('Mode use = ', mode)
        current_url = self.driver.current_url
        urlmode = current_url.split('//')[-1].split(".")[0]  # -- > live or demo
        if urlmode == "live" and mode == "Practice":
            # elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            # (By.CLASS_NAME, "account-menu-button")))
            elem_ele = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#navigation > div.account-menu-button.cfd > div.text-wrapper > div.user')))
            # elem_ele = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(
            #     (By.CSS_SELECTOR, '#navigation > div.account-menu-button.cfd > div.text-wrapper')))
            # elem_ele = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            #     (By.CSS_SELECTOR, '#navigation > div.account-menu-button.cfd > div.text-wrapper > div.user')))
            elem_ele.click()
            try:
                elem_chg = self.driver.find_element_by_class_name("green")
                elem_chg.click()
                current_url = self.driver.current_url
                self.driver.get(current_url)
            except:
                print('Unsuccessfull to change from', urlmode, 'to', mode)
        elif urlmode == "demo" and mode == "Real":
            elem_ele = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#navigation > div.account-menu-button.cfd > div.text-wrapper > div.user')))
            # elem_ele = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(
            #     (By.CSS_SELECTOR, '#navigation > div.account-menu-button.cfd > div.text-wrapper')))
            # elem_ele = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            #     (By.CSS_SELECTOR, '#navigation > div.account-menu-button.cfd > div.text-wrapper > div.user')))
            elem_ele.click()
            try:
                elem_chg = self.driver.find_element_by_class_name("blue")
                elem_chg.click()
                current_url = self.driver.current_url
                self.driver.get(current_url)
            except:
                print('Unsuccessfull to change from', urlmode, 'to', mode)
        else:
            print('Already on ' + mode + ' mode')

    def currency_had_macd(self, currency='', time_period=''):
        dictionary = {'1 minute': {"USD/JPY": float(0.00540),
                                   "GBP/USD": float(0.00011),
                                   "EUR/USD": float(0.00006),
                                   "USD/CHF": float(0.00005),
                                   "USD/CAD": float(0.00006),
                                   "AUD/USD": float(0.00005),
                                   "NZD/USD": float(0.00005)},
                      '5 minutes': {"USD/JPY": float(0.01075),
                                    "GBP/USD": float(0.00021),
                                    "EUR/USD": float(0.00016),
                                    "USD/CHF": float(0.00013),
                                    "USD/CAD": float(0.00016),
                                    "AUD/USD": float(0.00014),
                                    "NZD/USD": float(0.00014)}}
        if time_period in dictionary and currency in dictionary[time_period]:
            return dictionary[time_period][currency]
        elif time_period in dictionary and currency not in dictionary[time_period]:
            if time_period == list(dictionary.keys())[0]:
                return float(0.00006)
            elif time_period == list(dictionary.keys())[1]:
                return float(0.00013)
            else:
                return float(0.00010)
        else:
            return float(0)

    def currencies_to_use(self, level):
        dictionary = {'major': ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"],
                      'minor': ["EUR/GBP", "GBP/JPY", "AUD/JPY", "AUD/NZD", "CAD/JPY", "EUR/CAD", "EUR/CHF", "EUR/JPY",
                                "EUR/NZD", "GBP/CHF"]}
        if level in dictionary:
            return dictionary[level]
        else:
            return []

    def time_script_running_and_next(self, datetimestart, min_delay, min_gap, timezonename='Europe/London'):
        print()
        delaybeforerun = int(min_delay * 60) + 1
        timebetweenrun = int(min_gap * 60)
        epochstart = int(datetime.strptime(datetimestart, "%Y-%m-%d %H:%M:%S GMT%z").timestamp())
        arini_date = datetime.now(timezone(timezonename)).strftime("%Y-%m-%d %H:%M:%S GMT%z")
        arini_epoch = int(datetime.now(timezone(timezonename)).timestamp())
        lamascript = arini_epoch - epochstart
        nanti = int((arini_epoch + timebetweenrun) / timebetweenrun) * timebetweenrun + delaybeforerun
        tidor = nanti - arini_epoch
        futuretime = datetime.fromtimestamp(nanti, timezone(timezonename)).strftime('%Y-%m-%d %H:%M:%S GMT%z')
        print('SCRIPTS HAS RUN FOR', lamascript, 'secs', end='')
        print(', WILL RUN AGAIN AT :', futuretime, '( NOW =', arini_date, '/ in', tidor, 'secs )')
        sleep(tidor)

    def buy_sell_list_add_instrument(self, todopoint_dict, current_buysell, limit_buysell, buymark, sellmark):
        list_to_buysell = [vv for vv in list(todopoint_dict.keys()) if
                           todopoint_dict[vv] > sellmark > 0 or todopoint_dict[vv] < buymark < 0 or
                           todopoint_dict[vv] < sellmark < 0 or todopoint_dict[vv] > buymark > 0]
        to_add_number = len(list_to_buysell)
        avail_number = limit_buysell - current_buysell
        if 0 < to_add_number <= avail_number:
            list_add_instrument = list_to_buysell
        elif 0 < avail_number < to_add_number:
            list_add_instrument = list_to_buysell[:avail_number]
        else:
            list_add_instrument = []
        print(' -- > LIMIT =', limit_buysell, '// CURRENT_TRADE =', current_buysell, '// AVAILABLE =', avail_number,
              '// TO_ADD =', to_add_number, ':: LIST = ', list_to_buysell)
        if to_add_number == 0 and current_buysell != limit_buysell:
            print(' --- > # NOTHING TO ADD - NO Currency MEET the requirement for current Forex_Trading')
        elif current_buysell == limit_buysell:
            print(' --- > # NOTHING TO ADD - Had Reach Max_Limit =', limit_buysell)
        elif to_add_number > avail_number and avail_number > 0:
            print(' --- > Limit_Trader (', limit_buysell, ') nearly reach - SO only', avail_number,
                  'Currency will be Traded', '- > NEW LIST =', list_add_instrument)
        else:
            print(' --- > TO_ADD =', len(list_add_instrument), '- > LIST =', list_add_instrument)
        return list_add_instrument

    def final_dict_buy_sell_currency(self, list_instrument, dict_todopoint, open_position, all_currencies, buymark, buystart, sellmark, sellstart):
        buy_dict = {}
        sell_dict = {}
        if len(list_instrument) > 0:
            for curr in list_instrument:
                if dict_todopoint[curr] < buymark < 0 and curr not in open_position:
                    amount = buystart + all_currencies.index(curr)
                    print(' ---- > TO BUY = (Currency)', curr, '(Amount)', amount)
                    buy_dict[curr] = amount
                elif dict_todopoint[curr] > sellmark > 0 and curr not in open_position:
                    amount = sellstart + all_currencies.index(curr)
                    print(' ---- > TO SELL = (Currency)', curr, '(Amount)', amount)
                    sell_dict[curr] = amount
                elif dict_todopoint[curr] > buymark > 0 and curr not in open_position:
                    amount = buystart + all_currencies.index(curr)
                    print(' ---- > TO BUY = (Currency)', curr, '(Amount)', amount)
                    buy_dict[curr] = amount
                elif dict_todopoint[curr] < sellmark < 0 and curr not in open_position:
                    amount = sellstart + all_currencies.index(curr)
                    print(' ---- > TO SELL = (Currency)', curr, '(Amount)', amount)
                    sell_dict[curr] = amount
                else:
                    print(' ---- > CANNOT ADD (Currency)', curr, '-- Already EXIST in open_position')
        return buy_dict, sell_dict

    def open_position_printstatus(self, currency, currency_value, direction, directionpoint, closebuypoint, closesellpoint):
        print('  -- > ', currency, ' # DIRECTION =', direction, '/ CURRENT_DIRECTION_POINT =', directionpoint, end='')
        if closebuypoint < 0 and closesellpoint > 0:            ## GRADIENT
            if direction == 'BUY' and directionpoint > 0:
                print(' # - > RIGHT DIRECTION')
            elif direction == 'SELL' and directionpoint < 0:
                print(' # - > RIGHT DIRECTION')
            elif directionpoint == 0:
                print(' # - >', direction, 'BUT NO DIRECTION CURRENTLY!!!')
            elif direction == 'BUY' and closebuypoint <= directionpoint < 0:
                print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
            elif direction == 'SELL' and closesellpoint >= directionpoint > 0:
                print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
            else:
                if currency_value > 0:
                    print(' # - > WRONG DIRECTION !!! -- URGENT - TO CLOSE // PROFIT =', currency_value)
                elif currency_value <= 0:
                    print(' # - > WRONG DIRECTION !!! URGENT BUT CANNOT CLOSE // NOT_PROFIT =', currency_value)
        elif closebuypoint > 0 and closesellpoint < 0:         ## MACD
            if direction == 'BUY' and directionpoint < 0:
                print(' # - > RIGHT DIRECTION')
            elif direction == 'SELL' and directionpoint > 0:
                print(' # - > RIGHT DIRECTION')
            elif directionpoint == 0:
                print(' # - >', direction, 'BUT NO DIRECTION CURRENTLY!!!')
            elif direction == 'BUY' and closebuypoint >= directionpoint > 0:
                print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
            elif direction == 'SELL' and closesellpoint <= directionpoint < 0:
                print(' # - > SLIGHTLY WRONG DIRECTION !!! TO CHECK FOR NEXT RUN')
            else:
                if currency_value > 0:
                    print(' # - > WRONG DIRECTION !!! -- URGENT - TO CLOSE // PROFIT =', currency_value)
                elif currency_value <= 0:
                    print(' # - > WRONG DIRECTION !!! URGENT BUT CANNOT CLOSE // NOT_PROFIT =', currency_value)

    def final_close_position_elemenid(self, currency, currency_value, direction, directionpoint, hardprofit,
                                      closebuypoint, closesellpoint, exitprofit, elementid):
        if currency_value > hardprofit:
            print('    - > TO CLOSE #', currency, '// ACHIEVED Target Hard_Profit ( >', hardprofit, ') =', currency_value)
            return elementid
        elif direction == 'BUY' and directionpoint < closebuypoint < 0 and currency_value > exitprofit:    ## GRADIENT
            print('    - > TO CLOSE #', currency, '// CHANGE DIRECTION = BUY to SELL / Point =', directionpoint)
            return elementid
        elif direction == 'SELL' and directionpoint > closesellpoint > 0 and currency_value > exitprofit:  ## GRADIENT
            print('    - > TO CLOSE #', currency, '// CHANGE DIRECTION = SELL to BUY / Point =', directionpoint)
            return elementid
        elif direction == 'BUY' and directionpoint > closebuypoint > 0 and currency_value > exitprofit:    ## MACD
            print('    - > TO CLOSE #', currency, '// CHANGE DIRECTION = BUY to SELL / Point =', directionpoint)
            return elementid
        elif direction == 'SELL' and directionpoint < closesellpoint < 0 and currency_value > exitprofit:  ## MACD
            print('    - > TO CLOSE #', currency, '// CHANGE DIRECTION = SELL to BUY / Point =', directionpoint)
            return elementid
        else:
            return

    # def css_list_containing_text_in_class(self, driver, selector, text):
    #     elements = driver.find_elements_by_css_selector(selector)
    #     return [element for element in elements if text in element.get_attribute('class')]