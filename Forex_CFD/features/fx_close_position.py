__author__ = 'cromox'

from time import sleep
import inspect
from datetime import datetime
from pytz import timezone
from Forex_CFD.features.fx_buysell import FxBuySell

class FxClosePosition(FxBuySell):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def list_CFD_open_position(self):
        self.log.info("--> " + inspect.stack()[0][3] + " started")
        try:
            self.driver.find_element_by_css_selector(
                "#uniqName_0_0 > span.tab-item.tabpositions.has-tooltip.svg-icon-holder.tab-active")
        except:
            self.driver.find_element_by_css_selector(
                "#uniqName_0_0 > span.tab-item.tabpositions.has-tooltip.svg-icon-holder").click()
        xp_instr_table = '//div[@id="layout"]/div[@id="accountPanel"]/div[@id="positionsTable"]//table[@data-dojo-attach-point="tableNode"]/tbody/tr'
        instrument_list = self.driver.find_elements_by_xpath(xp_instr_table)
        sleep(1)
        free_fund = self.driver.find_elements_by_xpath(
            '//*[@id="equity-free"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
        total_fund = self.driver.find_elements_by_xpath(
            '//*[@id="equity-total"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
        result = self.driver.find_elements_by_xpath(
            '//*[@id="equity-ppl"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
        # "%.5f" % round(float(VALUE)), 5)
        myDFD = "%.2f" % round((float(total_fund.replace('£', '')) - float(result.replace('£', ''))), 2)
        arini = datetime.now(timezone('Europe/London')).strftime("%Y-%m-%d %H:%M:%S %Z%z")
        print('\n# No_Instruments =', len(instrument_list), '// NOW', arini, '// DFD =', '£' + str(myDFD),
              '// Total_Fund =', total_fund, '// Free_Fund =', free_fund, '// Live_Result =', result)
        dict1 = {}
        dict2 = {}
        if len(instrument_list) >= 1:
            i = 1
            for ele in instrument_list:
                id_ele = ele.get_attribute('id')
                print(i, end=' ) ')
                text = ''
                for info in ["name", "quantity", "direction", "averagePrice", "currentPrice", "margin", "ppl"]:
                    xpathx = f"//table[@data-dojo-attach-point='tableNode']//tr[@id='{id_ele}']//td[contains(@class,'{info}')]"
                    element = self.driver.find_elements_by_xpath(xpathx)[0]
                    print(info, "=", element.text.replace(' ', ''), end=' / ')
                    text = text + element.text.replace(' ', '') + ' / '
                dict1[i] = id_ele
                dict2[i] = text
                i += 1
                print()
        return dict1, dict2, arini

    def pilihan_to_close_position(self, num_choice):
        self.log.info("--> " + inspect.stack()[0][3] + " started")
        if num_choice > 3:
            print('r ) RERUN/CHECK CURRENCY PROJECTION')
            print('x ) QUIT')
            pilihan = input("Your Choice ? CLOSE [ 1 - " + str(num_choice - 2) + " ] or BUY/SELL [ " +
                            str(num_choice - 1) + " / " + str(
                num_choice) + " ] or RERUN [ r / 77 ] or QUIT [ x / 99 ] : ")
        elif num_choice == 3:
            print('r ) RERUN/CHECK CURRENCY PROJECTION')
            print('x ) QUIT')
            pilihan = input("Your Choice ? CLOSE [ 1 ] or BUY/SELL [ " +
                            str(num_choice - 1) + " / " + str(
                num_choice) + " ] or RERUN [ r / 77 ] or QUIT [ x / 99 ] : ")
        elif num_choice == 1:
            pilihan = 1
        else:
            print('r ) RERUN/CHECK CURRENCY PROJECTION')
            print('x ) QUIT')
            pilihan = input("Your Choice ? BUY/SELL [ " + str(num_choice - 1) + " / " + str(num_choice) +
                            " ] or RERUN [ r / 77 ] or QUIT [ x / 99 ] : ")
        try:
            return int(pilihan)
        except:
            print("Error - '" + str(pilihan) + "' is not an integer  -- >  ", end='')
            self.log.info("---> " + "Error - '" + str(pilihan) + "' is not an integer")
            if pilihan.lower()[0] == 'b':
                print('BUY forex !!')
                return int(num_choice - 1)
            elif pilihan.lower()[0] == 's':
                print('SELL forex !!')
                return int(num_choice)
            elif pilihan.lower()[0] == 'x':
                return int(99)
            elif pilihan.lower()[0] == 'q':
                return int(99)
            elif pilihan.lower()[0] == 'r':
                return int(77)
            else:
                return int(0)

    def pilihan_buy_or_sell(self, dict_position):
        self.log.info("--> " + inspect.stack()[0][3] + " started")
        n = len(dict_position)
        print(n + 1, ") BUY NEW")
        print(n + 2, ") SELL NEW")
        return {'buy': n + 1, 'sell': n + 2}

    def choice_currency(self, buysell):
        self.log.info("--> " + inspect.stack()[0][3] + " started")
        list = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        for curr in list:
            print(list.index(curr) + 1, ")", curr)
        currency = input("Chose currency to " + str(buysell) + " [ 1 - " + str(len(list)) + " ] : ")
        if currency in list:
            return currency
        elif 0 < int(currency) <= len(list):
            return list[int(currency) - 1]
        else:
            self.log.info("---> Wrong currency // currency = " + str(currency))
            return 'x'