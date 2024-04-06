import numpy as np
import enum
import scipy.signal as signal
import matplotlib.pyplot as plt
import time
import random
from scipy import stats
import sys
import multiprocessing
import struct
import datetime


DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
current_time = 0

class Time_S:
    def __init__(self):
        self.time = 0

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

class Rating:
    def __init__(self, completed):
        self.completed = completed  # was the task completed this attmept
        self.start_time_slack = 0
        self.end_time_slack = 0
        self.duration_slack = 0         # was there extra or negative time left 
        self.num_sessions = 0       # how many sessions did it take to complete



class Event: 
    def __init__(self, name, date, calendar=None):
        self.cal = calendar

        self.name = name
        self.id = None
        self.metaData = None

        self.date = date            # 1-7
        self.repeat_period = -1     # set to -1 if not repeated
        self.tar_time_start = 0
        self.tar_time_end = 0
        self.__tar_duration = self.tar_time_end - self.tar_time_start
        self.act_time_start = 0
        self.act_time_end = 0
        self.accumulated_session_time = 0
        self.sessions = 0
        
        self.priority = 0
        self.flexibility = 0
        self.time_mutable = True
        self.day_mutable = True

        self.children = None
        self.parent = None

        self.past_sessions = []     # list of past ratings 
        self.overall_success_rating = 0       # will reflect how well task is accomplished

    def plot_stats(self):
        plt.figure()
        
        st = []
        et = []
        du = []
        for session in self.past_sessions:
            st.append(session.start_time_slack)
            et.append(session.end_time_slack)
            du.append(session.duration_slack)

        plt.plot(st)
        plt.plot(et)
        plt.plot(du)
        plt.legend(['start time slack', 'end time slack', 'duration slack'])

        plt.show()

    def print_stats(self):
        av_st = 0
        av_et = 0
        av_du = 0
        for session in self.past_sessions:
            av_st += session.start_time_slack
            av_et += session.end_time_slack
            av_du += session.duration_slack

        num_elements = len(self.past_sessions)
        av_st /= num_elements
        av_et /= num_elements
        av_du /= num_elements

        print('average start time slack: ' + str(av_st))
        print('average end time slack: ' + str(av_et))
        print('average duration slack: ' + str(av_du))


    def set_time(self, start, end):
        if (start > end):
            print('invalid time')
            return
        self.tar_time_start = start
        self.tar_time_end = end
        self.__tar_duration = end - start

    def push_forward(self, new_time):
        self.time_start = new_time
    
    def change_priority(self, new_priority):
        self.priority = new_priority

    def start_task(self):
        self.act_time_start = self.cal.time.get_time()


    # returns true if task completed, returns false if not
    def end_task(self, percent_complete = 100):
        completed = bool(percent_complete >= 100)

        self.act_time_end = self.cal.time.get_time()
        duration = self.act_time_end - self.act_time_start

        session_rating = Rating(completed)
        # how far off the target start and end time were we... 
        session_rating.start_time_slack = self.act_time_start - self.tar_time_start
        session_rating.end_time_slack = self.act_time_end - self.tar_time_end

        # how far off the target duration...
        session_rating.duration_slack = duration - self.__tar_duration

        self.past_sessions.append(session_rating)

        # # lastly, 
        # if (completed):
        #     self.eval_task_performance()
        #     # reset accumulated_time
        #     self.accumulated_time = 0
        #     return True
        # else:
        #     # if not completed, will need to reschedule 
        #     # first, add elapsed time to total time
        #     self.accumulated_time += duration
        #     return False

    def eval_task_performance(self):
        # see if accumulated_time is greater than estimated time
        if (self.accumulated_time > self.tar_time_end - self.tar_time_start):
            return 1
        pass

    def plot_event_time_duration(self):
        time_duration = []
        for rate in self.past_accomplished:
            time_duration.append(rate.duration_slack)
        plt.plot(time_duration)
        plt.show()



class Calendar: 
    def __init__(self, user):
        self.time = Time_S()
        self.user = user
        self.event_list = []                # make an empty list of Event objs
        self.productivity_dist = [[0]*24]*7 # distribution from 0-10 productivity from 0:00 - 23:00

        self.std_prod_time()

        print('calendar created')

    def std_prod_time(self):
        self.productivity_dist = [[0, 0, 0, 0, 1, 2, 2, 3, 5, 6, 8, 9, 9, 8, 6, 4, 5, 5, 4, 4, 5, 3, 2, 1]]*7


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





    def read_calendar(self):
        pass

    def read_database(self):
        pass

    def send_to_calendar(self):
        pass

    def send_to_database(self):
        pass

