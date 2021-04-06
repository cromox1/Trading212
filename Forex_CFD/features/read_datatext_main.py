__author__ = 'cromox'

from time import sleep
import inspect
from selenium.webdriver.common.action_chains import ActionChains as hoover
from Forex_CFD.features.main_page import FxMainPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class FxReadDataText_Main(FxMainPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def from_search_goto_specific_currency(self, currency):
        self.log.info("-> " + inspect.stack()[0][3] + " started" + ' / CURRENCY = ' + currency)
        # if self.driver.find_element_by_xpath('//*[@id="search-header"]//*[@class="search-input"]'):
        #     self.driver.find_element_by_xpath('//*[@id="search-header"]//*[@class="search-input"]').click()
        # elemlist = self.driver.find_elements_by_id("navigation-search-button")
        elemlist = self.driver.find_elements_by_xpath('//*[@id="navigation"]//div[@id="navigation-search-button" and @class="search-button"]')
        hoover(self.driver).move_to_element_with_offset(elemlist[0], 10, 0).perform()
        elemlist[0].click()
        self.driver.find_element_by_xpath("//*[contains(text(),'Currencies')]").click()
        self.driver.find_element_by_xpath("//*[contains(text(),'Major')]").click()
        sleep(1)
        currency1 = currency.replace('/', '')
        xp_currency = '//*[@data-code="' + currency1 + '"]//*[@class="ticker"]//*[@class="has-ellipsed-text"]'
        element1 = self.driver.find_element_by_xpath(xp_currency)
        element1.click()
        print(currency, end=' ')
        sleep(0.5)

    def change_graph_to_candlestick(self):
        # self.log.info("--> " + inspect.stack()[0][3] + " started")
        xp_templatebar = '//*[@class="chart-menu"]//*[@data-dojo-attach-point="templatesArrowNode"]'
        elements = self.driver.find_elements_by_xpath(xp_templatebar)
        # print('number of elements = ', len(elements))
        element_template = elements[-1]
        element_template.click()
        # xp_pro_tab = '//*[@id="chart-templates"]/div[2]/div/div/div/div'
        xp_pro_tab = '//*[@id="chart-templates"]//div[contains(text(), "MACD")]'
        self.driver.find_element_by_xpath(xp_pro_tab).click()
        element_template.click()
        # print('-- > END 1 - Candlestick')
        sleep(0.5)

    def set_graph_EMA_value(self, value_EMA):
        # self.log.info("--> " + inspect.stack()[0][3] + " started")
        xp_indicator = '//*[@id="chartTabIndicators"]//*[@data-dojo-attach-point="indicatorsArrowNode"]'
        elements = self.driver.find_elements_by_xpath(xp_indicator)
        element_indicator = elements[-1]
        element_indicator.click()
        self.driver.find_element_by_xpath("//*[contains(text(),'Trend')]").click()
        # self.driver.find_element_by_xpath("//*[contains(text(),'EMA')]").click()  # < -- if using EMA
        self.driver.find_element_by_css_selector(".item-trend-sma").click()  # < -- if using Simple Moving Average (SMA)
        ## set SMA/EMA value
        xp_period = '//*[@id="chart-settings"]//*[@class="editable-input"]'
        element_period = self.driver.find_element_by_xpath(xp_period)
        element_period.clear()
        element_period.send_keys(str(value_EMA))
        ## set SMA/EMA colour and thickness
        # unixcolor_ele = self.driver.find_element_by_xpath("//div[@id='chart-settings']/div[3]/div[3]/div[2]/div")
        # (working on Windows but not Linux/Lubuntu)
        # unixcolor_ele = self.driver.find_element_by_css_selector('div.combobox._focusable.colorpicker-icon')
        unixcolor_ele = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.combobox._focusable.colorpicker-icon')))
        unixcolor_id = unixcolor_ele.get_attribute('id')
        unixcolor_ele.click()
        # self.driver.find_element_by_css_selector(".item-colorpicker-be4138").click()
        colorpick_ele = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".item-colorpicker-be4138")))
        colorpick_ele.click()
        unixcolor_list = str(unixcolor_id).split('_')
        ## thickness
        idthickness1 = int(unixcolor_list[-1]) + 1
        idthickness = '_'.join(str(i) for i in unixcolor_list[:-1] + [idthickness1])
        self.driver.find_element_by_css_selector(f"#{idthickness} > span").click()
        self.driver.find_element_by_css_selector(".item-main-2").click()
        ## set SMA/EMA use 'Open' price
        # '//div[@class="editable-content"]/div[@class="combobox combo_indicator_settings_price _focusable"]/span[@class="dropdown-arrow"]'
        # '//div[@id="chart-settings"]//div[@class="editable-container"]/div[@class="editable-content"]/div[@class="combo_indicator_settings_price"]/span[@class="dropdown-arrow"]'
        idprice1 = int(unixcolor_list[-1]) - 1
        idprice = '_'.join(str(i) for i in unixcolor_list[:-1] + [idprice1])
        self.driver.find_element_by_css_selector(f"#{idprice} > span").click()
        self.driver.find_element_by_css_selector(".item-indicator-settings-list-open").click()
        sleep(0.5)
        ## confirm button
        self.driver.find_elements_by_xpath('//div[@class="window-controls"]/div[@class="button confirm-button"]')[0].click()
        ## alternative confirm button
        # self.driver.find_element_by_css_selector(".confirm-button").click()
        # self.driver.find_element_by_xpath("//*[contains(text(),'Confirm')]").click()
        ## settings > disable Open position
        id_ele = self.driver.find_element_by_xpath('//div[@class="chart-container"]/div[@class="chart-menu"]').get_attribute('id')
        self.driver.find_element_by_css_selector(f"#{id_ele} > #chartTabSettings").click()
        self.driver.find_element_by_css_selector(".item-chart-settings-list-open-positions").click()
        # print('-- > END 2 -', value_EMA, 'EMA line')

    def change_graph_time_period(self, time_period):
        # self.log.info("--> " + inspect.stack()[0][3] + " started")
        self.driver.find_elements_by_xpath('//*[@id="chartTabPeriods"]//*[@class="arrow-icon svg-icon-holder"]')[-1].click()
        self.driver.find_element_by_xpath('//*[contains(text(), "' + time_period + '")]').click()
        # print('-- > END 3 - set time period ' + time_period)
        sleep(0.5)