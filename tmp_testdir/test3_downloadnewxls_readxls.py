import pandas as pd
import wget
from time import strftime, sleep

url1 = 'https://docs.londonstockexchange.com/sites/default/files/reports/'
# filexlsx = 'Instrument%20list_2.xlsx'
filexlsx = 'Instrument list_2.xlsx'
tmpfilename = 'tmptest123-' + str(strftime("%Y-%m-%d-%H-%M-%S")) + '.xlsx'

wget.download(url1+filexlsx, out=tmpfilename)
sleep(2)

# dataexcel = pd.read_excel(tmpfilename, sheet_name='1.1 Shares', skiprows=range(7), usecols=['Issuer Name', 'Instrument Name', 'Start Date', 'Security Mkt Cap (in £m)'])
dataexcel = pd.read_excel(tmpfilename, sheet_name='1.1 Shares', skiprows=range(7), usecols=['Issuer Name', 'Start Date'])
issuer_list = dataexcel['Issuer Name'].tolist()
start_list = dataexcel['Start Date'].tolist()
issuer_name = [x for x in issuer_list if type(x) == str][::-1]
start_date = [x.date() for x in start_list if type(x) == pd._libs.tslibs.timestamps.Timestamp][::-1]
dict_list = {issuer_name[i]:start_date[i] for i in range(len(issuer_name))}
# print(dict_list)
limit = 200
dict_list_sort = dict(sorted(dict_list.items(), key=lambda x: x[1], reverse=True)[:limit])

num = 1
for k,v in dict_list_sort.items():
    if type(k) == str:
        print(num, ')', v, ' // ' + k)
        num += 1

try:
    from os import remove as removefile
    removefile(tmpfilename)
    # print('  Successfully remove tmp file ' + str(self.tmpfilename))
except WindowsError as exx:
    print('  Error = ' + str(exx) + ' / file = ' + str(tmpfilename))