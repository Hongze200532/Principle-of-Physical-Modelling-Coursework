# Principle-of-Physical-Modelling-Coursework

### ST1_BlueCurve.py
This file aim to open the video document and capture the data of blue mass point movement and put in the csv file (mass_point_blue.coords.csv). While some data of the movement is missing as the mass point is shelter from the barrier, shows as <null> in the file.

### ST2_RedCurve.py
Basically as the Bluecurve file except for capturing the red mass point.

### ST3_Red->Blue.py
In order to fill the miss part of blue mass point movement data, we record the red one. As they are symmetry about the roatation center, we could uses the red mass point data to calculate the missing data. The fill data is also put into a csv file ('blue_ball_filled.csv').

### ST4_Visualisation.py
This file plot graphs of blue mass movement in scatter diagram and function curve. 

1. Clean the data, delete the red mass point and put into new file ('blue_ball_filled_clean.csv');

2. Convert the coordinate data (i.e. X&Y data) into theta, convert unit pixel into centimeter. Put into file (mass_point_theta.csv)

3. Visualise the movement with the data in csv file.
