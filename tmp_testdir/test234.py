## 'index ) element'
ema1 = 1.21187
ema2 = 1.21110
close1 = 1.21355
close2 = 1.21082

diffema1 = float(ema1) - float(close1)
print(diffema1)
print(str("%.5f" % round(diffema1, 5)))
peratus1 = abs(float(100*diffema1/ema1))
print('Peratus = ', peratus1)
print('Peratus = ', str("%.5f" % round(peratus1, 5)))

diffema2 = float(ema2) - float(close2)
print(diffema2)
print(str("%.5f" % round(diffema2, 5)))
peratus2 = abs(float(100*diffema2/ema2))
print('Peratus = ', peratus2)
print('Peratus = ', str("%.5f" % round(peratus2, 5)))

from datetime import datetime
print('TIME NOW = ', datetime.now())
print('STRFTIME = ', datetime.now().timestamp())


tukar = {'minute':60, 'hour': 3600, 'day': int(24*3600), 'week': int(24*3600*7), 'month': int(24*3600*30),
         'year': int(24*3600*365 + 6*3600)}

tperiod = '3 weeks'
timesequence = int(tperiod.split(' ')[0]) * int(tukar[tperiod.split(' ')[-1].replace('s','')])
print('TIMESEQ for' , tperiod, '=', timesequence)

tperiod = '3 days'
timesequence = int(tperiod.split(' ')[0]) * int(tukar[tperiod.split(' ')[-1].replace('s','')])
print('TIMESEQ for' , tperiod, '=', timesequence)

tperiod = '3 months'
timesequence = int(tperiod.split(' ')[0]) * int(tukar[tperiod.split(' ')[-1].replace('s','')])
print('TIMESEQ for' , tperiod, '=', timesequence)

nextexecute = int(datetime.now().timestamp()) + timesequence
print('TIME NOW = ', datetime.now(), ' / EPOCHTIME = ', int(datetime.now().timestamp()), ' / NEXT RUN = ',
      datetime.fromtimestamp(nextexecute).strftime('%Y-%m-%d %H:%M:%S'))