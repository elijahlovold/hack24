# example to fill the calendar

from cal import *

# create a calendar and set the productivity distributions
cal = Calendar('user')
cal.set_productivity(0, EVENING)
cal.set_productivity(1, MIDDAY)
cal.set_productivity(2, MORNING)
cal.set_productivity(3, MORNING)
cal.set_productivity(4, MORNING)
cal.set_productivity(5, EVENING)
cal.set_productivity(6, EVENING)

# create unique ids for tasks
ID1 = '3uumkvbpljdevh31optm20db79'
ID2 = '6ckvv9sshvg4qhgqjmgb2okq48'
ID3 = '54bp8qm17sc2de4namderaple1'

# add the events to the calendar 
cal.add_event(Event(ID1))
cal.add_event(Event(ID2))
cal.add_event(Event(ID3))

# set the date
date_string = "2023-01-31T18:30:00-08:00"
date_string_1 = "2023-03-31T18:30:00-08:00"
cal.set_date(ID1, date_string)
cal.set_date(ID2, date_string_1)
cal.set_date(ID3, date_string)

# set the priority  
cal.set_priority(ID1, 2)
cal.set_priority(ID2, 3)
cal.set_priority(ID3, 7)

# set the target start and end time for each event
date_string_start = "2023-01-31T11:00:00-08:00"
date_string_end = "2023-01-31T20:00:00-08:00"
cal.set_time(ID1, date_string_start, date_string_end)
date_string_start = "2023-01-31T06:00:00-08:00"
date_string_end = "2023-01-31T08:00:00-08:00"
cal.set_time(ID2, date_string_start, date_string_end)
date_string_start = "2023-01-31T02:30:00-08:00"
date_string_end = "2023-01-31T03:00:00-08:00"
cal.set_time(ID3, date_string_start, date_string_end)

# debug print
cal.print_list_names()

# loop four weeks simulating performance...
for i in range(4):
    time_series = [[6,8.5], [6,7], [6,8], [6.1,8.5], [5.7,8], [6.3,7.8], [6.7, 8]]

    set_day(0)
    for t in time_series:
        set_time(t[0] + (0.4 - random.random()))
        cal.start_task(ID2)
        set_time(t[1] + (0.5 - random.random()))
        cal.end_task(ID2)
        set_day(get_day()+1)

    time_series = [[11.4,20], [11.4,20], [11.2,20], [11.4,19], [10.4,20], [11.8,20], [11.4,19.2]]
    set_day(0)
    for t in time_series:
        set_time(t[0] + (0.2 - random.random()))
        cal.start_task(ID1)
        set_time(t[1] + (0.7 - random.random()))
        cal.end_task(ID1)
        set_day(get_day()+1)

# handle
event_handle = cal.event_from_id(ID1)
event_handle.print_stats()
event_handle.plot_stats()

# compute and display average performance for task
event_handle.average_performance()
print('overall rating', event_handle.overall_rating)

# save calendar to json
cal.save_calendar()

# plot the prod distribution
cal.plot_productivity_dist()