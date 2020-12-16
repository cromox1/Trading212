import requests

def currency_date_value(url):
    out1 = requests.get(url = url)
    data = []
    hari = ''
    for line in out1.text.split('\n'):
        if 'data-value=' in line:
            if 'data-value="--' not in line:
                data = data + [line]
        if 'data-type="date"' in line:
            hari = line
    tarikh = hari.split('content=')[-1].split('"')[1].replace('T', ' / ')
    # print('DATE = ', tarikh)
    datalast = data[-1]
    data_list = [float(x) for x in datalast.split('=')[1].split('"')[1].split(',')]
    avg = sum(data_list)/len(data_list)
    # print(data_list)
    # print('estimt = ',data_list[-4], ' / max = ', max(data_list), ' / min = ', min(data_list), ' / averg = ', avg)
    return tarikh, data_list[-4], min(data_list), max(data_list), avg

base_url = 'https://www.dailyfx.com/'
# currency = 'eur-usd'  # 1
# currency = 'gbp-usd'  # 2
# currency = 'usd-jpy'  # 3
# currency = 'usd-chf'  # 4
# currency = 'aud-usd'  # 5
# currency = 'usd-cad'  # 6
# currency = 'nzd-usd'  # 7
# currency = 'eur-gbp'
# currency = 'eur-jpy'
list_currency = ['eur-usd', 'gbp-usd', 'usd-jpy', 'usd-chf', 'aud-usd', 'usd-cad', 'nzd-usd']

for currncy in list_currency:
    url_curr = base_url + currncy
    data = currency_date_value(url_curr)
    print()
    print('DATE = ', data[0])
    print(currncy.upper(), ' = ', data[1], ' / min ', data[2], ' / max ', data[3], ' / avg ', data[4])

# https://s.tradingview.com/dailyfx/widgetembed/?frameElementId=tradingview_43f4c&symbol=FX_IDC%3AGBPUSD&interval=D&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=EEEFF0&studies=%5B%5D&hideideas=1&theme=Light&timezone=exchange&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=%5B%5D&disabled_features=%5B%5D&locale=en&utm_source=www.dailyfx.com&utm_medium=widget&utm_campaign=chart&utm_term=FX_IDC%3AGBPUSD