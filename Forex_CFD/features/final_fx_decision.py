__author__ = 'cromox'

from time import sleep
# from datetime import datetime
# from pytz import timezone
import inspect
from Forex_CFD.features.final_read_datatext import ReadAllDataText
from Forex_CFD.features.final_read_datatext_MACD import ReadAllDataTextMACD
from Forex_CFD.features.fx_close_position import FxClosePosition

class FxFinalDecision(FxClosePosition, ReadAllDataText, ReadAllDataTextMACD):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def mergeDict(self, dict1, dict2):
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = value + dict1[key]
        return dict3

    def mergeDictStrongOne(self, dict1, dict2):
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = value + 2 * dict1[key]
        return dict3

    def mergeDictNoZero(self, dict1, dict2):
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                if dict1[key] > 0 > dict2[key]:
                    dict3[key] = 0
                elif dict1[key] < 0 < dict2[key]:
                    dict3[key] = 0
                elif -4 < dict1[key] < 4:
                    dict3[key] = 0
                else:
                    dict3[key] = value + dict1[key]
        return dict3

    def close_position_elementid(self, id_element):
        xpathto = f"//table[@data-dojo-attach-point='tableNode']//tr[@id='{id_element}']//div[@class='close-icon svg-icon-holder']"
        self.driver.find_elements_by_xpath(xpathto)[0].click()
        self.driver.find_elements_by_xpath(f"//span[@class='btn btn-primary' and text()='OK']")[0].click()
        sleep(2)

    def direction_elementid(self, id_element):
        xpathto = f"//table[@data-dojo-attach-point='tableNode']//tr[@id='{id_element}']//td[contains(@class,'direction')]"
        return  self.driver.find_elements_by_xpath(xpathto)[0].text

    def close_position_pilihan_elementid(self, dict1, dict2, pilihan):
        print(' -- > Close Position [', str(pilihan), '] =', dict2[int(pilihan)])
        confirmation = input("Confirm to CLOSE position [ " + str(pilihan) + " ] ? [ Y / N ] : ")
        id_ele = dict1[int(pilihan)]
        if confirmation.lower() == 'y':
            self.close_position_elementid(id_ele)
        else:
            print("CHANGE MIND!! - Didn't CLOSE [", str(pilihan), '] =', dict2[int(pilihan)])

    def buy_currency_with_amount(self, currency):
        amount = input('Amount to BUY (min 500) : ')
        try:
            if currency != 'x':
                self.buy_stock(currency, int(amount))
            else:
                print('Wrong currency')
        except:
            print('ERROR on BUY')
            self.log.info("---> ERROR on BUY // amount = " + str(amount))

    def sell_currency_with_amount(self, currency):
        amount = input('Amount to SELL (min 500) : ')
        try:
            if currency != 'x':
                self.sell_stock(currency, int(amount))
            else:
                print('Wrong currency')
        except:
            print('ERROR on SELL')
            self.log.info("---> ERROR on SELL // amount = " + str(amount))

    def close_position_CFD_ANY(self, value_EMA, tperiod, rerun):
        self.log.info("-> " + inspect.stack()[0][3] + " started")
        if rerun == 'Y':
            self.looping_check_all_currencies(value_EMA, tperiod)
        list_choice = self.list_CFD_open_position()
        dict1 = list_choice[0]
        dict2 = list_choice[1]
        buy_sell_dict = self.pilihan_buy_or_sell(dict1)
        number_of_choice = len(dict1) + 2
        pilihan = self.pilihan_to_close_position(number_of_choice)
        try:
            rerun = 'N'
            if len(dict1) > 0 and 0 < int(pilihan) <= len(dict1):
                self.close_position_pilihan_elementid(dict1, dict2, pilihan)
            elif int(pilihan) == buy_sell_dict['buy']:
                currency = self.choice_currency("BUY")
                self.buy_currency_with_amount(currency)
            elif int(pilihan) == buy_sell_dict['sell']:
                currency = self.choice_currency("SELL")
                self.sell_currency_with_amount(currency)
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

    def close_position_CFD_ANY_auto(self, value_EMA, list_tperiod):
        self.log.info("-> " + inspect.stack()[0][3] + " started")
        ### ni section nak tengok apa yg kita ada skrg
        list_choice = self.list_CFD_open_position()
        dict1 = list_choice[0]
        dict2 = list_choice[1]
        masastart = list_choice[2]
        open_position = {}
        newdict1 = {}
        for kk,vv in dict2.items():
            newkk = vv.split(' ')[0]
            newvv1 = vv.split('/')[-2].replace(' ','')
            newvv = round(float(newvv1), 2)
            newvvid = dict1[kk]
            open_position.update({newkk: newvv})
            newdict1.update({newkk: newvvid})

        # ### ni section checking whatever status of the current Forex/CFD
        # all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        # list_currencies = [i for i in all_currencies if i not in open_position]
        # list_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        list_currencies = self.currencies_to_use('major')     # all_currencies
        todopoint = {}
        tocloseone = {}
        if len(list_currencies) >= 1:
            for tperiod in list_tperiod:
                newpoint = self.looping_check_currencies(value_EMA, tperiod, list_currencies)
                todopoint = self.mergeDictNoZero(todopoint, newpoint)
                tocloseone = self.mergeDictStrongOne(tocloseone, newpoint)
        return todopoint, open_position, tocloseone, newdict1, masastart

    def close_position_CFD_ANY_auto_MACD(self, value_EMA, tperiod):
        self.log.info("-> " + inspect.stack()[0][3] + " started")
        ### ni section nak tengok apa yg kita ada skrg
        list_choice = self.list_CFD_open_position()
        dict1 = list_choice[0]
        dict2 = list_choice[1]
        masastart = list_choice[2]
        open_position = {}
        newdict1 = {}
        for kk,vv in dict2.items():
            newkk = vv.split(' ')[0]
            newvv1 = vv.split('/')[-2].replace(' ','')
            newvv = round(float(newvv1), 2)
            newvvid = dict1[kk]
            open_position.update({newkk: newvv})
            newdict1.update({newkk: newvvid})

        # ### ni section checking whatever status of the current Forex/CFD
        # all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        # list_currencies = [i for i in all_currencies if i not in open_position]
        # list_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        list_currencies = self.currencies_to_use('major')   # all_currencies
        todopoint = {}
        tocloseone = {}
        if len(list_currencies) >= 1:
            newpoint = self.looping_check_currencies_MACD(value_EMA, tperiod, list_currencies)
            todopoint = self.mergeDictNoZero(todopoint, newpoint)
            tocloseone = self.mergeDictStrongOne(tocloseone, newpoint)
        return todopoint, open_position, tocloseone, newdict1, masastart

    def close_position_CFD_ANY_manual_MACD(self, value_EMA, tperiod, rerun):
        # self.log.info("-> " + inspect.stack()[0][3] + " started")
        list_currencies = self.currencies_to_use('major')  # all_currencies
        todopoint = {}
        tocloseone = {}
        if rerun == 'Y' and len(list_currencies) >= 1:
            newpoint = self.looping_check_currencies_MACD(value_EMA, tperiod, list_currencies)
            todopoint = self.mergeDictNoZero(todopoint, newpoint)
            tocloseone = self.mergeDictStrongOne(tocloseone, newpoint)
            print('\nCHK1 -- \n todopoint =', todopoint, '\n tocloseone =', tocloseone)
        list_choice = self.list_CFD_open_position()
        dict1 = list_choice[0]
        dict2 = list_choice[1]
        masastart = list_choice[2]
        buy_sell_dict = self.pilihan_buy_or_sell(dict1)
        number_of_choice = len(dict1) + 2
        pilihan = self.pilihan_to_close_position(number_of_choice)
        print('\nCHK2 -- dict1 =', dict1, ' / len(dict1) =', len(dict1))
        print('\nCHK3 -- dict2 =', dict2, ' / len(dict2) =', len(dict2))
        print('\nCHK4 -- pilihan =', pilihan)
        if len(dict1) > 0:
            try:
                rerun = 'N'
                if len(dict1) > 0 and 0 < int(pilihan) <= len(dict1):
                    self.close_position_pilihan_elementid(dict1, dict2, pilihan)
                elif int(pilihan) == buy_sell_dict['buy']:
                    currency = self.choice_currency("BUY")
                    self.buy_currency_with_amount(currency)
                elif int(pilihan) == buy_sell_dict['sell']:
                    currency = self.choice_currency("SELL")
                    self.sell_currency_with_amount(currency)
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
        return pilihan, todopoint, masastart, rerun