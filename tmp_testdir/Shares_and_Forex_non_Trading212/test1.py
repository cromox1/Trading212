# from datetime import datetime
#
# # current date and time
# now = datetime.now()
#
# timestamp = datetime.timestamp(now)
# print("timestamp =", timestamp)

data1 = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'b', 'd'][::-1]
data2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14][::-1]

dict1 = {data1[i]:data2[i] for i in range(len(data1))}

print(dict1)

dict_list_sort = dict(sorted(dict1.items(), key=lambda x: x[1], reverse=True))

print(dict_list_sort)