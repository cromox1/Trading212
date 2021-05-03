__author__ = 'cromox'

import inspect
from Forex_CFD.features.dailyfx_currency import currency_date_value
from Forex_CFD.features.read_datatext_tooltip import FxReadDataText_ToolTip

class ReadAllDataText(FxReadDataText_ToolTip):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def looping_check_all_currencies(self, value_EMA, tperiod):
        self.log.info("-> " + inspect.stack()[0][3] + " started")
        grph_div_start_point = 1.331 # 1.329  # division graph of starting point? ( value = 1.28 to infinity)
        fxconvert = currency_date_value()
        print()
        todopoint = {}
        # all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        all_currencies = self.currencies_to_use('major')
        tocheck_currencies = all_currencies
        for currency in tocheck_currencies:
            ix = all_currencies.index(currency) + 1
            print(str(ix) + ' ) (tperiod: ' + str(tperiod) + ') // ', end='')
            tindakan = self.main_collect_data(currency, value_EMA, tperiod, grph_div_start_point, fxconvert)
            todopoint.update(tindakan)
            ix += 1
        print('\nToDoPoint = ', todopoint)
        return todopoint

    def looping_check_currencies(self, value_EMA, tperiod, list_currency):
        self.log.info("-> " + inspect.stack()[0][3] + " started")
        grph_div_start_point = 1.331 # 1.329  # division graph of starting point? ( value = 1.28 to infinity)
        fxconvert = currency_date_value()
        print()
        print('### Scanning Data Result ( SMA =', value_EMA, ' / tperiod =' , tperiod,') ###')
        todopoint = {}
        # all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        all_currencies = self.currencies_to_use('major')
        for currency in list_currency:
            ix = all_currencies.index(currency) + 1
            print(str(ix) + ' ) ', end='')
            tindakan = self.main_collect_data(currency, value_EMA, tperiod, grph_div_start_point, fxconvert)
            todopoint.update(tindakan)
            ix += 1
        print('\nToDoPoint = ', todopoint)
        return todopoint

    def main_collect_data(self, currency, value_EMA, time_period, grph_div_start, dict_fx):
        # self.log.info("-> " + inspect.stack()[0][3] + " started")
        self.from_search_goto_specific_currency(currency)
        self.change_graph_to_candlestick()
        self.set_graph_EMA_value(value_EMA)
        self.change_graph_time_period(time_period)
        # collect data from graph
        collectdata = self.collecting_data_on_graph(grph_div_start)
        datalist = collectdata[0]
        emalist = collectdata[-1]
        gradient1 = float(datalist[-2]) - float(datalist[-3])
        gradient2 = float(datalist[-3]) - float(datalist[-4])
        gradient3 = float(datalist[-5]) - float(datalist[-6])
        ### convert to GBP
        gradient1x = 5000 * gradient1 / float(dict_fx[currency.split('/')[-1]])
        gradient2x = 5000 * gradient2 / float(dict_fx[currency.split('/')[-1]])
        gradient3x = 5000 * gradient3 / float(dict_fx[currency.split('/')[-1]])
        text1 = ''
        # markah = int(time_period.split(' ')[0])
        if int(time_period.split(' ')[0]) == 1:
            markah = 1
        elif int(time_period.split(' ')[0]) == 5:
            markah = 1.71
        elif int(time_period.split(' ')[0]) == 10:
            markah = 1.72
        else:
            markah = 2
        tindakan = {}
        tindakan[currency] = 0
        nearema1 = float(abs(float(datalist[-1]) - float(emalist[-1])))
        nearema2 = float(abs(float(datalist[-2]) - float(emalist[-2])))

        #### NEWLY CONDITIONS
        if currency == "USD/JPY":
            floatjauh = float(0.0595)
            floatdekat = float(0.0123)
        else:
            floatjauh = float(0.000595)
            floatdekat = float(0.000123)
        indexbesar = float(0.77)
        # 1
        if float(datalist[-4]) < float(datalist[-3]) < float(datalist[-2]) <= float(datalist[-1]) and \
                float(datalist[-1]) <= float(emalist[-1]):
            tindakan[currency] = tindakan[currency] + int(3 * markah)
            text1 = text1 + 'BUY1 '
        if float(datalist[-4]) > float(datalist[-3]) > float(datalist[-2]) >= float(datalist[-1]) and \
                float(datalist[-1]) > float(emalist[-1]) + floatdekat:
            tindakan[currency] = tindakan[currency] - int(2 * markah)
            text1 = text1 + 'SELL1 '
        # 2
        if gradient3x < gradient2x < gradient1x and float(datalist[-1]) <= float(emalist[-1]):
            tindakan[currency] = tindakan[currency] + int(2 * markah)
            text1 = text1 + 'BUY2 '
        if gradient3x > gradient2x > gradient1x and float(datalist[-1]) > float(emalist[-1]) + floatdekat:
            tindakan[currency] = tindakan[currency] - int(2 * markah)
            text1 = text1 + 'SELL2 '
        # 3
        if float(datalist[-1]) > float(datalist[-2]) and abs(gradient1x) >= indexbesar:
            tindakan[currency] = tindakan[currency] + int(2 * markah)
            text1 = text1 + 'BUY3 '
        if float(datalist[-1]) < float(datalist[-2]) and abs(gradient1x) >= indexbesar:
            tindakan[currency] = tindakan[currency] - int(2 * markah)
            text1 = text1 + 'SELL3 '
        # 4
        if nearema1 < floatdekat and float(datalist[-1]) < float(emalist[-1]) and abs(gradient1x) >= indexbesar:
            tindakan[currency] = tindakan[currency] + int(3 * markah)
            text1 = text1 + 'BUY4 '
        if nearema1 > floatjauh and float(datalist[-1]) > float(emalist[-1]) and abs(gradient1x) >= indexbesar:
            tindakan[currency] = tindakan[currency] - int(3 * markah)
            text1 = text1 + 'SELL4 '
        # 5
        if float(datalist[-5]) < float(emalist[-5]) and float(datalist[-2]) >= float(emalist[-2]) \
            and float(datalist[-1]) >= float(datalist[-2]):
            tindakan[currency] = tindakan[currency] + int(2 * markah)
            text1 = text1 + 'BUY5 '
        if float(datalist[-5]) > float(emalist[-5]) + floatjauh and float(datalist[-2]) > float(emalist[-2]) \
            and float(datalist[-1]) <= float(datalist[-2]):
            tindakan[currency] = tindakan[currency] - int(2 * markah)
            text1 = text1 + 'SELL5 '
        # 6
        if nearema2 > nearema1 and float(datalist[-1]) > float(datalist[-2]):
            tindakan[currency] = tindakan[currency] + int(2 * markah)
            text1 = text1 + 'BUY6 '
        if nearema2 > nearema1 and float(datalist[-1]) < float(datalist[-2]):
            tindakan[currency] = tindakan[currency] - int(2 * markah)
            text1 = text1 + 'SELL6 '
        # 7
        if float(datalist[-1]) < float(emalist[-1]) - floatjauh and abs(gradient1x) >= indexbesar:
            tindakan[currency] = tindakan[currency] + int(3 * markah)
            text1 = text1 + 'BUY7 '
        if float(datalist[-1]) > float(emalist[-1]) + floatjauh and abs(gradient1x) >= indexbesar:
            tindakan[currency] = tindakan[currency] - int(2 * markah)
            text1 = text1 + 'SELL7 '

        ######
        print(' # Grade:', str("%.5f" % round(gradient3, 5)), '/',
              str("%.6f" % round(gradient3x, 6)),
              '//', str("%.5f" % round(gradient2, 5)), '/', str("%.6f" % round(gradient2x, 6)),
              '//', str("%.5f" % round(gradient1, 5)), '/', str("%.6f" % round(gradient1x, 6)), '#', text1)
        return tindakan