from datetime import datetime
from pytz import timezone,all_timezones

arini = datetime.now(timezone('Asia/Kuala_Lumpur')).strftime("%Y-%m-%d %H:%M:%S GMT%z")
print('ARINI =', arini)

masastart = arini
epochstart = int(datetime.strptime(masastart, "%Y-%m-%d %H:%M:%S GMT%z").timestamp())
# epochstart = int(datetime.strftime(masastart, "%Y-%m-%d %H:%M:%S %Z%z").timestamp())

print('EPOCH =', epochstart)

print(all_timezones)