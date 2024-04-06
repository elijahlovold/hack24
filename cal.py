
from event import *

MORNING = [[0, 0, 0, 0, 3, 4, 7, 9, 9, 8, 7, 7, 6, 6, 5, 4, 4, 3, 3, 3, 3, 3, 2, 1]]*7
MIDDAY = [[0, 0, 0, 0, 1, 2, 2, 3, 5, 6, 8, 9, 9, 8, 6, 4, 5, 5, 4, 4, 5, 3, 2, 1]]*7
EVENING = [[0, 0, 0, 0, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6, 6, 6, 8, 8, 9, 9, 8, 7, 5, 3]]*7

DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

class Calendar: 
    def __init__(self, user):
        self.user = user
        self.event_list = []                # make an empty list of Event objs
        self.productivity_dist = [[0]*24]*7 # distribution from 0-10 productivity from 0:00 - 23:00

        self.productivity_dist = EVENING
        print('calendar created')


    def plot_productivity_dist(self, type='Day'):
        plt.figure()

        # Setting the y-axis range from 0 to 10
        plt.ylim(0, 10)
        plt.ylabel("Productivity")

        if (type == 'Day'):

            # Adding labels and title
            plt.xlabel("Hour of the Week")

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


    def add_event(self, event):
        self.event_list.append(event)


    # This will automatically move low priority around to better fit schedule 
    def optimize_calendar(self):

        # move stuff around
        for event in self.event_list:
            print(event.name)
            print(event.priority)

    def push_event(self, i):
        pass

    def load_calendar(self):
        for ev in self.event_list:
            ev.from_json_file()
        self.from_json_file()


    def save_calendar(self):
        for ev in self.event_list:
            ev.to_json_file()
        self.to_json_file() 
    
    def to_json_file(self):
        json_data = json.dumps(self.productivity_dist)
        with open((self.user + '.json'), 'w') as f:
            json.dump(json_data, f)

    def from_json_file(self):
        file_path = self.user + '.json'
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        self.productivity_dist = json.loads(json_data)    
