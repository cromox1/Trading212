import pandas as pd

dataexcel = pd.read_excel(r'Instrument_list_1.xlsx', sheet_name='1.1 Shares', skiprows=range(7), usecols=['Issuer Name', 'Instrument Name', 'Start Date', 'Security Mkt Cap (in £m)'])
# print(dataexcel)
# print(dataexcel.columns.ravel())
# df = pd.DataFrame(dataexcel, columns=['Issuer Name'])
# print(df)

# print(dataexcel['Issuer Name'].tolist())
# print(dataexcel['Start Date'].tolist())
# issuer_name = [x for x in dataexcel['Issuer Name'].tolist() if type(x) == str].reverse()
issuer_list = [x for x in dataexcel['Issuer Name'].tolist()]
start_list = [x for x in dataexcel['Start Date'].tolist()]
# print(issuer_name)
# print(type(issuer_name[0]))
# print(type(issuer_name[-1]))
issuer_name = [x for x in issuer_list if type(x) == str][::-1]
start_date = [x for x in start_list if type(x) == pd._libs.tslibs.timestamps.Timestamp][::-1]
print(len(issuer_name))
print(len(start_date))
# issuer_name = [x for x in dataexcel['Issuer Name'] if type(x) == str].reverse()
# start_date = [x for x in dataexcel['Start Date'] if type(x) == str].reverse()
dict_list = {issuer_name[i]:start_date[i] for i in range(len(issuer_name))}
# print(dict_list
limitone = 200
# dict_list_sort = {k: v for k, v in sorted(dict_list.items(), key=lambda item: item[1], reverse=True)[:limitone]}
dict_list_sort = dict(sorted(dict_list.items(), key=lambda x: x[1], reverse=True)[:limitone])
# dict_list_sort = sorted([(value,key) for (key,value) in dict_list.items()], reverse=True)
# print(dict_list_sort)

num = 1
for k,v in dict_list_sort.items():
    if type(k) == str:
        print(num, ')', v, '= ' + k)
        num += 1