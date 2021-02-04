from selenium.webdriver.common.action_chains import ActionChains as hoover
from Forex_CFD.utilities.util import Util
from Forex_CFD.features.dailyfx_currency import currency_date_value
from Forex_CFD.features.main_page import FxMainPage

class FxReadDataText_ToolTip(FxMainPage):

    def __init__(self, driver):
        super(FxReadDataText_ToolTip, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def movearound_showtext(self, element, x_value, y_value, prev_text):
        # print('DISPLAY = ( x2 y2 ) ', int(x_value), int(y_value))
        hoover(self.driver).move_to_element_with_offset(element, int(x_value), int(y_value)).perform()
        chktext = element.text.split('\n')[0].replace(' ', '')
        try:
            if chktext == prev_text:
                text = 'duplicate'
            elif str(element.text.split('\n')[4]) == 'Close':
                text = 'xlocation / ' + str(element.location['x']) + ' / ylocation / ' + str(element.location['y'])
            else:
                text = self.text_to_display(element.text.split('\n'))
        except:
            text = 'out_of_boundary_or_wrong_value'
        return int(element.location['x']), int(element.location['y']), text, chktext

    def text_to_display(self, list_text):
        if len(list_text) >= 12:
            text = " / ".join(
                list_text[0:1] + list_text[3:7] + list_text[11:13] + list_text[-2:]).replace('Tick volume', 'TickV')
        else:
            text = " / ".join(list_text[0:3])
        return text

    def looping_check_all_currencies(self, value_EMA, tperiod):
        grph_div_start_point = 1.329  # division graph of starting point? ( value = 1.28 to infinity)
        fxconvert = currency_date_value()
        ix = 1
        print()
        for currency in ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]:
            print(str(ix) + ' ) (tperiod: ' + str(tperiod) + ') // ', end='')
            self.driver = self.main_collect_data(self, currency, value_EMA, tperiod, grph_div_start_point, fxconvert)
            ix += 1