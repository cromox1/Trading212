def currencies_to_use(level):
    dictionary = {'major' : ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"],
                  'minor' : ["EUR/GBP", "GBP/JPY", "AUD/JPY", "AUD/NZD", "CAD/JPY", "EUR/CAD", "EUR/CHF", "EUR/JPY", "EUR/NZD", "GBP/CHF"]}
    if level in dictionary:
        return dictionary[level]
    else:
        return []