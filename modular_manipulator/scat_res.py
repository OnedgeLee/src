#%%
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
# dist = round(math.hypot(pt2[0]- pt1[0], pt2[1]- pt1[1], pt2[2]- pt1[2]), 4)
df = pd.read_csv('/Users/user/Downloads/srm_data_plot/1.csv')

x = df.loc[:,"x"]
y = df.loc[:,"y"]
z = df.loc[:,"z"]
zdirs = (None, 'x', 'y', 'z', (1, 1, 0), (1, 1, 1))
fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')
ax.set_ylim(-0.1, 0.2)
ax.set_xlim(-0.2, 0)
ax.set_zlim(0.6, 0.8)

X = list(x.values)
Y = list(y.values)
Z = list(z.values)

origin = X[0], Y[0], Z[0]
init_a = [X[1], Y[1], Z[1]]
init_b = [X[2], Y[2], Z[2]]
init_c = [X[3], Y[3], Z[3]]
ax.scatter(X[0], Y[0], Z[0], c='red')
plt.draw()
del X[0]
del Y[0]
del Z[0]
for i in range(3) :
    ax.scatter(X[i], Y[i], Z[i], c='blue')
for _ in range(3) :
    del X[0]
    del Y[0]
    del Z[0]
    
d_x = [X[0]]
d_y = [Y[0]]
d_z = [Z[0]]
plt.draw()
plt.pause(10)
for i in range(1, len(X)) :
    if i%4 == 0 :
        ax.scatter(d_x[0], d_y[0], d_z[0], c='red')
        del d_x[0]
        del d_y[0]
        del d_z[0]
        d1 = round(math.hypot(d_x[0]- init_a[0], d_y[0]- init_a[1], d_z[0]- init_a[2]), 4)
        d2 = round(math.hypot(d_x[1]- init_b[0], d_y[1]- init_b[1], d_z[1]- init_b[2]), 4)
        d3 = round(math.hypot(d_x[2]- init_c[0], d_y[2]- init_c[1], d_z[2]- init_c[2]), 4)
        ax.scatter(d_x, d_y, d_z, c='green')
        ax.text2D(-0.05, 0.95, "d1: " + str(d1), transform=ax.transAxes)
        ax.text2D(-0.05, 0.85, "d2: " + str(d2), transform=ax.transAxes)
        ax.text2D(-0.05, 0.75, "d3: " + str(d3), transform=ax.transAxes)

        plt.draw()
        plt.pause(0.1)
        del ax.collections[4]
        del ax.collections[4]
        for _ in range(3) :
            del ax.texts[0]
        # del ax.texts
        d_x = [X[i]]
        d_y = [Y[i]]
        d_z = [Z[i]]
    else :
        d_x.append(X[i])
        d_y.append(Y[i])
        d_z.append(Z[i])
