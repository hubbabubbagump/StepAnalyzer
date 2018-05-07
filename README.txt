CMPT 318 Project

Members:
Ethan Jung
David Tran
Edwin Li

This project analyzes walking data sets. The walking data sets is stored in the 'data' folder. The 'data/position_distances.csv' spreadsheet contains the distance traveled of data sets with pocket, hand and ankle data. The 'data/steps_heights.csv' spreadsheet contains the heights of the people that recorded pocket data. The 'data/positions' folder contains the data sets with hand, ankle and pocket phone positions. The 'data/steps' folder contains anonymized data with walking data recorded from a phone in the pocket.

Pulling the repository will pull all files needed to run the program, the initial data, and the results from running the initial data. 

To add walking data from the pocket, add the accelerometer data to the 'data/steps' folder, and add the name of the file and height of the person to 'data/steps_heights.csv' in the 'data' folder. To add a data set with pocket, ankle and hand phone location data, add all three  files to the'data/positions' folder, and name the files as '<name of person>_<phone location>'. Copy the pocket data to the 'data/steps' folder and update 'data/steps_heights.csv' accordingly. Also update 'data/position_distances.csv' with the distance traveled during each of the pocket, hand and ankle sensor recordings.

To run the program, run 'sensor_analysis.py' using python3. The program will automatically import 'peakdetect.py' and 'data_smoother.py'. The libraries scipy, matplotlib, pandas, numpy and os are required  to run 'sensor_analysis.py'.

The program 'sensor_analysis.py' will generate and overwrite 'acceleration_analysis.csv' and 'steps_analysis.csv' in the data folder. The 'acceleration_analysis.csv' spreadsheet contains the estimated distance traveled and estimated velocity of each of the data sets containing hand, ankle and pocket data. The 'steps_analysis.csv' spreadseet contains the steps per second of the anonymized pocket data. 

In the 'plots' folder, the files in the 'plots/acceleration' and 'plots/positions' folder are generated and overwritten, along with the  'plots/steps-height.svg' file.

The 'plots/acceleration' folder contains the graphs, per person, of the difference between the estimated distance and true  distance traveled. The 'plots/positions' folder contains graphs of the acceleration and velocity graph of each of the phone, ankle and pocket data sets. The graphs in the 'plots/positions' folder also plots the locations of each peak. The 'plots/steps-height.svg' graph folder attempts to perform a regression on the steps/second and heights of each of the anonymized pocket data.

