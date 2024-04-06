from cal import *


cal = Calendar('user')
# cal.set_productivity(0, EVENING)
# cal.set_productivity(1, MIDDAY)
# cal.set_productivity(2, MORNING)
# cal.set_productivity(3, MORNING)
# cal.set_productivity(4, MORNING)
# cal.set_productivity(5, EVENING)
# cal.set_productivity(6, EVENING)

cal.add_event(Event('id213'))
cal.add_event(Event('id313'))
cal.add_event(Event('id413'))

date_string = "2023-01-31T18:30:00-08:00"
date_string_1 = "2023-03-31T18:30:00-08:00"
cal.set_date('id213', date_string)
cal.set_date('id313', date_string_1)
cal.set_date('id413', date_string)

cal.set_priority('id213', 2)
cal.set_priority('id313', 3)
cal.set_priority('id413', 7)

# cal.set_time('id213', 11, 20)
# cal.set_time('id313', 6, 8)
# cal.set_time('id413', 7, 8)

# cal.sort_events_by_time()

cal.push_event('id313', 7.5)

cal.print_list_names()

event_handle = cal.event_list[0]

for i in range(5):
    time_series = [[6,8.5], [6,7], [6,8], [6.1,8.5], [5.7,8], [6.3,7.8], [6.7, 8]]

    set_day(0)
    for t in time_series:
        set_time(t[0] + (0.4 - random.random()))
        cal.start_task('id313')
        set_time(t[1] + (0.5 - random.random()))
        cal.end_task('id313')
        set_day(get_day()+1)

    time_series = [[11.4,20], [11.4,20], [11.2,20], [11.4,19], [10.4,20], [11.8,20], [11.4,19.2]]

    set_day(0)
    for t in time_series:
        set_time(t[0] + (0.2 - random.random()))
        cal.start_task('id213')
        set_time(t[1] + (0.7 - random.random()))
        cal.end_task('id213')
        set_day(get_day()+1)

event_handle.print_stats()
event_handle.plot_stats()

cal.save_calendar()
event_handle.average_performance()
print('overall rating', event_handle.overall_rating)

cal.plot_productivity_dist()