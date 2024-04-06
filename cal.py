
from event import *

MORNING = [0, 0, 0, 0, 3, 4, 7, 9, 9, 8, 7, 7, 6, 6, 5, 4, 4, 3, 3, 3, 3, 3, 2, 1]
MIDDAY = [0, 0, 0, 0, 1, 2, 2, 3, 5, 6, 8, 9, 9, 8, 6, 4, 5, 5, 4, 4, 5, 3, 2, 1]
EVENING = [0, 0, 0, 0, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6, 6, 6, 8, 8, 9, 9, 8, 7, 5, 3]
FLATLINE = [5]*24

DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def sigmoid(x):
    return 10 / (1 + np.exp(-x/8))

class Calendar: 
    def __init__(self, user):
        self.user = user
        self.event_list = []                # make an empty list of Event objs
        # Initialize productivity_dist as a list of lists with separate inner lists
        self.productivity_dist = [FLATLINE[:] for _ in range(7)]
        self.id_list = []
        # test = [FLATLINE]*7
        # self.productivity_dist = test.copy()
        print('calendar created')

    def set_productivity(self, day, distribution):
        self.productivity_dist[day%7] = distribution.copy()

    def add_event(self, event):
        self.event_list.append(event)
        self.sort_events_by_time()

    def set_id(self, name, id):
        self.event_from_name(name).id = id

    def set_name(self, id, name):
        self.event_from_id(id).name = name

    def set_priority(self, id, priority):
        self.event_from_id(id).priority = priority

    def set_transparency(self, id, transparency):
        self.event_from_id(id).transparency = transparency

    def set_mutability(self, id, mutable):
        self.event_from_id(id).time_mutable = mutable

    def set_repeat(self, id, repeat):
        self.event_from_id(id).repeat_period = repeat

    def set_date(self, id, date_string):
        self.event_from_id(id).set_date(date_string)
    
    def get_analytics(self, id):
        analytics = []
        event = self.event_from_id(id)            
        return event.past_sessions  

    def get_overall_performance(self, id):
        return self.event_from_id(id).overall_rating

    def average_performance(self, id):
        self.event_from_id(id).average_performance()

        
    def set_time(self, id, start_string, end_string):
        start = iso_to_time(start_string)
        end = iso_to_time(end_string)

        if end < start:
            print('error', end, '<', start)
            return
        event = self.event_from_id(id)
        event.set_time(start, end)
        self.sort_events_by_time()

    def sort_events_by_time(self):
        for event in self.event_list:
            if event.tar_time_start == 0: 
                return
        def event_sort_key(event):
            return event.tar_time_start
        self.event_list.sort(key=event_sort_key)

    def sort_events_by_priority(self):
        def event_sort_key(event):
            return event.priority
        self.event_list.sort(key=event_sort_key)

    def event_from_name(self, name):
        for event in self.event_list:
            if name == event.name:
                return event
        print('warning!, not found')
        return -1

    def event_from_id(self, id):
        for event in self.event_list:
            if id == event.id:
                return event
        print('warning!, not found')
        return None

    def report_low_performance(self):
        for event in self.event_list:
            if (event.overall_performance):
                pass


    # This will automatically move low priority around to better fit schedule 
    def optimize_calendar(self):
        # move stuff around
        for event in self.event_list:
            print(event.name)
            print(event.priority)


    def push_event(self, id, time):
        # grab the target event 
        tar_event = self.event_from_id(id)

        # time_int = iso_to_time(time)

        # start by assigning target time to new time
        tar_event.tar_time_start = time 
        tar_event.tar_time_end = time + tar_event.tar_duration
        moved_event = None
        moved_time = 0
        
        # loop over from current element to end of array
        for current_event in self.event_list:
            if current_event.id != tar_event.id:
                # current_event = self.event_list[j]
                # if event collides with an object, push that object forward
                # only collides if on same day
                if(self.check_time_collision(tar_event, current_event)):
                    # if collided obj has higher priority or is not mutable, move tar
                    if((not current_event.time_mutable) or tar_event.priority < current_event.priority):
                        moved_event = tar_event        
                        moved_time = current_event.tar_time_end     # add 5 min buffer
                    # else, collided obj needs to move
                    else:
                        moved_event = current_event
                        moved_time = tar_event.tar_time_end     # add 5 min buffer
            
                # if we collided with an obj, move one of them
                if (moved_event != None):
                    self.push_event(moved_event.id, moved_time)
                    moved_event = None

            
    def check_time_collision(self, event1, event2):
        if (event1.is_transparent and event2.is_transparent):
            return False

        if (event1.date != event2.date):
            print('different dates!')
            return False

        s1 = event1.tar_time_start
        e1 = event1.tar_time_end
        s2 = event2.tar_time_start
        e2 = event2.tar_time_end

        if (s1 >= s2 and s1 < e2):
            return True
        if (e1 > s2 and e1 <= e2):
            return True           
        if (s2 >= s1 and s2 < e1):
            return True           
        if (e2 > s1 and e2 <= e1):
            return True           

        return False

    def start_task(self, id):
        event = self.event_from_id(id)
        event.start_task()

    def end_task(self, id):
        event = self.event_from_id(id)
        event.end_task()
        
        self.update_productivity(event)

    def update_productivity(self, event):
        recent_stats = event.past_sessions[-1]
        start_int = int(recent_stats[0])
        end_int = int(recent_stats[1])

        scale = recent_stats[3]/5.0

        day = get_day()
        for i in range(start_int, end_int):
            self.productivity_dist[day][i] += scale 

        # self.productivity_dist = [[sigmoid(x) for x in row] for row in self.productivity_dist]


    def load_calendar(self):
        self.from_json_file()

        for id in self.id_list:
            self.add_event(Event(id))

        for ev in self.event_list:
            ev.from_json_file()

    def save_calendar(self):
        self.id_list = []
        for ev in self.event_list:
            self.id_list.append(ev.id) 
            ev.to_json_file()
        self.to_json_file() 
    
    def to_json_file(self):
        json_data = json.dumps({'prod': self.productivity_dist, 'id': self.id_list})
        with open((SAVES + str(self.user) + '.json'), 'w') as f:
            json.dump(json_data, f)

    def from_json_file(self):
        file_path = SAVES + str(self.user) + '.json'
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        data = json.loads(json_data)   
        # print(data) 
        self.productivity_dist = data['prod']    
        self.id_list = data['id']    

    def plot_event_data(self, id):
        self.event_from_id(id).plot_stats()

    def plot_productivity_dist(self, type='Day'):
        plt.figure()

        # Setting the y-axis range from 0 to 10
        plt.ylim(0, 10)
        plt.ylabel("Productivity")
        plt.grid(True)

        if (type == 'Day'):

            # Adding labels and title
            plt.xlabel("Hour of the day")

            for dist in self.productivity_dist:
                plt.plot(dist)        
                
            plt.legend(['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat'])
        
        elif (type == 'Week'):
            # Setting the x-axis ticks to "Sun" through "Sat"
            plt.xticks(range(len(DAYS)), DAYS)
            # Adding labels and title
            plt.xlabel("Day of the Week")

            weekly_dist = []
            for dist in self.productivity_dist:
                weekly_dist.append(dist)

            plt.plot(weekly_dist)
        plt.show()


    def print_list_names(self):
        for event in self.event_list:
            print(f"task - {event.name: <10}| start time - {event.tar_time_start: <5} | end time - {event.tar_time_end: <5} | id = {event.id: <5}")