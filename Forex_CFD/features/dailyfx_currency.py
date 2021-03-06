__author__ = 'cromox'

from requests import get as req_get

def currency_date_value():
    baseurl = 'https://www.dailyfx.com/'
    dict1 = {}
    for currency in ['gbp-usd', 'gbp-jpy', 'gbp-chf', 'gbp-cad']:
        url = baseurl + currency
        out1 = req_get(url = url)
        data = []
        for line in out1.text.split('\n'):
            if 'data-value=' in line:
                if 'data-value="--' not in line:
                    data = data + [line]
        datalast = data[-1]
        data_list = [float(x) for x in datalast.split('=')[1].split('"')[1].split(',')]
        average = sum(data_list)/len(data_list)
        dict1[currency.replace('gbp-', '').upper()] = "%.7f" % round(average, 7)
    # print('DICT_CURRENCY = ', dict1)
    return dict1