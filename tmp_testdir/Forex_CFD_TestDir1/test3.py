from datetime import datetime
from time import sleep

tidor = 130

# id = int(datetime.datetime.strptime(tarikh, '%Y-%m-%d %H:%M:%S').timestamp())
skrg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # .timestamp()
print('SKRG = ', skrg)
epoch1 = datetime.now().timestamp()
print('EPOCH = ', epoch1)
future = epoch1 + tidor
print('FUTURE = ', int(future))
# futuretime = datetime.strftime(epoch1, '%Y-%m-%d %H:%M:%S')
futuretime = datetime.fromtimestamp(int(future)).strftime('%Y-%m-%d %H:%M:%S')
print('FUTURETIME = ', futuretime)