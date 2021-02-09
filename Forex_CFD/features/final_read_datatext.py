__author__ = 'cromox'

from datetime import datetime
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
        ix = 1
        print()
        todopoint = {}
        for currency in ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]:
            print(str(ix) + ' ) (tperiod: ' + str(tperiod) + ') // ', end='')
            tindakan = self.main_collect_data(currency, value_EMA, tperiod, grph_div_start_point, fxconvert)
            todopoint.update(tindakan)
            ix += 1
        print('\nToDoPoint = ', todopoint)
        return todopoint

    def main_collect_data(self, currency, value_EMA, time_period, grph_div_start, dict_fx):
        # self.log.info("-> " + inspect.stack()[0][3] + " started")
        arini = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        gradient3 = float(datalist[-4]) - float(datalist[-5])
        ### convert to GBP
        gradient1x = 5000 * gradient1 / float(dict_fx[currency.split('/')[-1]])
        gradient2x = 5000 * gradient2 / float(dict_fx[currency.split('/')[-1]])
        gradient3x = 5000 * gradient3 / float(dict_fx[currency.split('/')[-1]])
        text1 = ''
        markah = int(time_period.split(' ')[0])
        tindakan = {}
        tindakan[currency] = 0
        if gradient3x < gradient2x < gradient1x and abs(gradient1x) >= float(0.7) and \
                float(datalist[-1]) >= float(datalist[-2]):
            text1 = text1 + ' BUY/LONG1 @' + str(datalist[-2]) + '<' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] + (1*markah)
        if gradient3x > gradient2x > gradient1x and abs(gradient1x) >= float(0.7) and \
                float(datalist[-1]) <= float(datalist[-2]):
            text1 = text1 + ' SELL/SHORT1 @' + str(datalist[-2]) + '>' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] - (1*markah)
        if float(datalist[-4]) < float(datalist[-3]) < float(datalist[-2]) and abs(gradient1x) >= float(0.7) \
                and float(datalist[-1]) >= float(datalist[-2]):
            text1 = text1 + ' BUY/LONG2 @' + str(datalist[-2]) + '<' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] + (1*markah)
        if float(datalist[-4]) > float(datalist[-3]) > float(datalist[-2]) and abs(gradient1x) >= float(0.7) \
                and float(datalist[-1]) <= float(datalist[-2]):
            text1 = text1 + ' SELL/SHORT2 @' + str(datalist[-2]) + '>' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] - (1*markah)
        if float(datalist[-5]) <= float(emalist[-5]) and float(datalist[-2]) >= float(emalist[-2]) \
                and float(datalist[-1]) >= float(datalist[-2]):
            text1 = text1 + ' BUY/LONG3 @' + str(datalist[-2]) + '<' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] + (1*markah)
        if float(datalist[-5]) > float(emalist[-5]) + float(0.00075) and abs(float(datalist[-2]) - float(emalist[-2])) \
                < float(0.00025) and float(datalist[-1]) <= float(datalist[-2]):
            text1 = text1 + ' SELL/SHORT3 @' + str(datalist[-2]) + '>' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] - (1*markah)
        if float(datalist[-4]) < float(datalist[-3]) < float(datalist[-2]) < float(datalist[-1]):
            text1 = text1 + ' BUY/LONG4 @' + str(datalist[-2]) + '<' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] + (1*markah)
        if float(datalist[-4]) > float(datalist[-3]) > float(datalist[-2]) > float(datalist[-1]):
            text1 = text1 + ' SELL/SHORT4 @' + str(datalist[-2]) + '>' + str(datalist[-1])
            tindakan[currency] = tindakan[currency] - (1*markah)
        print('TIME ' + str(arini) + ' # GRADIENT for ' + currency + ' =', str("%.5f" % round(gradient3, 5)), '/',
              str("%.6f" % round(gradient3x, 6)),
              '//', str("%.5f" % round(gradient2, 5)), '/', str("%.6f" % round(gradient2x, 6)),
              '//', str("%.5f" % round(gradient1, 5)), '/', str("%.6f" % round(gradient1x, 6)), '#', text1)
        return tindakan