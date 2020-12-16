import requests
# import wget

# url1 = "https://api.londonstockexchange.com/api/gw/lse/instruments/alldata/CS1"
#
# req1 = requests.get(url1)
# print(req1.json())
# print(req1.json().get("description"))

url2 = 'https://www.worldtradingdata.com/'

req2 = requests.get(url2)
print(req2.text)


