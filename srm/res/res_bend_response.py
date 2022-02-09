import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

w_dir  = '/Users/shetshield/Desktop/workspace/python_ws/p_res/'
f_name = 'p_res_'
ext = '.csv'
f_n = [0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
"""
ang_list = [0.0,
            1.6023911333584258,
            3.25002275472884,
            4.946957840601142,
            6.697906574619198,
            8.508380593759275,
            10.384897985735293,
            12.335261073949935,
            14.368941314690067,
            16.497626577681366,
            18.736023326169125,
            21.103075819519326,
            23.62390254903347,
            26.333044813750153,
            29.2803117109867,
            32.5423232300939,
            36.248498930816595,
            40.65264722497219]
"""
ang_list = [0.0,
            0.8470236848232602,
            1.8205483622724785,
            2.920574032346247,
            4.147100695046197,
            6.315174089103777,
            7.434950843528536,
            8.681228590578895,
            10.054007330254963,
            11.553287062556537,
            13.179067787483785,
            14.931349505036302,
            16.810132215214757,
            18.815415918018555,
            20.947200613448132,
            23.20548630150308,
            25.590272982183798,
            28.10156065548996,
            30.739349321421805,
            33.5036389799792,
            36.394429631162104,
            39.411721274970574,
            42.55551391140466,
            45.82580754046444,
            49.222602162149705,
            51.02363457202777,
            51.27836085829361,
            51.533087144559516,
            51.787813430825445,
            52.04253971709124,
            52.297266003357215,
            52.55199228962305,
            52.806718575888944,
            53.06144486215487,
            53.316171148420686,
            53.57089743468661,
            53.82562372095241
]

ang_list = [0.0,
            0.8470236848232602,
            1.8205483622724785,
            2.920574032346247,
            4.147100695046197,
            6.315174089103777,
            7.434950843528536,
            8.681228590578895,
            10.054007330254963,
            11.553287062556537,
            13.179067787483785,
            14.931349505036302,
            16.810132215214757,
            18.815415918018555,
            20.947200613448132,
            23.20548630150308,
            25.590272982183798,
            28.10156065548996,
            30.739349321421805,
            33.5036389799792,
            36.394429631162104,
            39.411721274970574,
            42.55551391140466,
            45.82580754046444,
            49.222602162149705,
            50.23986138351738,
            50.49458766978319,
            50.74931395604912,
            51.004040242315035,
            51.25876652858087,
            51.51349281484677,
            51.768219101112614,
            52.022945387378535,
            52.27767167364445,
            52.53239795991025,
            52.78712424617622,
            53.04185053244207
]
'''
ang_list =[0.0,
           0.8470236848232602,
           1.8205483622724785,
           2.920574032346247,
           4.147100695046197,
           4.449872277768659,
           5.7193497111980385,
           7.1153281372541,
           8.637807555935636,
           10.28678796724261,
           12.062269371175136,
           13.964251767733458,
           15.99273515691731,
           18.14771953872668,
           20.429204913161538,
           22.83719128022217,
           25.371678639908154,
           28.032666992219912,
           30.820156337157265,
           33.734146674720066,
           36.774638004908496,
           39.94163032772254,
           43.235123643162126,
           46.65511795122723,
           50.20161325191801,
           50.23986138351738,
           50.49458766978319,
           50.74931395604912,
           51.004040242315035,
           51.25876652858087,
           51.51349281484677,
           51.768219101112614,
           52.022945387378535,
           52.27767167364445,
           52.53239795991025,
           52.78712424617622,
           53.04185053244207
]
'''
ang_list = [0.0 ,
0.592297398558133 ,
1.3110957897405118 ,
2.1563951735490505 ,
3.128195549983018 ,
4.226496919042432 ,
5.451299280727186 ,
6.802602635038309 ,
8.280406981974823 ,
9.884712321536583 ,
11.61551865372435 ,
13.472825978537434 ,
15.456634295976084 ,
17.5669436060404 ,
19.803753908730283 ,
22.167065204045645 ,
24.656877491986627 ,
27.27319077255329 ,
30.01600504574544 ,
32.88532031156325 ,
35.881136570006696 ,
39.00345382107551 ,
42.252272064769976 ,
45.62759130109017 ,
49.12941153003577 ,
50.23986138351738 ,
50.49458766978319 ,
50.74931395604912 ,
51.004040242315035 ,
51.25876652858087 ,
51.51349281484677 ,
51.768219101112614 ,
52.022945387378535 ,
52.27767167364445 ,
52.53239795991025 ,
52.78712424617622 ,
53.04185053244207
]
ang_list = [0.0 ,
            0.592297398558133 ,
            1.3110957897405118 ,
            2.1563951735490505 ,
            3.128195549983018 ,
            4.226496919042432 ,
            5.451299280727186 ,
            6.802602635038309 ,
            8.280406981974823 ,
            9.884712321536583 ,
            11.61551865372435 ,
            13.472825978537434 ,
            15.456634295976084 ,
            17.5669436060404 ,
            19.803753908730283 ,
            22.167065204045645 ,
            24.656877491986627 ,
            27.27319077255329 ,
            30.01600504574544 ,
            32.88532031156325 ,
            35.881136570006696 ,
            39.00345382107551 ,
            42.252272064769976 ,
            45.62759130109017 ,
            49.12941153003577 ,
]
ang_list2 = [
0.0, 0.8470236848232602, 1.8205483622724785, 2.920574032346247, 4.147100695046197, 5.50012835037236, 6.979656998322979, 8.585686638899675, 10.318217272101592, 12.17724889792977, 14.162781516383053, 16.274815127462194, 18.513349731166578, 20.87838532749697, 23.369921916452665, 25.98795949803387, 28.73249807224086, 31.603537639073373, 34.60107819853138, 37.72511975061506, 40.975662295324355, 44.35270583265907, 47.85625036261947, 51.48629588520543, 55.24284240041697
]



v_list = [i for i in range(0, -37, -1)]
ang_init = 8
ang_last = 20

v = [26, -24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, 0]

"""
angle_list  = list()
stddev_list = list()
for _f in f_n :
    f  = w_dir + f_name + str(_f) + ext
    df = pd.read_csv(f)
    angle = list(df.loc[:,'a'].values)
    ai = angle[0:ang_init]
    al = angle[-ang_last:]
    # a_i = sum(angle[0:ang_init])/ang_init
    # a_l = sum(angle[-ang_last:])/ang_last
    mi = np.mean(ai, axis=0)
    ml, stddev = np.mean(al, axis=0), np.std(al, axis=0)
    angle_list.append(abs(ml-mi))
    stddev_list.append(stddev)
"""
# print(angle_list)

import numpy as np
import pandas as pd
from math import degrees
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

df = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/sim_lin_bend/sim_res_1ch_bend_mod_neo575.csv')
df2 = pd.read_csv('/Users/shetshield/Desktop/workspace/python_ws/exp_p_res/exp_p_res_1ch_bend_mod2.csv')
x1 = list(df.loc[:, 'x1'].values)
x2 = list(df.loc[:, 'x2'].values)
x3 = list(df.loc[:, 'x3'].values)
x0 = list(df.loc[:, 'x0'].values)

y1 = list(df.loc[:, 'y1'].values)
y2 = list(df.loc[:, 'y2'].values)
y3 = list(df.loc[:, 'y3'].values)
y0 = list(df.loc[:, 'y0'].values)

z1 = list(df.loc[:, 'z1'].values)
z2 = list(df.loc[:, 'z2'].values)
z3 = list(df.loc[:, 'z3'].values)
z0 = list(df.loc[:, 'z0'].values)

# equation_plane(x1[0], y1[0], z1[0], x3[0], y3[0], z3[0], x4[0], y4[0], z4[0])
# equation_plane(x1[3], y1[3], z1[3], x3[3], y3[3], z3[3], x4[3], y4[3], z4[3])

from sympy import Plane, Point3D, Line3D
p = Plane(Point3D(x2[0], y2[0], z2[0]), Point3D(x1[0], y1[0], z1[0]), Point3D(x3[0], y3[0], z3[0]))
# p = Plane(Point3D(x2[5], y2[5], z2[5]), Point3D(x1[5], y1[5], z1[5]), Point3D(x3[5], y3[5], z3[5]))
L = Line3D(Point3D(0, 0, 0), Point3D(0, 0, 1))
angle = list()
for i in range(len(x1)):
    try :
        p = Plane(Point3D(x2[i], y2[i], z2[i]), Point3D(x1[i], y1[i], z1[i]), Point3D(x3[i], y3[i], z3[i]))
        _angle  = abs(degrees(p.angle_between(L)))
        d_angle = 90 - _angle
        angle.append(d_angle)
        print(d_angle)
    except :
        pass
X = np.linspace(-24, 0, 25)
X1 = np.linspace(-24, 0, 25)
# X1 = [-10, -10, -10]
X2 = np.linspace(-24, 0, 25)
# print(angle)
# print(angle2)

fig = plt.figure()
ax  = fig.add_subplot(111)
ax.set_ylim([-3, 54])
ax.minorticks_on()
# x_tick_list = [0, 5, 10, 15, 20]
ax.set_xlim([-27, 2])
x_tick_list = [-25, -20, -15, -10,-5, 0]
y_tick_list = [0, 15, 30, 45]

ax.set_yticks(y_tick_list)
ax.set_xticks(x_tick_list)

plt.setp(ax.get_yticklabels(), fontsize=10)
plt.setp(ax.get_xticklabels(), fontsize=10)

ax.tick_params(which='both', width=1)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=3, color='black')

