# -*- coding: utf-8 -*-

from data_smoother import smooth_df, trim_df
from peak_detect import get_peaks
from plotting import plot_template, plot_regress,  plot_distance_diff
from calculations import generate_kinematics_data
from scipy.stats import linregress
import pandas as pd
import numpy as np
import os

#Performs regression to determine if there's a relationship
#between height and steps per second
def steps_analysis(data):
    slope, intercept, r_value, p_value, std_err = linregress(data['height'], data['steps_per_sec'])
    plot_regress(data, slope, intercept, p_value)

#Plots the accuracy of each position via a bar chart
def acceleration_analysis(data):
    names = data['name'].apply(lambda x: x.split('_')[0])
    distinct_people = list(set(names))
    for name in distinct_people:
        data_filtered = data[data['name'].str.startswith(name)]
        data_raw = data_filtered[data_filtered['version'].str.startswith('raw')]
        abs_dist_raw = data_raw.apply(lambda x: get_distance_difference(x.est_distance,x.true_distance),axis = 1)
        data_smooth = data_filtered[data_filtered['version'].str.startswith('smooth')]
        abs_dist_smooth = data_smooth.apply(lambda x: get_distance_difference(x.est_distance,x.true_distance),axis = 1)
        abs_dist_raw = np.array(list(abs_dist_raw))
        abs_dist_smooth = np.array(list(abs_dist_smooth))
        name_list = np.array(list(data_filtered['name']))
        name_list = name_list[0::2] #Grab every second item
        plot_distance_diff(name_list, abs_dist_raw, abs_dist_smooth, name)

def get_distance_difference(est_dist, true_dist):
    return est_dist - true_dist

#Gather the results into a dictionary
def gather_results(data, peak_df, distance, version):
    totalTime = data['time'].iloc[-1] - data['time'].iloc[0]
    return {'version':version, 
            'velocity':data[distance].iloc[-1]/data['time'].iloc[-1], 
            'distance':data[distance].iloc[-1],
            'steps':peak_df.shape[0], 
            'steps_per_sec':peak_df.shape[0]/totalTime}

#Generate estimates of velocity, distance, and number of steps using acceleration data (for raw and smoothed data)
def analyze_acceleration(path, filename, accel_raw):
    file = pd.read_csv(path + filename, sep = ';|,', engine = 'python')
    accel_smooth = accel_raw + '_smooth'
    velocity_raw = 'velocity_raw'
    distance_raw = 'distance_raw'
    velocity_smooth = 'velocity_smooth'
    distance_smooth = 'distance_smooth'
    
    data = smooth_df(file)
    data = trim_df(data)
    data = generate_kinematics_data(data, accel_raw, velocity_raw, distance_raw)
    data = generate_kinematics_data(data, accel_smooth, velocity_smooth, distance_smooth)
    
    peaks = get_peaks(data, accel_raw)
    peaks_smooth = get_peaks(data, accel_smooth)
    peak_df = pd.DataFrame(peaks, columns=['time', 'acceleration'])
    peak_df_smooth = pd.DataFrame(peaks_smooth, columns=['time', 'acceleration'])
    
    plot_template(filename, data, peak_df, peak_df_smooth, 
                  accel_raw, accel_smooth, velocity_raw, velocity_smooth)

    raw_results = gather_results(data, peak_df, distance_raw, 'raw')
    smooth_results = gather_results(data, peak_df_smooth, distance_smooth, 'smooth')
    return {'raw':raw_results,
            'smooth':smooth_results,
            'name':filename.split('.')[0]}

#Get smoothed number of steps per seconds
def analyze_steps(path, filename):
    file = pd.read_csv(path + filename, sep = ';|,', engine = 'python')
    data = smooth_df(file)
    data = trim_df(data)
    peaks = get_peaks(data, 'ax_smooth')
    return len(peaks)/(data['time'].iloc[-1] - data['time'].iloc[0])

def main():
    distance_df = pd.read_csv('data/position_distances.csv', sep = ';|,', engine = 'python')
    dirs = os.listdir('data/positions/')
    version = [] 
    velocity = []
    distance = [] 
    steps = [] 
    steps_per_sec = []
    name = []
    for filename in dirs:
        analysis = analyze_acceleration('data/positions/', filename, 'ax')
        version = np.append(version, [analysis['raw']['version'], analysis['smooth']['version']], axis=0)
        velocity = np.append(velocity, [analysis['raw']['velocity'], analysis['smooth']['velocity']], axis=0)
        distance = np.append(distance, [analysis['raw']['distance'], analysis['smooth']['distance']], axis=0)
        steps = np.append(steps, [analysis['raw']['steps'], analysis['smooth']['steps']], axis=0)
        steps_per_sec = np.append(steps_per_sec, [analysis['raw']['steps_per_sec'], analysis['smooth']['steps_per_sec']], axis=0)
        name = np.append(name, [analysis['name'], analysis['name']], axis=0)
    analysis_df = pd.DataFrame({'version':version, 'est_velocity':velocity, 'est_distance':distance, 'steps':steps, 'steps_per_sec':steps_per_sec, 'name':name})
    analysis_df = pd.merge(analysis_df, distance_df, on='name')
    acceleration_analysis(analysis_df)
    
    analysis_df.to_csv('data/acceleration_analysis.csv', index=False)
    
    step_analysis_df = pd.read_csv('data/step_heights.csv', sep = ';|,', engine = 'python')
    steps_list = []
    dirs = os.listdir('data/steps/')
    for filename in dirs:
        steps_list = np.append(steps_list, [analyze_steps('data/steps/', filename)], axis=0)
    step_analysis_df['steps_per_sec'] = steps_list
    steps_analysis(step_analysis_df)
    
    step_analysis_df.to_csv('data/steps_analysis.csv', index=False)
    
if __name__ == '__main__':
    main()
