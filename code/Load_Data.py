#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

traj = pd.read_csv("../data/'FY25 ADC HS Data Updated.csv'")


tplot = traj.plot(x=traj.columns[1],y=traj.columns[2])
tplot.axis([-4e5,1.0e5,-2e5,3e5])
tplot.axis('square')

ax = plt.figure().add_subplot(projection='3d')
ax.plot(traj['Rx(km)[J2000-EARTH]'],traj['Ry(km)[J2000-EARTH]'],traj['Rz(km)[J2000-EARTH]'])
#ax.set_xlim(-4e5,1e5)
#ax.set_ylim(-2e5,3e5)
#ax.set_zlim(-4e5,1e5)
ax.set_aspect('equal', adjustable='box')
#ax.show()


# In[43]:


ax = plt.figure().add_subplot(projection='3d')
ax.plot(traj['Rx(km)[J2000-EARTH]'],traj['Ry(km)[J2000-EARTH]'],traj['Rz(km)[J2000-EARTH]'])


# In[51]:


plt.plot(traj['Rx(km)[J2000-EARTH]'],traj['Ry(km)[J2000-EARTH]'])
#ax.set_xlim(-4e5,1e5)
#ax.set_ylim(-2e5,3e5)
#ax.set_zlim(-4e5,1e5)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel('J2000 R_x location')
ax.set_ylabel('J2000 R_y location')
plt.show()


# In[ ]:




