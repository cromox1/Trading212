# if currency == "USD/JPY":
#     had_macd = float(0.01075)
# elif currency == "GBP/USD":
#     had_macd = float(0.00021)
# elif currency == "EUR/USD":
#     had_macd = float(0.00016)
# elif currency == "USD/CHF":
#     had_macd = float(0.00013)
# elif currency == "USD/CAD":
#     had_macd = float(0.00016)
# elif currency == "AUD/USD":
#     had_macd = float(0.00014)
# elif currency == "NZD/USD":
#     had_macd = float(0.00014)
# else:
#     had_macd = float(0.00013)

def currency_had_macd(currency='', time_period=''):
    dictionary = {'1 minute': {"USD/JPY": float(0.01070),
                               "GBP/USD": float(0.00017),
                               "EUR/USD": float(0.00013),
                               "USD/CHF": float(0.00011),
                               "USD/CAD": float(0.00013),
                               "AUD/USD": float(0.00012),
                               "NZD/USD": float(0.00012)},
                  '5 minutes': {"USD/JPY": float(0.01075),
                                "GBP/USD": float(0.00021),
                                "EUR/USD": float(0.00016),
                                "USD/CHF": float(0.00013),
                                "USD/CAD": float(0.00016),
                                "AUD/USD": float(0.00014),
                                "NZD/USD": float(0.00014)},
                  '': {'': float(0.00013)}}
    return dictionary[time_period][currency]

print(currency_had_macd("USD/CAD", '1 minute'))
print(currency_had_macd("EUR/USD", '5 minutes'))
print(currency_had_macd("USD/CAD", '5 minutes'))
print(currency_had_macd("EUR/USD", '1 minute'))
print(currency_had_macd("AUD/USD", '1 minute'))
print(currency_had_macd("USD/JPY", '5 minutes'))
print(currency_had_macd())
print(currency_had_macd("GBP/USD", '5 minutes'))
print(currency_had_macd("NZD/USD", '1 minute'))