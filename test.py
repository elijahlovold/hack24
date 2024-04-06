from datetime import datetime

# Get the current date and time
current_time = datetime.now().time()
hour = current_time.hour
minute = current_time.minute
time = hour + minute/60.0
# Print the current time
print("Current time:", hour, " ", minute, " ", time)