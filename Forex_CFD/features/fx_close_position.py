from time import sleep
from datetime import datetime
from Forex_CFD.utilities.util import Util
from Forex_CFD.features.fx_buysell import FxBuySell

class FxClosePosition(FxBuySell):

    def __init__(self, driver):
        super(FxClosePosition, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def list_CFD_open_position(self):
        instrument_list = self.driver.find_elements_by_xpath('//table[@data-dojo-attach-point="tableNode"]//tr')
        sleep(1)
        free_fund = self.driver.find_elements_by_xpath(
            '//*[@id="equity-free"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
        total_fund = self.driver.find_elements_by_xpath(
            '//*[@id="equity-total"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
        result = self.driver.find_elements_by_xpath(
            '//*[@id="equity-ppl"]/span[@data-dojo-attach-point="valueNode"]')[-1].text.replace(' ', '')
        # "%.5f" % round(float(VALUE)), 5)
        myDFD = "%.2f" % round((float(total_fund.replace('£', '')) - float(result.replace('£', ''))), 2)
        arini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('\n# No of Instruments = ', len(instrument_list), ' // TIME_RUN =', arini, '// DFD = ', '£' + str(myDFD),
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
        return dict1, dict2

    def pilihan_to_close_position(self, num_choice):
        # pilihan = 0
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
        n = len(dict_position)
        print(n + 1, ") BUY NEW")
        print(n + 2, ") SELL NEW")
        return {'buy': n + 1, 'sell': n + 2}

    def choice_currency(self, buysell):
        list = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        for curr in list:
            print(list.index(curr) + 1, ")", curr)
        currency = input("Chose currency to " + str(buysell) + " [ 1 - " + str(len(list)) + " ] : ")
        if currency in list:
            return currency
        elif 0 < int(currency) <= len(list):
            return list[int(currency) - 1]
        else:
            return 'x'

    def close_position_CFD_ANY(self, value_EMA, tperiod, rerun):
        if rerun == 'Y':
            ## TODO
            driver = looping_check_all_currencies(driver, value_EMA, tperiod)    #### 2 errors
        list_choice = self.list_CFD_open_position()
        dict1 = list_choice[0]
        dict2 = list_choice[-1]
        buy_sell_dict = self.pilihan_buy_or_sell(dict1)
        number_of_choice = len(dict1) + 2
        pilihan = self.pilihan_to_close_position(number_of_choice)
        try:
            rerun = 'N'
            if len(dict1) > 0 and 0 < int(pilihan) <= len(dict1):
                print(' -- > Close Position [', str(pilihan), '] =', dict2[int(pilihan)])
                confirmation = input("Confirm to CLOSE position [ " + str(pilihan) + " ] ? [ Y / N ] : ")
                id_ele = dict1[int(pilihan)]
                if confirmation.lower() == 'y':
                    xpathto = f"//table[@data-dojo-attach-point='tableNode']//tr[@id='{id_ele}']//div[@class='close-icon svg-icon-holder']"
                    self.driver.find_elements_by_xpath(xpathto)[0].click()
                    self.driver.find_elements_by_xpath(f"//span[@class='btn btn-primary' and text()='OK']")[0].click()
                    sleep(2)
                else:
                    print("CHANGE MIND!! - Didn't CLOSE [", str(pilihan), '] =', dict2[int(pilihan)])
            elif int(pilihan) == buy_sell_dict['buy']:
                currency = self.choice_currency("BUY")
                amount = input('Amount to BUY (min 500) : ')
                try:
                    if currency != 'x':
                        self.buy_stock(currency, int(amount))
                    else:
                        print('Wrong currency')
                except:
                    print('ERROR on BUY')
            elif int(pilihan) == buy_sell_dict['sell']:
                currency = self.choice_currency("SELL")
                amount = input('Amount to SELL (min 500) : ')
                try:
                    if currency != 'x':
                        self.sell_stock(currency, int(amount))
                    else:
                        print('Wrong currency')
                except:
                    print('ERROR on SELL')
            elif int(pilihan) == 99:
                print("You choose - QUIT/EXIT !!")
                self.driver.close()
            elif int(pilihan) == 77:
                print("You choose - RERUN !!")
                rerun = 'Y'
            else:
                print("Out of range")
            return pilihan, rerun
        except:
            rerun = 'N'
            print("Nothing TODO")
            return pilihan, rerun