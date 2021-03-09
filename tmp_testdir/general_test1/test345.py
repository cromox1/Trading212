from datetime import datetime
from time import sleep

url1 = "https://live.trading212.com/"
url2 = "https://demo.trading212.com/"

print('word = ', url1.split('//')[-1].split(".")[0])
print('word = ', url2.split('//')[-1].split(".")[0])
print(datetime.now())
sleep(0.5)
print(datetime.now())

list1 = ["a", "b", "b", "c", "c"]
print(list1)

#
# print(len(list2))
#
# print(list2[3])
# print(list2[3][0])
# print(list2[3][1])
# print()
#
#
# dict_position = {1: ['USD/JPY', 0], 2: ['GBP/USD', 0], 3: ['GBP/USD', 1], 4: ['EUR/USD', 0], 5: ['EUR/USD', 1]}
# def pilihan_buy_or_sell(dict_position):
#     n = len(dict_position)
#     print(n + 1, " ) BUY NEW")
#     print(n + 2, " ) SELL NEW")
#     return {n + 1 : 'buy', n + 2 : 'sell'}
#
# dict = pilihan_buy_or_sell(dict_position)

# print(dict)

# listx = ["GBP/USD", "EUR/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"]
#
# print(listx)
# for curr in listx:
#     print(listx.index(curr) + 1, ")", curr)

# list2 = {1: ['USD/JPY', 0], 2: ['GBP/USD', 0], 3: ['GBP/USD', 1], 4: ['EUR/USD', 0], 5: ['EUR/USD', 1]}
#
# for k,v in list2.items():
#     # print('k = ', k , ' / v = ', v)
#     print(k, ') ', v[0], ' / position = ' , v[1])
#
# print(list2.values())
#
# if "GBP/USD" not in list2.values():
#     print('OK')
# else:
#     print('NOT_OK')
#

# DICT1 =  {1: ['USD/JPY', 0], 2: ['AUD/USD', 0], 3: ['USD/JPY', 0], 4: ['EUR/USD', 0], 5: ['EUR/USD', 0]}
# 1 ) name = USD/JPY / quantity = 1000 / direction = BUY / averagePrice = 103.82700 / currentPrice = 103.772 / margin = - / ppl = -0.39 /
# 2 ) name = AUD/USD / quantity = 501 / direction = SELL / averagePrice = 0.7712700 / currentPrice = 0.77157 / margin = 0.56 / ppl = -0.11 /
# 3 ) name = USD/JPY / quantity = 1000 / direction = BUY / averagePrice = 103.82700 / currentPrice = 103.772 / margin = - / ppl = -0.39 /
# 4 ) name = EUR/USD / quantity = 6000 / direction = BUY / averagePrice = 1.2181700 / currentPrice = 1.21673 / margin = 10.67 / ppl = -6.35 /
# 5 ) name = EUR/USD / quantity = 6000 / direction = BUY / averagePrice = 1.2181700 / currentPrice = 1.21673 / margin = 10.67 / ppl = -6.35 /

print('MY MAIN TEST ----- ')

instruments = ['USD/JPY', 'AUD/USD', 'USD/JPY', 'EUR/USD', 'EUR/USD']

print(instruments)
for i in range(len(instruments)):
    print(i + 1, ")", instruments[i])

dict1 = {}
ix = 1
jy = 0
for text in instruments:
    if text not in [x[0] for x in list(dict1.values())]:
        jy = 0
        dict1[ix] = [text, jy]
        print("DICT1 [ ", ix, " ] ", dict1)
    else:
        jy += 1
        dict1[ix] = [text, jy]
        print("DICT2 [ ", ix, " ] ", dict1)
    ix += 1
print("DICT_ALL = ", dict1)
print(list(dict1.values()))
print([x[0] for x in list(dict1.values())])

print()
def test_pilihan(num_choice):
    pilihan = input('PILIHAN = ')
    if pilihan.lower()[0] == 'b':
        return int(num_choice - 2)
    elif pilihan.lower()[0] == 's':
        return int(num_choice - 1)
    elif pilihan.lower()[0] == 'x':
        return int(99)
    else:
        return int(0)

num_choice = 7
cubaan = test_pilihan(num_choice)
print('CHOICE = ', num_choice, ' / NO PILIHAN = ', cubaan)

dict3 = {}
print('len_dict3 = ', len(dict3))
dict4 = {1: 'a'}
print('len_dict4 = ',len(dict4))