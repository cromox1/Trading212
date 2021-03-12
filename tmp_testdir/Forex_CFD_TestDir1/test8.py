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

# def currency_had_macd(currency='', time_period=''):
#     dictionary = {'1 minute': {"USD/JPY": float(0.00540),
#                                "GBP/USD": float(0.00011),
#                                "EUR/USD": float(0.00006),
#                                "USD/CHF": float(0.00005),
#                                "USD/CAD": float(0.00006),
#                                "AUD/USD": float(0.00005),
#                                "NZD/USD": float(0.00005),
#                                '': float(0.00006)},
#                   '5 minutes': {"USD/JPY": float(0.01075),
#                                 "GBP/USD": float(0.00021),
#                                 "EUR/USD": float(0.00016),
#                                 "USD/CHF": float(0.00013),
#                                 "USD/CAD": float(0.00016),
#                                 "AUD/USD": float(0.00014),
#                                 "NZD/USD": float(0.00014),
#                                 '': float(0.00013)},
#                   '': {'': float(0.00010)}}
#     return dictionary[time_period][currency]

# def currency_had_macd(currency=None, time_period=None):
#     default_x = str('0.000123')
#     dictionary = {'1 minute': {"USD/JPY": str('0.00540'),
#                                "GBP/USD": str('0.00011'),
#                                "EUR/USD": str('0.00006'),
#                                "USD/CHF": str('0.00005'),
#                                "USD/CAD": str('0.00006'),
#                                "AUD/USD": str('0.00005'),
#                                "NZD/USD": str('0.00005')},
#                   '5 minutes': {"USD/JPY": str('0.01075'),
#                                 "GBP/USD": str('0.00021'),
#                                 "EUR/USD": str('0.00016'),
#                                 "USD/CHF": str('0.00013'),
#                                 "USD/CAD": str('0.00016'),
#                                 "AUD/USD": str('0.00014'),
#                                 "NZD/USD": str('0.00014')}}
#     if time_period in dictionary and currency in dictionary[time_period]:
#         x = dictionary[time_period][currency]
#     else:
#         x = default_x
#     return x

def currency_had_macd(currency='', time_period=''):
    dictionary = {'1 minute': {"USD/JPY": float(0.00540),
                               "GBP/USD": float(0.00011),
                               "EUR/USD": float(0.00006),
                               "USD/CHF": float(0.00005),
                               "USD/CAD": float(0.00006),
                               "AUD/USD": float(0.00005),
                               "NZD/USD": float(0.00005)},
                  '5 minutes': {"USD/JPY": float(0.01075),
                                "GBP/USD": float(0.00021),
                                "EUR/USD": float(0.00016),
                                "USD/CHF": float(0.00013),
                                "USD/CAD": float(0.00016),
                                "AUD/USD": float(0.00014),
                                "NZD/USD": float(0.00014)}}
    if time_period in dictionary and currency in dictionary[time_period]:
        return dictionary[time_period][currency]
    elif time_period in dictionary and currency not in dictionary[time_period]:
        if time_period == list(dictionary.keys())[0]:
            return float(0.00006)
        elif time_period == list(dictionary.keys())[1]:
            return float(0.00013)
        else:
            return float(0.00010)
    else:
        return float(0)

print(1, "USD/CAD", '1 minute', currency_had_macd("USD/CAD", '1 minute'))
print(2, "EUR/USD", '5 minutes', currency_had_macd("EUR/USD", '5 minutes'))
print(3, "USD/CAD", '5 minutes', currency_had_macd("USD/CAD", '5 minutes'))
print(4, "EUR/USD", '1 minute', currency_had_macd("EUR/USD", '1 minute'))
print(5, "AUD/USD", '1 minute', currency_had_macd("AUD/USD", '1 minute'))
print(6, "USD/JPY", '5 minutes', currency_had_macd("USD/JPY", '5 minutes'))
print(7, ' ', ' ', currency_had_macd())
print(8, "GBP/USD", '5 minutes', currency_had_macd("GBP/USD", '5 minutes'))
print(9, "NZD/USD", '1 minute', currency_had_macd("NZD/USD", '1 minute'))
print(10, "XXX/YYY", '5 minutes', currency_had_macd("XXX/YYY", '5 minutes'))
print(11, "XXX/YYY", '10 minutes', currency_had_macd("XXX/YYY", '10 minutes'))

dictionary1 = {'1 minute': {"USD/JPY": float(0.00540),
                               "GBP/USD": float(0.00011),
                               "EUR/USD": float(0.00006),
                               "USD/CHF": float(0.00005),
                               "USD/CAD": float(0.00006),
                               "AUD/USD": float(0.00005),
                               "NZD/USD": float(0.00005)},
                  '5 minutes': {"USD/JPY": float(0.01075),
                                "GBP/USD": float(0.00021),
                                "EUR/USD": float(0.00016),
                                "USD/CHF": float(0.00013),
                                "USD/CAD": float(0.00016),
                                "AUD/USD": float(0.00014),
                                "NZD/USD": float(0.00014)}}

print(21, 'TEST1', list(dictionary1.keys())[0])
print(22, 'TEST2', list(dictionary1.keys())[1])