todopoint = {'GBP/USD': 0, 'EUR/USD': 0, 'USD/JPY': 1, 'USD/CHF': 5, 'USD/CAD': -6, 'AUD/USD': 0, 'NZD/USD': 4}
open_position = {'AUD/USD': -0.15, 'GBP/USD': -5.82, 'NZD/USD': -0.17, 'USD/CAD': -2.51}

for ko,vo in open_position.items():
    if vo < -0.30:
        print('TO CLOSE/RUGI = ', ko)
    if vo > 0.50:
        print('TO CLOSE/UNTUNG = ', ko)

for kt,vt in todopoint.items():
    if vt > 0 and kt not in open_position:
        print('TO BUY // Currency = ', kt, end=' / ')
        print('Amount = ', 511 + list(todopoint.keys()).index(kt))
    elif vt < 0 and kt not in open_position:
        print('TO SELL // Currency = ', kt, end=' / ')
        print('Amount = ', 501 + list(todopoint.keys()).index(kt))

all_currencies = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]

newcurr = [i for i in all_currencies if i not in open_position]
print('NEWCURR = ', newcurr)