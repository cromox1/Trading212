import pandas as pd

dataexcel = pd.read_excel(r'Instrument_list_1.xlsx', sheet_name='1.1 Shares', skiprows=range(7), usecols=['Issuer Name', 'Instrument Name', 'Start Date', 'Security Mkt Cap (in £m)'])
issuer_list = [x for x in dataexcel['Issuer Name'].tolist() if type(x) == str]
start_list = [x for x in dataexcel['Start Date'].tolist() if type(x) == pd._libs.tslibs.timestamps.Timestamp]
# print(dataexcel['Issuer Name'].tolist())
# print(dataexcel['Start Date'].tolist())
# print(type(start_list[0]))
print(issuer_list)
print(start_list)