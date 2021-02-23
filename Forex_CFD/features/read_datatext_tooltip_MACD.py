__author__ = 'cromox'

from time import sleep
import inspect
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as hoover
from Forex_CFD.features.read_datatext_main import FxReadDataText_Main

class FxReadDataText_ToolTip(FxReadDataText_Main):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def movearound_showtext_two(self, element, x_value, y_value, prev_text):
        # self.log.info("--> " + inspect.stack()[0][3] + " started")
        # print('DISPLAY ( x2 y2 ) ', str(element.location['x']), str(element.location['y']), ' / x , y', int(x_value), int(y_value))
        hoover(self.driver).move_to_element_with_offset(element, int(x_value), int(y_value)).perform()
        chktext = element.text.split('\n')[0].replace(' ', '')
        try:
            if chktext == prev_text:
                text = 'duplicate'
            elif str(element.text.split('\n')[4]) == 'Close':
                text = 'xlocation / ' + str(element.location['x']) + ' / ylocation / ' + str(element.location['y'])
            else:
                text = self.text_to_display_two(element.text.split('\n'))
        except:
            text = 'out_of_boundary_or_wrong_value'
        return int(element.location['x']), int(element.location['y']), text, chktext

    def text_to_display_two(self, list_text):
        # self.log.info("--> " + inspect.stack()[0][3] + " started")
        if len(list_text) >= 12:
            text = " / ".join(
                list_text[0:1] + list_text[3:7] + list_text[11:13] + list_text[-2:]).replace('Tick volume', 'TickV')
        else:
            text = " / ".join(list_text[0:3])
        return text

    def collecting_data_on_graph_two(self, fr_graph_div):
        self.log.info("--> " + inspect.stack()[0][3] + " started")
        y_divider = 4.75 # 4.25 # 3.75 # 4.3 # 3.5 # 2.7 # 4  # 8 # 4.45 # 2.5 (min) # 4.4567
        data_list = []
        EMA_list = []
        lebar = self.driver.execute_script("return window.innerWidth")
        tinggi = self.driver.execute_script("return window.innerHeight")
        # print('LEBAR = ', lebar, ' / TINGGI = ', tinggi, end=' // ')
        xp_chart_container = '//div[(@class="chart-container") or (@class="chart-container draggable")]//div[@class="clip-path"]'
        elements_chart_container = self.driver.find_elements_by_xpath(xp_chart_container)
        xdisplay = lebar
        ydisplay = tinggi
        if elements_chart_container[-1].get_attribute('style') != None:
            xdisplay = int(
                elements_chart_container[-1].get_attribute('style').split(';')[0].split('width:')[-1].split('px')[0])
            ydisplay = int(
                elements_chart_container[-1].get_attribute('style').split(';')[1].split('height:')[-1].split('px')[0])

        # print('DISPLAY ( x y ) ', xdisplay, ydisplay, ' / START_POSITION = ', int(float(xdisplay)/float(fr_graph_div)),
        #    int(ydisplay/y_divider), end=' // ')

        # css_tooltip = 'div.chart-tooltip'
        # toolTip = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_tooltip)))
        xp_tooltip = '//div[@class="chart-tooltip"]'
        toolTip = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_tooltip)))
        sleep(1)
        try:
            move0 = self.movearound_showtext_two(toolTip, int(float(xdisplay) / float(fr_graph_div)),
                                        int(ydisplay / y_divider), 'x')
        except:
            move0 = self.movearound_showtext_two(toolTip, int(float(xdisplay) / float(fr_graph_div)),
                                             int(ydisplay / y_divider) - 100, 'x')
        arrear = move0[0]
        chktext = move0[-1]
        stepadd = 5
        for steppx in range(1, xdisplay, stepadd):
            if int(arrear / 8) % 2 == 0:
                ynum = -11
            else:
                ynum = -19
            move = self.movearound_showtext_two(toolTip, -9, ynum, chktext)
            arrear = move[0]
            chktext = move[-1]
            if move[2] != 'duplicate' and move[2].split('/')[0].replace(' ', '') != 'xlocation':
                # print('NEWTEXT = ', move[2])
                data_list = data_list + [move[2].split('Open')[-1].split('/')[1].replace(' ', '')]
                # EMA_list = EMA_list + [move[2].split('EMA')[-1].split('/')[1].replace(' ', '')]
                EMA_list = EMA_list + [move[2].split('SMA')[-1].split('/')[1].replace(' ', '')]
            elif move[2].split('/')[0].replace(' ', '') == 'xlocation':
                # print('NEWTEXT = ', move[2])
                break
            if arrear > xdisplay + 190 - 15:
                # print('xlocation = ', arrear, ' / xdisplay = ', xdisplay)
                break
        xp_backbutton = '//*[@id="search-header"]//*[@data-dojo-attach-point="backButtonNode"]'
        self.driver.find_element_by_xpath(xp_backbutton).click()
        self.driver.find_element_by_xpath(xp_backbutton).click()
        # print('DATALIST = ', data_list)
        # print('EMALIST = ', EMA_list)
        return data_list, EMA_list