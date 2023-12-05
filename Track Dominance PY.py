# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 08:10:54 2023

@author: logan
"""

### Track Dominance 

import fastf1 as ff1
from fastf1 import plotting 
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np 
import pandas as pd

### Cache
ff1.Cache.enable_cache(r"C:\Users\logan\Documents\Python\notebooks\Cache")

### Setup Plotting
plotting.setup_mpl()

session = ff1.get_session(2023, 'Las Vegas', 'R')
session.load()

### Select Verstappen and Leclerc
drivers = ['VER', 'LEC']

### Limit to just selected drivers
compare_drivers = session.laps[session.laps['Driver'].isin(drivers)]
compare_drivers

fastest_lap_VER = session.laps.pick_driver('VER').pick_fastest()
fastest_lap_LEC = session.laps.pick_driver('LEC').pick_fastest()

telemetry_VER = fastest_lap_VER.get_telemetry().add_distance()
telemetry_LEC = fastest_lap_LEC.get_telemetry().add_distance()

telemetry_VER['Driver'] = 'VER'
telemetry_LEC['Driver'] = 'LEC'
telemetry_drivers = telemetry_VER.append(telemetry_LEC)

num_minisectors = 25

total_distance = max(telemetry_drivers['Distance'])

minisector_length = total_distance/num_minisectors
minisector_length

# Ininitate minisector variable with 0 meters as the starting point 
minisectors = [0]

#Add multiples of minisector_length to the minisectors
for i in range(0, (num_minisectors -1)):
    minisectors.append(minisector_length * (i + 1))
    
telemetry_drivers['Minisector'] = telemetry_drivers['Distance'].apply(
    lambda dist: (
        int((dist // minisector_length) + 1)
    )
)

average_speed = telemetry_drivers.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]

# Drop speed column and rename driver column 
fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns = {'Driver':'Fastest_driver'})

fastest_driver

# Join this df to the telemetry data 
telemetry_drivers = telemetry_drivers.merge(fastest_driver, on=['Minisector'])
telemetry_drivers = telemetry_drivers.sort_values(by=['Distance'])

# Convert driver names to integers
telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == 'VER', 'Fastest_driver_int'] = 1
telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == 'LEC', 'Fastest_driver_int'] = 2

x = np.array(telemetry_drivers['X'].values)
y = np.array(telemetry_drivers['Y'].values)

points = np.array([x,y]).T.reshape(-1,1,2)
segments = np.concatenate([points[:-1], points[1:]], axis =1)
fastest_driver_array = telemetry_drivers['Fastest_driver_int'].to_numpy().astype(float)

cmap = plt.get_cmap('spring', 2)
lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(fastest_driver_array)
lc_comp.set_linewidth(5)

plt.rcParams['figure.figsize'] = [12,6]

plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft = False, left = False, labelbottom = False, bottom = False)

cbar = plt.colorbar(mappable=lc_comp, label='Driver', boundaries=np.arange(1, 4))
cbar.set_ticks(np.arange(1.5, 3.5))
cbar.set_ticklabels(['VER', 'LEC'])
plt.title('2023 Grand Prix | VER VS LEC', font_size =16)
plt.show()
