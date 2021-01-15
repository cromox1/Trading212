import requests

api_key = '28648e8b2c532b9cf935e4a213f604b9'

base_url = 'http://api.marketstack.com/v1/'

parameter = {'access_key': api_key, 'limit' : 50, 'date_from' : '2020-11-01', 'offset' : 10, 'code' : 'GBP'}
out1 = requests.get(url = base_url + 'currencies', params = parameter)

print()
print(out1.json())

print()
i = 1
for value in out1.json()['data']:
    print(i, value)
    i += 1

# api_result = requests.get('http://api.marketstack.com/v1/tickers/aapl/eod', params = {'access_key': api_key})
api_result = requests.get('http://api.marketstack.com/v1/eod', params = {'access_key': api_key, 'symbols' : "MSFT"})

api_response = api_result.json()
print(api_response)
# eod_data = api_response['data']['eod']
eod_data = api_response['data']
print(eod_data)

print()
i = 1
for stock_data in eod_data:
    print(i, "Ticker %s has a day high of  %s on %s" % (stock_data['symbol'], stock_data['high'], stock_data['date']))
    i += 1