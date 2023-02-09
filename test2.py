
from datetime import date, datetime

today = date.today()
print(today.strftime("%d-%m-%y"))
print(today.isoweekday())

print(datetime(2022,12,2))

dt = datetime(2022,12,2,18,25)
print(dt.hour)

from email_custom import send_email,Email

Email.sendEmail("New Flights","2022.12.10 10:45 168.00")