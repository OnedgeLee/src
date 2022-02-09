"""
    Ejector Model Performance Comparison Plot
"""

import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

w_dir  = '/Users/shetshield/Desktop/workspace/python_ws/ejector_model_performance/ejector_model_performance.csv'

import numpy as np
import pandas as pd
from math import degrees
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/ejector_model_performance/ejector_model_performance.csv')

ax  = df.plot.line(x='t', y='H74', c='black')
ax1 = df.plot.line(x='t', y='L74', c='blue', ax=ax)
ax2 = df.plot.line(x='t', y='L44', c='red', ax=ax)
ax3 = df.plot.line(x='t', y='H44', c='green', ax=ax)

x_tick_list = [0, 0.4, 0.8, 1.2]
y_tick_list = [-45, -30, -15, 0]

ax.set_yticks(y_tick_list)
ax.set_xticks(x_tick_list)

plt.setp(ax.get_yticklabels(), fontsize=10)
plt.setp(ax.get_xticklabels(), fontsize=10)

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=7)
ax.tick_params(which='minor', length=3, color='black')

ax.set_xlabel('Time (s)', fontsize=12)
ax.set_ylabel('Pressure (kPa)', fontsize=12)

ax.xaxis.set_minor_locator(plt.MultipleLocator(0.4/3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(15/3))

ax.legend(['H74', 'L74', 'L44', 'H44'], edgecolor='black', fontsize=12)
plt.show()