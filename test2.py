
from datetime import date, datetime

today = date.today()
print(today.strftime("%d-%m-%y"))
print(today.isoweekday())

print(datetime(2022,12,2))

dt = datetime(2022,12,2,18,25)
print(dt.hour)