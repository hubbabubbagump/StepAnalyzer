# -*- coding: utf-8 -*-

import pandas as pd
from scipy import signal

#For removing the first and last 8 seconds of the data
def trim_df(data):
    firstTime = data['time'].iloc[0]
    lastTime = data['time'].iloc[-1]
    cutOffTime = 6
    data = data[data['time'] >= firstTime + cutOffTime]
    data = data[data['time'] <= lastTime - cutOffTime]
    data['time'] = data['time'] - (firstTime + cutOffTime)
    return data

#For smoothing data
def smooth_df(data):
    #If the horizontal acceleration is negative, then
    #the orientation of the phone was flipped.
    #Flip the ax values to gain a positive acceleration mean
    if data['ax'].mean() < 0:
        data['ax'] = data['ax'] * -1
    
    data['ax_smooth'] = smooth(data, 'ax')
    data['ay_smooth'] = smooth(data, 'ay')
    data['az_smooth'] = smooth(data, 'az')
    data['aT_smooth'] = smooth(data, 'aT')
    return data

#Code from lecture slides: http://www.cs.sfu.ca/~ggbaker/data-science/content/filtering.html#filtering
def smooth(data, axis):
    #Increase the 2nd variable to adhere more to original data 
    #Decrease to smooth more
    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
    return signal.filtfilt(b, a, data[axis])