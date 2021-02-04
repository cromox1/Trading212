from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as hoover
from Forex_CFD.utilities.util import Util
from Forex_CFD.features.read_datatext_tooltip import FxReadDataText_ToolTip

class FxReadDataText_Main(FxReadDataText_ToolTip):

    def __init__(self, driver):
        super(FxReadDataText_Main, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def from_search_goto_specific_currency(self, currency):
        # if self.driver.find_element_by_xpath('//*[@id="search-header"]//*[@class="search-input"]'):
        #     self.driver.find_element_by_xpath('//*[@id="search-header"]//*[@class="search-input"]').click()
        elemlist = self.driver.find_elements_by_id("navigation-search-button")
        hoover(self.driver).move_to_element_with_offset(elemlist[0], 10, 0).perform()
        elemlist[0].click()
        self.driver.find_element_by_xpath("//*[contains(text(),'Currencies')]").click()
        self.driver.find_element_by_xpath("//*[contains(text(),'Major')]").click()
        sleep(1)
        currency1 = currency.replace('/', '')
        xp_currency = '//*[@data-code="' + currency1 + '"]//*[@class="ticker"]//*[@class="has-ellipsed-text"]'
        element1 = self.driver.find_element_by_xpath(xp_currency)
        element1.click()
        # print('\nCURRENCY = ', currency)
        print('CURRENCY = ', currency)
        sleep(0.5)

    def change_graph_to_candlestick(self):
        xp_templatebar = '//*[@class="chart-menu"]//*[@data-dojo-attach-point="templatesArrowNode"]'
        elements = self.driver.find_elements_by_xpath(xp_templatebar)
        # print('number of elements = ', len(elements))
        element_template = elements[-1]
        element_template.click()
        # xp_pro_tab = '//*[@id="chart-templates"]/div[2]/div/div/div/div'
        xp_pro_tab = '//*[@id="chart-templates"]//*[contains(text(), "PRO")]'
        self.driver.find_element_by_xpath(xp_pro_tab).click()
        element_template.click()
        # print('-- > END 1 - Candlestick')
        sleep(0.5)

    def set_graph_EMA_value(self, value_EMA):
        xp_indicator = '//*[@id="chartTabIndicators"]//*[@data-dojo-attach-point="indicatorsArrowNode"]'
        elements = self.driver.find_elements_by_xpath(xp_indicator)
        element_indicator = elements[-1]
        element_indicator.click()
        self.driver.find_element_by_xpath("//*[contains(text(),'Trend')]").click()
        # self.driver.find_element_by_xpath("//*[contains(text(),'EMA')]").click()  # < -- if using EMA
        self.driver.find_element_by_css_selector(".item-trend-sma").click()  # < -- if using Simple Moving Average (SMA)
        xp_period = '//*[@id="chart-settings"]//*[@class="editable-input"]'
        element_period = self.driver.find_element_by_xpath(xp_period)
        element_period.clear()
        element_period.send_keys(str(value_EMA))
        if self.driver.find_element_by_xpath("//div[@id='chart-settings']/div[3]/div[3]/div[2]/div"):
            self.driver.find_element_by_xpath("//div[@id='chart-settings']/div[3]/div[3]/div[2]/div").click()
            self.driver.find_element_by_css_selector(".item-colorpicker-be4138").click()
        # confirm button
        self.driver.find_elements_by_xpath('//div[@class="window-controls"]/div[@class="button confirm-button"]')[0].click()
        ## alternative
        # self.driver.find_element_by_xpath("//*[contains(text(),'Confirm')]").click()
        # print('-- > END 2 -', value_EMA, 'EMA line')

    def change_graph_time_period(self, time_period):
        self.driver.find_elements_by_xpath('//*[@id="chartTabPeriods"]//*[@class="arrow-icon svg-icon-holder"]')[-1].click()
        self.driver.find_element_by_xpath('//*[contains(text(), "' + time_period + '")]').click()
        # print('-- > END 3 - set time period ' + time_period)
        sleep(0.5)

    def collecting_data_on_graph(self, fr_graph_div):
        y_divider = 4  # 8 # 4.45 # 2.5 # 4.4567
        data_list = []
        EMA_list = []
        lebar = self.driver.execute_script("return window.innerWidth")
        tinggi = self.driver.execute_script("return window.innerHeight")
        # print('LEBAR x = ', lebar, ' / TINGGI y = ', tinggi)
        xp_chart_container = '//*[((@class="chart-container") or (@class="chart-container draggable")) and (@tabindex="-1")]'
        elements_chart_container = self.driver.find_elements_by_xpath(xp_chart_container)
        xdisplay = lebar
        ydisplay = tinggi
        if elements_chart_container[-1].get_attribute('style') != None:
            xdisplay = int(
                elements_chart_container[-1].get_attribute('style').split(';')[0].split('width:')[-1].split('px')[0])
            ydisplay = int(
                elements_chart_container[-1].get_attribute('style').split(';')[1].split('height:')[-1].split('px')[0])
        # print('DISPLAY = ( x y ) ', xdisplay, ydisplay, ' / START_POSITION = ', int(float(xdisplay)/float(fr_graph_div)),
        #   int(ydisplay/y_divider))
        xp_tooltip = '//*[@class="chart-tooltip"]'
        toolTip = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_tooltip)))
        sleep(1)
        move0 = self.movearound_showtext(toolTip, int(float(xdisplay) / float(fr_graph_div)),
                                    int(ydisplay / y_divider), 'x')
        arrear = move0[0]
        chktext = move0[-1]
        stepadd = 5
        for steppx in range(1, xdisplay, stepadd):
            if int(arrear / 8) % 2 == 0:
                ynum = -11
            else:
                ynum = -19
            move = self.movearound_showtext(toolTip, -9, ynum, chktext)
            arrear = move[0]
            chktext = move[-1]
            if move[2] != 'duplicate' and move[2].split('/')[0].replace(' ', '') != 'xlocation':
                # print('NEWTEXT = ', move[2])
                data_list = data_list + [move[2].split('Close')[-1].split('/')[1].replace(' ', '')]
                # EMA_list = EMA_list + [move[2].split('EMA')[-1].split('/')[1].replace(' ', '')]
                EMA_list = EMA_list + [move[2].split('SMA')[-1].split('/')[1].replace(' ', '')]
            elif move[2].split('/')[0].replace(' ', '') == 'xlocation':
                # print('NEWTEXT = ', move[2])
                break
            if arrear > xdisplay + 190 - 15:
                print('xlocation = ', arrear, ' / xdisplay = ', xdisplay)
                break
        xp_backbutton = '//*[@id="search-header"]//*[@data-dojo-attach-point="backButtonNode"]'
        self.driver.find_element_by_xpath(xp_backbutton).click()
        self.driver.find_element_by_xpath(xp_backbutton).click()
        # print('DATALIST = ', data_list)
        # print('EMALIST = ', EMA_list)
        return data_list, EMA_list