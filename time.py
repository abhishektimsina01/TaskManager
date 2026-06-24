from datetime import time, date, datetime, timedelta
from django.utils import timezone
import uuid

print(time(2,0,0))
date1  = date(2004, 4, 28)
print(date1)
date2 = date(2004, 4, 29)
print(date2)
print(date1 < date2)
print(type(time(2,0,0)))
print(datetime(2005,6,28, 9, 53))
data = datetime.now() + timedelta(hours= 24)
print(datetime.now(), 5*"=", data)
print(str(uuid.uuid4()))