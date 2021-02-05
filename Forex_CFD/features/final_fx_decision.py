from time import sleep
from Forex_CFD.features.final_read_datatext import ReadAllDataText
from Forex_CFD.features.fx_close_position import FxClosePosition

class FxFinalDecision(FxClosePosition, ReadAllDataText):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def close_position_CFD_ANY(self, value_EMA, tperiod, rerun):
        if rerun == 'Y':
            self.looping_check_all_currencies(value_EMA, tperiod)
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