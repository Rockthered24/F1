# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 20:18:14 2023

@author: logan
"""

import fastf1 as ff1
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection

import numpy as np

ff1.Cache.enable_cache(r"C:\Users\logan\Documents\Python\notebooks\Cache")

session = ff1.get_session(2023, 'Las Vegas Grand Prix', 'Q')
session.load()

lap = session.laps.pick_fastest()
tel = lap.get_telemetry()



x = np.array(tel['X'].values)
y = np.array(tel['Y'].values)

tel.head()

points = np.array([x,y]).T.reshape(-1,1,2)
segments = np.concatenate([points[:-1], points[1:]], axis = 1)
gear = tel['nGear'].to_numpy().astype(float)

cmap = cm.get_cmap('Paired')

lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(gear)
lc_comp.set_linewidth(4)

cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
cbar.set_ticks(np.arange(1.5, 9.5))
cbar.set_ticklabels(np.arange(1, 9))

plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

title = plt.suptitle(
    f"Fastest Lap Gear Shift Visualization\n"
    f"{lap['Driver']} - {session.event['EventName']} {session.event.year}"
)

plt.show()
