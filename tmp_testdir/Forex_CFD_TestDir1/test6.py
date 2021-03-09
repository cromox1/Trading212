from datetime import datetime
# from time import sleep
#
# bezamasa = int(5 * 60)
# arini_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# arini_epoch = int(datetime.now().timestamp())
# nanti = int((arini_epoch + bezamasa) / bezamasa) * bezamasa + 61
# tidor = nanti - arini_epoch
# futuretime = datetime.fromtimestamp(nanti).strftime('%Y-%m-%d %H:%M:%S')
# print('SCRIPT WILL RUN AGAIN AT :', futuretime, '( NOW =', arini_date, '/ in', tidor, 'secs )')
# # sleep(tidor)
#
# testepoch = nanti + 23456
# datetestepoch = datetime.fromtimestamp(testepoch).strftime('%Y-%m-%d %H:%M:%S')
# print('TEST DATE = ', datetestepoch)

mytime = '2021-03-03 17:16:57'
myepoch = datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S").timestamp()
print('MYEPOCH = ', myepoch)
mydate = datetime.fromtimestamp(myepoch).strftime('%Y-%m-%d %H:%M:%S')
print('MYDATETIME = ', mydate)

