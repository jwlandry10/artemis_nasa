#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
from data_funcs import *

traj = pd.read_csv("/home/jwlandry/src/artemis_nasa/data/FY25 ADC HS Data Updated.csv")

tplot = traj.plot(x=traj.columns[1],y=traj.columns[2])
tplot.axis([-4e5,1.0e5,-2e5,3e5])
tplot.axis('square')

ax = plt.figure().add_subplot(projection='3d')
ax.plot(traj['Rx(km)[J2000-EARTH]'],traj['Ry(km)[J2000-EARTH]'],traj['Rz(km)[J2000-EARTH]'])
ax.set_aspect('equal', adjustable='box')

ax = plt.figure().add_subplot(projection='3d')
ax.plot(traj['Rx(km)[J2000-EARTH]'],traj['Ry(km)[J2000-EARTH]'],traj['Rz(km)[J2000-EARTH]'])

plt.figure()
plt.plot(traj['Rx(km)[J2000-EARTH]'],traj['Ry(km)[J2000-EARTH]'])
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel('J2000 R_x location')
ax.set_ylabel('J2000 R_y location')


# Calculate total slant range distance as square root of sum of squares of the distance (range) components
traj['Rmag'] = traj['Rx(km)[J2000-EARTH]']**2 + traj['Ry(km)[J2000-EARTH]']**2 + traj['Rz(km)[J2000-EARTH]']**2
traj['Rmag'] = np.sqrt(traj['Rmag'])

plt.figure()
plt.plot(traj['MISSION ELAPSED TIME (min)'],traj['Rmag'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Range (km)')

# calculate total velocity as square root of sum of squares of the velocity components
# V magnitude is sqrt(v_x^2 + v_y^2 + v_z^2) or the speed
traj['Vmag'] = traj['Vx(km/s)[J2000-EARTH]']**2 + traj['Vy(km/s)[J2000-EARTH]']**2 + traj['Vz(km/s)[J2000-EARTH]']**2
traj['Vmag'] = np.sqrt(traj['Vmag'])

plt.figure()
plt.plot(traj['MISSION ELAPSED TIME (min)'],traj['Vmag'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Speed (km/s)')

# Can also plot this in semi-log space
plt.figure()
plt.semilogy(traj['MISSION ELAPSED TIME (min)'],traj['Vmag'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Speed (km/s)')

# Which deep space network dishes can see the satellite
plt.figure()
plt.plot(traj['MISSION ELAPSED TIME (min)'],traj['WPSA Range'])
plt.plot(traj['MISSION ELAPSED TIME (min)'],traj['DS54 Range'])
plt.plot(traj['MISSION ELAPSED TIME (min)'],traj['Range DS24'])
plt.plot(traj['MISSION ELAPSED TIME (min)'],traj['Range DS34'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Range to Dish (km)')
ax.legend(['WPSA','DS54','DS24','DS34'])

# Figure out which dish is the best at a given time
ranges = ['WPSA Range', 'DS54 Range', 'Range DS24', 'Range DS34']
dsn_loc = ['WPSA', 'DS54', 'DS24', 'DS34']
traj['best_range'] = np.nanmin(traj[ranges], axis=1)

plt.figure()
plt.plot(traj['MISSION ELAPSED TIME (min)'], traj['best_range'])
plt.plot(traj['MISSION ELAPSED TIME (min)'], traj['WPSA Range'])
plt.plot(traj['MISSION ELAPSED TIME (min)'], traj['DS54 Range'])
plt.plot(traj['MISSION ELAPSED TIME (min)'], traj['Range DS24'])
plt.plot(traj['MISSION ELAPSED TIME (min)'], traj['Range DS34'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Range to Dish (km)')
ax.legend(['best','WPSA','DS54','DS24','DS34'])
plt.savefig('range_dish.png')

# Make a list of the min distance ranges and dishes
min_values = traj[ranges].min(axis=1)
min_indices = traj[ranges].idxmin(axis=1)

# Idnetify which dish is closest at a given time
ranges2 = ['WPSA Range', 'DS54 Range', 'Range DS24', 'Range DS34']
ranges2.append(np.nan)
dishes = [ranges2.index(x) for x in min_indices]

plt.figure()
plt.plot(traj['MISSION ELAPSED TIME (min)'], dishes)
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Deep Space ')

# Set up to calculate bitrate using other function find_best_dsn
slant_ranges = traj[ranges].to_numpy()
visibility = ['WPSA', 'DS54', 'DS24', 'DS34']
dish_viz = traj[visibility].to_numpy()
dish_size = [12, 34, 34, 34]
bitrate = find_best_dsn(slant_ranges, dish_viz, dish_size)

max_bitrate = [np.max([x for x in row]) for row in bitrate]
max_bitrate_cutoff = [x if x<10000 else 10000 for x in max_bitrate]

plt.figure()
plt.semilogy(traj['MISSION ELAPSED TIME (min)'], max_bitrate_cutoff)
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Bitrate (kbps)')

# Plot only first 2000 mins to show change in mass, speed
plt.figure()
plt.plot(traj['MISSION ELAPSED TIME (min)'], traj['MASS (kg)'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Mass (kg)')
ax.set_xlim(0,2000)

plt.figure()
plt.semilogy(traj['MISSION ELAPSED TIME (min)'],traj['Vmag'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Speed (km/s)')
ax.set_xlim(0,2000)

plt.figure()
plt.plot(traj['MISSION ELAPSED TIME (min)'], traj['MASS (kg)'])
ax = plt.gca()
ax.set_xlabel('Time (mins)')
ax.set_ylabel('Mass (kg)')

# plot locations on Map using cartopy
plt.figure()
ax = plt.axes(projection=ccrs.Mollweide())
ax.stock_img()
ds24_lon, ds24_lat = -116.875, 35.3399
ds34_lon, ds34_lat = 148.982, -35.3985
ds54_lon, ds54_lat = -4.2541, 40.4256
wpsa_lon, wpsa_lat = -75.475, 37.9273

plt.plot([ds24_lon, ds34_lon, ds54_lon, wpsa_lon], [ds24_lat, ds34_lat, ds54_lat, wpsa_lat],
         marker='o', linestyle='None', color='red',
         transform=ccrs.PlateCarree(),
         )

plt.show()
