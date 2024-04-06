from cal import *


# ev = Event('work', '1/2/3')
# ev.time_mutable = False
# ev.day_mutable = False
# ev.repeat_period = 7    # every week
# ev.set_time(9, 17)
# ev.priority = 10



cal = Calendar('user')

cal.add_event(Event('work', '1/2/3'))
cal.add_event(Event('school', '1/5/3'))

event_handle = cal.event_list[0]

event_handle.time_mutable = False
event_handle.day_mutable = False
event_handle.repeat_period = 7    # every week
event_handle.set_time(9, 17)
event_handle.priority = 10


# for i in range(10):
#     cal.time.set_time(9 + (0.5 - random.random()))
#     event_handle.start_task()
#     cal.time.set_time(17 + (0.5 - random.random())*2)
#     event_handle.end_task()

# event_handle.print_stats()
# event_handle.plot_stats()

cal.save_calendar()
cal.productivity_dist = [[0]*24]*7

cal.event_list[0].from_json_file()
print(cal.event_list[0].repeat_period)

cal.load_calendar()

cal.plot_productivity_dist()