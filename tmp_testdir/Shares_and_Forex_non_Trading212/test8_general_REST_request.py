import requests

api_key = '28648e8b2c532b9cf935e4a213f604b9'

base_url = 'http://api.marketstack.com/v1/'

parameter = {'access_key': api_key, 'symbols': 'AAPL', 'sort' : 'DESC', 'limit' : 100, 'date_from' : '2020-11-01'}
out1 = requests.get(url = base_url + 'eod', params = parameter)

# print(out1.json())

# for k,v in out1.json().items():
#     print(v)

print()

# print(out1.json()['data'])
for i in out1.json()['data']:
    print(i)

