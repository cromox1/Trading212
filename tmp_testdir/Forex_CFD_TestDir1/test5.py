from datetime import datetime
from time import sleep

tidor5 = int(5 * 60)
arini_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
arini_epoch = int(datetime.now().timestamp())
print('ARINI_EPOCH = ', arini_epoch)
nanti = int((arini_epoch + tidor5) / tidor5) * tidor5 + 1
tidor = nanti - arini_epoch
print('NANTI = ', nanti)
futuretime = datetime.fromtimestamp(nanti).strftime('%Y-%m-%d %H:%M:%S')
print('SCRIPT WILL RUN AGAIN AT :', futuretime, '( NOW =', arini_date, '/ in', tidor, 'secs )')
# sleep(tidor)