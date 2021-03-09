dict1 = {'a' : 1}
dict2 = {'b' : 2}
dict3 = {'c' : 0}
dictall = {}
dictall.update(dict1)
print(dictall)
dictall.update(dict2)
print(dictall)
dictall.update(dict3)
print(dictall)

# ToDoPoint1 =  {'GBP/USD': 0, 'EUR/USD': 2, 'USD/JPY': 0, 'USD/CHF': 0, 'USD/CAD': 0, 'AUD/USD': 0, 'NZD/USD': 0}
ToDoPoint1 =  {'GBP/USD': -2, 'EUR/USD': -4, 'USD/JPY': -2, 'USD/CHF': 2, 'USD/CAD': 2, 'AUD/USD': -2, 'NZD/USD': -2}
ToDoPoint2 =  {'GBP/USD': -8, 'EUR/USD': 0, 'USD/JPY': 0, 'USD/CHF': 0, 'USD/CAD': 5, 'AUD/USD': 0, 'NZD/USD': 10}

# def mergeDict(dict1, dict2):
#    dict3 = {**dict1, **dict2}
#    for key, value in dict3.items():
#        if key in dict1 and key in dict2:
#                dict3[key] = value + dict1[key]
#    return dict3
#
# dict3 = mergeDict(ToDoPoint1, ToDoPoint2)
# print('Dict3 = ', dict3)


def mergeDictStrongOne(dict1, dict2):
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            # dict3[key] = value + 2 * dict1[key]
            dict3[key] = 2 * dict1[key] + dict2[key]
    return dict3

print('Dict1', ToDoPoint1)
print('Dict2', ToDoPoint2)
dict3 = mergeDictStrongOne(ToDoPoint1, ToDoPoint2)
print('Dict3 = ', dict3)