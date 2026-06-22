from datetime import time, date, datetime, timedelta
from django.utils import timezone

print(time(2,0,0))
print(date(2004, 4, 28))
print(type(time(2,0,0)))
print(datetime(2005,6,28, 9, 53))
data = datetime.now() + timedelta(hours= 24)
print(datetime.now(), 5*"=", data)