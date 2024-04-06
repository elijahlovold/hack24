from cal import *


cal = Calendar('user')
# cal.set_productivity(0, EVENING)
# cal.set_productivity(1, MIDDAY)
# cal.set_productivity(2, MORNING)
# cal.set_productivity(3, MORNING)
# cal.set_productivity(4, MORNING)
# cal.set_productivity(5, EVENING)
# cal.set_productivity(6, EVENING)

cal.add_event(Event(1000, 'work'))
cal.add_event(Event(2000, 'school'))
cal.add_event(Event(3000, 'eat'))


cal.set_priority(1000, 2)
cal.set_priority(2000, 3)
cal.set_priority(3000, 7)

cal.set_time(1000, 11, 20)
cal.set_time(2000, 6, 8)
cal.set_time(3000, 7, 8)

# # cal.sort_events_by_time()

# cal.print_list_names()

# cal.push_event('school', 7.5)

# cal.print_list_names()

event_handle = cal.event_list[0]

for i in range(5):
    time_series = [[6,8.5], [6,7], [6,8], [6.1,8.5], [5.7,8], [6.3,7.8], [6.7, 8]]

    set_day(0)
    for t in time_series:
        set_time(t[0] + (0.4 - random.random()))
        cal.start_task(2000)
        set_time(t[1] + (0.5 - random.random()))
        cal.end_task(2000)
        set_day(get_day()+1)

    time_series = [[11.4,20], [11.4,20], [11.2,20], [11.4,19], [10.4,20], [11.8,20], [11.4,19.2]]

    set_day(0)
    for t in time_series:
        set_time(t[0] + (0.2 - random.random()))
        cal.start_task(1000)
        set_time(t[1] + (0.7 - random.random()))
        cal.end_task(1000)
        set_day(get_day()+1)

event_handle.print_stats()
event_handle.plot_stats()

# cal.save_calendar()
# cal.productivity_dist = [[0]*24]*7

# print(cal.event_list[0].repeat_period)
# cal.load_calendar()
event_handle.average_performance()
print('overall rating', event_handle.overall_rating)

cal.plot_productivity_dist()