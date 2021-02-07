#%%
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.mplot3d import proj3D

fig = plt.figure(figsize=(15, 15))
ax  = fig.add_subplot(111, projection='3d')
# plt.quiver(0, 0, 0, 0.01, 0.01, 0.01, color='red', alpha=.8, lw=3)
f_vec = ax.quiver(0, 0, 0, 0.03, 0.03, 0.03, arrow_length_ratio=0.3, headwidth=5, pivot='tail', color='blue', alpha=.8, lw=5)

plt.show()