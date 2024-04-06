from datetime import datetime

# Date information in ISO 8601 format
date_string = "2023-01-31T18:30:00-08:00"

# Parse the date string into a datetime object
time = datetime.fromisoformat(date_string)
print(time)
print(time.date().year)
print(time.date().month)
print(time.date().day)
print(time.time().hour)
print(time.time().minute)
print(time.time().second)