import pandas as pd
import wget
from os import path
from time import strftime, sleep
import datetime

# chk if file exist, if not download from LSE url
tmpfilename = 'tmp-' + str(strftime("%Y-%m")) + '-issuer-all.xlsx'
if path.exists('tmpdir/' + tmpfilename) == False:
    ## web UI = https://www.londonstockexchange.com/reports?tab=issuers
    # https://docs.londonstockexchange.com/sites/default/files/reports/Issuer%20list_4.xlsx
    url1 = 'https://docs.londonstockexchange.com/sites/default/files/reports/'
    filexlsx = 'Issuer list_4.xlsx'
    wget.download(url1+filexlsx, out='tmpdir/' + tmpfilename)
    sleep(2)

dataexcel = pd.read_excel('tmpdir/' + tmpfilename, sheet_name='Companies', skiprows=range(5), usecols=['Company Name', 'Admission Date', 'Country of Incorporation'])
comp_list = dataexcel['Company Name'].fillna('').tolist()
date_list = dataexcel['Admission Date'].fillna(datetime.datetime(1900, 1, 1)).tolist()
country_list = dataexcel['Country of Incorporation'].fillna('').tolist()

company = [x for x in comp_list][::-1]
datejoin = [x.date() for x in date_list][::-1]
country = [x for x in country_list][::-1]

dict_start = {company[i]:datejoin[i] for i in range(len(company))}
dict_country = {company[i]:country[i] for i in range(len(company))}

dict_start_sort = dict(sorted(dict_start.items(), key=lambda x: x[1], reverse=True))

num = 1
for kk,vv in dict_start_sort.items():
    if type(kk) == str and vv.year > 2017:
        print(num, ')', vv, ' // ', kk, ' // ', dict_country[kk])
        num += 1

# try:
#     from os import remove as removefile
#     removefile(tmpfilename)
#     # print('  Successfully remove tmp file ' + str(self.tmpfilename))
# except WindowsError as exx:
#     print('  Error = ' + str(exx) + ' / file = ' + str(tmpfilename))