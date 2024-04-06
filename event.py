import numpy as np
import enum
# import scipy.signal as signal
import matplotlib.pyplot as plt
import time
import random
# from scipy import stats
import sys
import multiprocessing
import struct
from datetime import datetime
import json

SAVES = 'saves/'

time_r = 0
day_r = 0

# def get_time():
#     current_time = datetime.now().time()
#     hour = current_time.hour
#     minute = current_time.minute
#     time = hour + minute/60.0

#     return time

def iso_to_date(date_string):
    time = datetime.fromisoformat(date_string)
    return [time.date().month, time.date().day, time.date().year]

def date_time_to_iso(date, hour, min):
    return datetime(date[2], date[0], date[1], hour, min)

def iso_to_time(date_string):
    time = datetime.fromisoformat(date_string)
    return time.time().hour + time.time().minute/60.0


def set_day(day):
    global day_r
    day_r = int(day)%7

def set_time(time):
    global time_r
    time_r = time

def get_time():
    global time_r
    return time_r

def get_day():
    global day_r
    return day_r

# [start_time, end_time, duration, num_sessions]

class Event: 
    def __init__(self, id, name=''):
        self.name = name
        self.id = id
        self.metaData = None

        self.date = [0, 0, 0]            # 1-7
        self.repeat_period = -1     # set to -1 if not repeated
        self.tar_time_start = 0
        self.tar_time_end = 0
        self.tar_duration = self.tar_time_end - self.tar_time_start
        self.act_time_start = 0
        self.act_time_end = 0
        self.accumulated_session_time = 0
        self.sessions = 0
        
        self.priority = 0               # how important is the task?
        self.flexibility = 0            # how flexible is the amount of time required
        self.is_transparent = False     # can they overlap?
        self.time_mutable = True        # can be moved?
        self.day_mutable = True

        self.children = None
        self.parent = None

        self.past_sessions = []     # list of past ratings 
        self.overall_rating = 0       # will reflect how well task is accomplished

    def set_time(self, start, end):
        if (start > end):
            print('invalid time')
            return
        self.tar_time_start = start
        self.tar_time_end = end
        self.tar_duration = end - start

    def set_date(self, date_string):
        self.date = iso_to_date(date_string)
        print(self.date)

    def push_forward(self, new_time):
        self.time_start = new_time
    
    def change_priority(self, new_priority):
        self.priority = new_priority

    def start_task(self):
        self.act_time_start = get_time() 


    # returns true if task completed, returns false if not
    def end_task(self, percent_complete = 100):
        completed = bool(percent_complete >= 100)

        self.act_time_end = get_time()
        self.compute_rating()

    def compute_rating(self):
        duration = self.act_time_end - self.act_time_start

        session_rating = [] 

        # how far off the target start and end time were we... 
        session_rating.append(self.act_time_start)
        session_rating.append(self.act_time_end)

        # how far off the target duration...
        session_rating.append(duration)
        
        # larger is worse... 
        session_rating.append(self.tar_duration - duration)

        self.past_sessions.append(session_rating)
        # print('session', self.past_sessions[-1])
    
    def average_performance(self):
        running_total = 0
        for session in self.past_sessions:
            running_total += session[3]
        
        number_sessions = len(self.past_sessions)
        self.overall_rating = running_total/number_sessions       


    def to_json_file(self):
        json_data = json.dumps(self.__dict__)
        with open((SAVES + str(self.id) + '.json'), 'w') as f:
            json.dump(json_data, f)

    def from_json_file(self):
        file_path = SAVES + str(self.id) + '.json'
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        self.__dict__ = json.loads(json_data)


    def plot_stats(self):
        plt.figure()
        
        st = []
        et = []
        du = []
        for session in self.past_sessions:
            st.append(session[0])
            et.append(session[1])
            du.append(session[2])

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
            av_st += session[0]
            av_et += session[1]
            av_du += session[2]

        num_elements = len(self.past_sessions)
        av_st /= num_elements
        av_et /= num_elements
        av_du /= num_elements

        print('average start time slack: ' + str(av_st))
        print('average end time slack: ' + str(av_et))
        print('average duration slack: ' + str(av_du))


    def plot_event_time_duration(self):
        time_duration = []
        for rate in self.past_accomplished:
            time_duration.append(rate.duration_slack)
        plt.plot(time_duration)
        plt.show()

