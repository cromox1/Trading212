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
        # grph_div_start_point = 2
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
        # print('\nToDoPoint = ', todopoint)
        return todopoint

    def main_collect_data_MACD(self, currency, value_EMA, time_period, grph_div_start, dict_fx):
        # self.log.info("-> " + inspect.stack()[0][3] + " started")
        self.from_search_goto_specific_currency(currency)
        self.change_graph_to_candlestick()
        self.set_graph_EMA_value(value_EMA)
        self.change_graph_time_period(time_period)
        # beginning value
        tindakan = {}
        tindakan[currency] = 0
        ## MACD filter limit
        if currency == "USD/JPY":
            had_macd = float(0.01075)
        elif currency == "GBP/USD":
            had_macd = float(0.00021)
        elif currency == "EUR/USD":
            had_macd = float(0.00016)
        elif currency == "USD/CHF":
            had_macd = float(0.00010)
        elif currency == "USD/CAD":
            had_macd = float(0.00016)
        elif currency == "AUD/USD":
            had_macd = float(0.00014)
        elif currency == "NZD/USD":
            had_macd = float(0.00014)
        else:
            had_macd = float(0.00013)

        collectdata = self.collecting_data_on_graph_MACD(grph_div_start)
        macdlist1 = collectdata
        macdlist = [float(i) for i in macdlist1]
        MACD_point = []
        for i in macdlist:
            if i < -1*had_macd:
                MACD_point.append(-2)
            elif -1*had_macd <= i < -0.3*had_macd:
                MACD_point.append(-1)
            elif 0.3*had_macd < i <= had_macd:
                MACD_point.append(1)
            elif i > had_macd:
                MACD_point.append(2)
            else:
                MACD_point.append(0)

        print('// MACD:', MACD_point, '/ last', macdlist1[-1], '// HAD', -1*had_macd, had_macd, end=' ')
        tindakan[currency] =  MACD_point[-1]
        if macdlist[-2] > macdlist[-1] and macdlist[-2] > macdlist[-3] and macdlist[-2] > 0 and macdlist[-1] > 0:
            print('// MACD_high1', macdlist1[-3], macdlist1[-2], macdlist1[-1], end=' ')
            tindakan[currency] =  tindakan[currency] + 5
        elif macdlist[-2] > macdlist[-1] and macdlist[-2] > macdlist[-3] and macdlist[-2] > 0:
            print('// MACD_high2', macdlist1[-2], end=' ')
            tindakan[currency] =  tindakan[currency] + 3
        elif macdlist[-3] > macdlist[-2] and macdlist[-3] > macdlist[-4] and macdlist[-3] > 0:
            print('// MACD_high3', macdlist1[-3], end=' ')
            tindakan[currency] =  tindakan[currency] + 3
        elif macdlist[-2] > 0 and macdlist[-1] < 0:
            print('// MACD_high4A', macdlist1[-2], end=' ')
            tindakan[currency] = tindakan[currency] + 4
        elif macdlist[-3] > 0 and macdlist[-2] < 0 and macdlist[-1] < 0:
            print('// MACD_high4B', macdlist1[-3], end=' ')
            tindakan[currency] = tindakan[currency] + 4
        if macdlist[-2] < macdlist[-1] and macdlist[-2] < macdlist[-3] and macdlist[-2] < 0 and macdlist[-1] < 0:
            print('// MACD_low1', macdlist1[-3], macdlist1[-2], macdlist1[-1], end=' ')
            tindakan[currency] =  tindakan[currency] - 5
        elif macdlist[-2] < macdlist[-1] and macdlist[-2] < macdlist[-3] and macdlist[-2] < 0:
            print('// MACD_low2', macdlist1[-2], end=' ')
            tindakan[currency] =  tindakan[currency] - 3
        elif macdlist[-3] < macdlist[-2] and macdlist[-3] < macdlist[-4] and macdlist[-3] < 0:
            print('// MACD_low3', macdlist1[-3], end=' ')
            tindakan[currency] =  tindakan[currency] - 3
        elif macdlist[-2] < 0 and macdlist[-1] > 0:
            print('// MACD_low4A', macdlist1[-2], end=' ')
            tindakan[currency] = tindakan[currency] - 4
        elif macdlist[-3] < 0 and macdlist[-2] > 0 and macdlist[-1] > 0:
            print('// MACD_low4B', macdlist1[-3], end=' ')
            tindakan[currency] = tindakan[currency] - 4

        print('// POINT =', tindakan[currency])
        return tindakan