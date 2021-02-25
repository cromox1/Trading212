__author__ = 'cromox'

import inspect
from Forex_CFD.features.dailyfx_currency import currency_date_value
from Forex_CFD.features.read_datatext_tooltip import FxReadDataText_ToolTip

class ReadAllDataTextMACD(FxReadDataText_ToolTip):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def looping_check_currencies_MACD(self, value_EMA, tperiod, list_currency):
        self.log.info("-> " + inspect.stack()[0][3] + " started")
        grph_div_start_point = 1.331 # 1.329  # division graph of starting point? ( value = 1.28 to infinity)
        fxconvert = currency_date_value()
        print()
        print('### Scanning Data Result ( SMA =', value_EMA, ' / tperiod =' , tperiod,') ###')
        todopoint = {}
        all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
        for currency in list_currency:
            ix = all_currencies.index(currency) + 1
            print(str(ix) + ' ) ', end='')
            tindakan = self.main_collect_data_MACD(currency, value_EMA, tperiod, grph_div_start_point, fxconvert)
            todopoint.update(tindakan)
            ix += 1
        print('\nToDoPoint = ', todopoint)
        return todopoint

    def main_collect_data_MACD(self, currency, value_EMA, time_period, grph_div_start, dict_fx):
        # self.log.info("-> " + inspect.stack()[0][3] + " started")
        self.from_search_goto_specific_currency(currency)
        self.change_graph_to_candlestick()
        self.set_graph_EMA_value(value_EMA)
        self.change_graph_time_period(time_period)
        # collect data from graph

        collectdata = self.collecting_data_on_graph_MACD(grph_div_start)
        datalist = collectdata[0]
        print('DATALIST = ', datalist)
        smalist = collectdata[1]
        print('SMALIST = ', smalist)
        macdlist = collectdata[-1]
        print('MACDLIST = ', macdlist)

        tindakan = {}
        return tindakan