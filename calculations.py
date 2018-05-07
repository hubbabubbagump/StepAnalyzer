# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

#For calculating velocity with acceleration OR distance with velocity
#velocity = init_velocity + acceleration*diff_time
#distance = init_distance + velocity*diff_time
def calc_kinematics(data, kin_label, known_label):
    data[kin_label] = data[known_label] * (data['time'] - data['time'].shift(1))
    data[kin_label].iloc[0] = 0
    data[kin_label] = np.absolute(data[kin_label].cumsum())
    return data

#Add the velocity and distance estimates to the dataframe
def generate_kinematics_data(data, accel, velocity, distance):
    new_data = calc_kinematics(data, velocity, accel)
    new_data = calc_kinematics(new_data, distance, velocity)
    return new_data