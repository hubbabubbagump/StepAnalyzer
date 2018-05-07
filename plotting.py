# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#plot the difference between estimated distance and true distance
def plot_distance_diff(name_list, abs_dist_raw, abs_dist_smooth, name):
    x = np.array(range(len(name_list)))
    width = 0.4
    mid_line = [width * -1, 1, len(name_list) - 1 + 0.4]
    x_raw = x - width / 2
    x_smooth = x + width / 2
    plt.xticks(x, name_list)
    plt.bar(x_raw, abs_dist_raw, color='b', width=width, align='center')
    plt.bar(x_smooth, abs_dist_smooth, color='r', width=width, align='center')
    plt.legend(['raw data', 'smoothed data'])
    plt.plot(mid_line, np.zeros(abs_dist_raw.shape), 'k-')
    plt.ylabel('Difference (m)')
    plt.title('Difference between estimated and true distance traveled')
    plt.tight_layout()
    plt.savefig('plots/acceleration/' + name + '.svg')
    plt.close()    

#Plots the linear regression between height and steps/sec 
def plot_regress(data, slope, intercept, p_value):
    plt.scatter(data['height'], data['steps_per_sec'], color ='blue')
    plt.plot(data['height'], data['height']*slope + intercept, 'r-', linewidth=1)
    plt.ylabel('steps per second')
    plt.xlabel('height')
    plt.title('steps vs height, p-value: {}'.format(p_value))
    plt.tight_layout()
    plt.savefig('plots/steps-height.svg')
    plt.close()
    
#Plots the acceleration, velocity, and number of steps
def plot_results(data, peak_df, accel, velocity, title):
    plt.plot(data['time'], np.zeros(data['time'].shape), 'g-')
    plt.plot(data['time'], data[accel], 'r-')
    plt.plot(data['time'], data[velocity], 'b-')
    plt.plot(peak_df.time, peak_df['acceleration'], 'v')
    plt.title(title)
    plt.legend(['zero line', 'acceleration', 'velocity', 'steps'])
    plt.xlabel('Time (s)')
    plt.ylabel('Distance (m)')
    
#Creates plot for unsmoothed and smoothed data
def plot_template(filename, data, peak_df, peak_df_smooth, accel_raw, accel_smooth, velocity_raw, velocity_smooth):
    plt.subplot(2,1,1)
    plot_results(data, peak_df, accel_raw, velocity_raw, 'Unsmoothed Plot of Data')
    plt.subplot(2,1,2)
    plot_results(data, peak_df_smooth, accel_smooth, velocity_smooth, 'Smoothed Plot of Data')
    plt.tight_layout()
    plt.savefig('plots/positions/'+ filename.split('.')[0] + '.svg')
    plt.close()