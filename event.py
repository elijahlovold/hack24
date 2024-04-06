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
import json


def get_time():
    current_time = datetime.now().time()
    hour = current_time.hour
    minute = current_time.minute
    time = hour + minute/60.0

    return time


class Rating:
    def __init__(self, completed):
        self.completed = completed  # was the task completed this attmept
        self.start_time_slack = 0
        self.end_time_slack = 0
        self.duration_slack = 0         # was there extra or negative time left 
        self.num_sessions = 0       # how many sessions did it take to complete



class Event: 
    def __init__(self, name, date):
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

        self.past_sessions = [[]]     # list of past ratings 
        self.overall_success_rating = 0       # will reflect how well task is accomplished

    def compute_overall(self): 
        av_du = 0
        for session in self.past_sessions:
            av_du += session.duration_slack

        num_elements = len(self.past_sessions)
        av_du /= num_elements

        self.overall_success_rating = 1/av_du


        
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
        self.act_time_start = get_time() 


    # returns true if task completed, returns false if not
    def end_task(self, percent_complete = 100):
        completed = bool(percent_complete >= 100)

        self.act_time_end = get_time()
        duration = self.act_time_end - self.act_time_start

        session_rating = Rating(completed)

        # how far off the target start and end time were we... 
        session_rating.start_time_slack = self.act_time_start - self.tar_time_start
        session_rating.end_time_slack = self.act_time_end - self.tar_time_end

        # how far off the target duration...
        session_rating.duration_slack = duration - self.__tar_duration

        self.past_sessions.append(session_rating)

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

    def to_json_file(self):
        json_data = json.dumps(self.__dict__)
        with open((self.name + '.json'), 'w') as f:
            json.dump(json_data, f)

    def from_json_file(self):
        file_path = self.name + '.json'
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        self.__dict__ = json.loads(json_data)