ax.xaxis.set_minor_locator(plt.MultipleLocator(5/2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(15/3))

"""
ax.plot(X, list(reversed(angle)), c='black')
ax.plot(v_list, ang_list, c='blue')
ax.plot(v, list(reversed(angle_list)), c='red')
err = plt.errorbar(x=v, y=list(reversed(angle_list)), yerr=stddev_list, linestyle='None', ecolor='black', mfc='black', mec='black',
                            capsize=4, capthick=1)

axins = inset_axes(ax, width=1.2, height=1.4, loc=5)

axins.scatter(-10, angle_list[6], c='red')
err = plt.errorbar(x=-10, y=angle_list[6], yerr=stddev_list[6], linestyle='None', ecolor='black', mfc='black', mec='black',
                            capsize=4, capthick=1)
# axins.axes.get_xaxis().set_visible(False)

# print(angle_list[6])
x_tick = [-10]
y_tick = [22.44, 22.48]

# axins.set_xticklabels(x_tick, fontsize=18)
# axins.set_yticklabels(y_tick, fontsize=18)
axins.set_yticks(y_tick)
axins.set_xticks(x_tick)
"""
# ax.plot(X, list(reversed(angle2)), c='gray')
ax.plot(X1, list(reversed(angle)), c='blue')
ax.plot(X2, list(reversed(ang_list)), c='black')
ax.plot(X2, list(reversed(ang_list2)), c='black', linestyle='--')
ax1 = df2.plot.line(x='p_avg', y='angle_abs', c='red', ax=ax)
ax.set_xlabel('Pressure (kPa)', fontsize=12)
ax.set_ylabel('Bending angle ($^\circ$)', fontsize=12)

# ax.legend(['Both pressure sources', 'Single pressure source'], frameon=False, fontsize=18)
ax.legend(['Simulation', 'Kinematic model', 'Model without adjustment', 'Experiment'], edgecolor='black', fontsize=12)
# ax.legend(['Simulation', 'Experiment'], edgecolor='black', fontsize=12)
plt.show()