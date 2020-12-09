import pandas as pd
import wget
from os import path
from time import strftime, sleep

# chk if file exist, if not download from LSE url
tmpfilename = 'tmp-' + str(strftime("%Y-%m")) + '-issues-IPOs.xlsx'
if path.exists('tmpdir/' + tmpfilename) == False:
    ## web UI = https://www.londonstockexchange.com/reports?tab=new-issues-and-ipos
    # https://docs.londonstockexchange.com/sites/default/files/reports/New%20issues%20and%20IPOs_1.xlsx
    url1 = 'https://docs.londonstockexchange.com/sites/default/files/reports/'
    filexlsx = 'New issues and IPOs_1.xlsx'
    wget.download(url1+filexlsx, out='tmpdir/' + tmpfilename)
    sleep(2)

dataexcel = pd.read_excel('tmpdir/' + tmpfilename, sheet_name='New Issues and IPOs', skiprows=range(6), usecols=['Company', 'TIDM', 'Date', 'Issue Price', 'Currency'])
comp_list = dataexcel['Company'].tolist()
tidm_list = dataexcel['TIDM'].tolist()
date_list = dataexcel['Date'].tolist()
price_list = dataexcel['Issue Price'].fillna(0).tolist()
currc_list = dataexcel['Currency'].replace('GBX','GBP').fillna('PENCE').tolist()

company = [x for x in comp_list][::-1]
datejoin = [x.date() for x in date_list][::-1]
compcode = [x for x in tidm_list][::-1]
priceone = [x for x in price_list][::-1]
currency = [x for x in currc_list][::-1]

dict_start = {company[i]:datejoin[i] for i in range(len(company))}
dict_code = {company[i]:compcode[i] for i in range(len(company))}
dict_price = {company[i]:priceone[i] for i in range(len(company)) if priceone[i] != 0 }
dict_currency = {company[i]:currency[i] for i in range(len(company))}

dict_start_sort = dict(sorted(dict_start.items(), key=lambda x: x[1], reverse=True))

num = 1
for kk,vv in dict_start_sort.items():
    if type(kk) == str and vv.year > 2017:
        sitename = kk.replace(' ', '-').replace('"', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '').lower()
        siteurl = 'https://www.londonstockexchange.com/stock/' + dict_code[kk].replace(' ', '') + '/' + sitename + '/company-page'
        if kk in dict_price.keys():
            print(num, ')', vv, ' // ', kk, ' // ', dict_currency[kk], dict_price[kk], ' / ', siteurl)
        else:
            print(num, ')', vv, ' // ', kk, ' // ', ' GBP 0.0 # / ' , siteurl)
        num += 1

# try:
#     from os import remove as removefile
#     removefile(tmpfilename)
#     # print('  Successfully remove tmp file ' + str(self.tmpfilename))
# except WindowsError as exx:
#     print('  Error = ' + str(exx) + ' / file = ' + str(tmpfilename))