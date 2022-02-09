import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi, sin, cos, atan
from sympy import *

IS_SCATTER = False

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_bend_res_pts.csv')

plt.rcParams["figure.autolayout"] = True

ax = df.plot.scatter(x='x1', y='z1', c='black', s=12)
ax1 = df.plot.scatter(x='x2', y='z2', c='blue', s=12, ax=ax)
ax2 = df.plot.scatter(x='x3', y='z3', c='black', s=12, ax=ax)
ax3 = df.plot.scatter(x='x4', y='z4', c='blue', s=12, ax=ax)
ax4 = df.plot.scatter(x='x5', y='z5', c='black', s=12, ax=ax)
ax5 = df.plot.scatter(x='x6', y='z6', c='blue', s=12, ax=ax)

ax.set_xlabel('x (mm)', fontsize=12)
ax.set_ylabel('z (mm)', fontsize=12)
# ax.legend(['Simulation result', 'Kinematic model'], edgecolor='black', fontsize=12)
plt.show()

# print(X)