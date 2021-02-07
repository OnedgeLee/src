#!/usr/bin/env python

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from std_msgs.msg import String
import rospy, sys, time
import numpy as np
from math import radians, cos, sin
from scipy.spatial.transform import Rotation as ROT

fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')
arw       = 2
arw_len   = arw
max_vel   = 30
angle_thr = 0.2

rot = ROT.from_euler('zyx', [0, 0, 0], degrees=True)
v1 = [1, 1, 0]
v2 = [-1, 1, 0]
v3 = [-1, -1, 0]
v4 = [1, -1, 0]

def init_axis(_ax, _v1, _v2, _v3, _v4, _rot) :
    if len(_ax.lines) == 4 :
        for i in range(4) :
            del _ax.lines[0]
    _ax.set_xlim(-2, 2)
    _ax.set_ylim(-2, 2)
    _ax.set_zlim(-2, 2)
    _ax.set_xlabel('X')
    _ax.set_ylabel('Y')
    _ax.set_zlabel('Z')
    _v11 = _rot.apply(_v1)
    _v22 = _rot.apply(_v2)
    _v33 = _rot.apply(_v3)
    _v44 = _rot.apply(_v4)
    _ax.plot([_v11[0], _v22[0]], [_v11[1], _v22[1]], [_v11[2], _v22[2]], color='red', alpha=.8, lw=3)
    _ax.plot([_v22[0], _v33[0]], [_v22[1], _v33[1]], [_v22[2], _v33[2]], color='red', alpha=.8, lw=3)
    _ax.plot([_v33[0], _v44[0]], [_v33[1], _v44[1]], [_v33[2], _v44[2]], color='red', alpha=.8, lw=3)
    _ax.plot([_v44[0], _v11[0]], [_v44[1], _v11[1]], [_v44[2], _v11[2]], color='red', alpha=.8, lw=3)

init_axis(ax, v1, v2, v3, v4, rot)

def imu_data_callback(msg) :
    global f_dir, R, P, Y, angle, magnitude
    _tmp  = msg.data.split(",")
    f_dir = str(_tmp[0])
    R, P, Y = float(_tmp[1]), float(_tmp[2]), float(_tmp[3])
    angle, magnitude = float(_tmp[4]), float(_tmp[5])

def quiver_data_to_segments(X, Y, Z, u, v, w, length=1):
    segments = (X, Y, Z, X+u*length, Y+v*length, Z+w*length)
    segments = np.array(segments).reshape(6,-1)
    return [[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*list(segments))]

def q2s(x, y, z, u, v, w, l) :
    x = x
    y = y
    z = z
    u = x+u*l
    v = y+v*l
    w = z+w*l
    return x, y, z, u, v, w

f_vec = ax.quiver(*q2s(0,0,0,0,0,0,0))

def update(_ax, x, y, z, u, v, w, l) :
    global f_vec
    f_vec.remove()
    f_vec = _ax.quiver(*q2s(x, y, z, u, v, w, l), arrow_length_ratio=0.3)

def main() :
    rospy.init_node('visualization', anonymous=False)
    sub_imu_data = rospy.Subscriber('imu_data', String, imu_data_callback)
    r   = rospy.Rate(1000)

    # f_vec = ax.quiver(0, 0, 0, 0.3, 0.3, 0.3, arrow_length_ratio=0.8, pivot='tail', color='blue', alpha=.8, lw=5)
    # f_vec = ax.quiver(*q2s(0,0,0,0,0,0,0))
    while not rospy.is_shutdown() :
        try :
            if abs(angle) > angle_thr :
                rot = ROT.from_euler('zyx', [Y, R, P], degrees=True)
                init_axis(ax, v1, v2, v3, v4, rot)
                ratio   = min(magnitude/max_vel, 1)
                arw_len = arw * ratio
                if f_dir == "1" :
                    print("1")
                    arw_x = arw_len * sin(radians(angle))
                    arw_y = arw_len * cos(radians(angle))
                    update(ax, -arw_x, -arw_y, 0, arw_x, arw_y, 0, arw_len)
                    # segments = quiver_data_to_segments(0, 0, 0, arw_x, arw_y, 0)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, 0-arw_x, 0-arw_y, 0, 1)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, arw_x, arw_y, 0, 1)
                    # f_vec.set_segments(segments)
                elif f_dir == "2" :
                    print("2")
                    arw_x = -arw_len * sin(radians(angle))
                    arw_y = arw_len * cos(radians(angle))
                    # segments = quiver_data_to_segments(0, 0, 0, arw_x, arw_y, 0)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, 0-arw_x, 0-arw_y, 0, 1)
                    update(ax, -arw_x, -arw_y, 0,arw_x, arw_y, 0, arw_len)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, arw_x, arw_y, 0, 1)
                    # f_vec.set_segments(segments)
                elif f_dir =="3" :
                    print("3")
                    arw_x = -arw_len * sin(radians(angle))
                    arw_y = -arw_len * cos(radians(angle))
                    # segments = quiver_data_to_segments(0, 0, 0, arw_x, arw_y, 0)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, 0-arw_x, 0-arw_y, 0, 1)
                    update(ax, -arw_x, -arw_y, 0,arw_x, arw_y, 0, arw_len)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, arw_x, arw_y, 0, 1)
                    # f_vec.set_segments(segments)
                else :
                    print("4")
                    arw_x = arw_len * sin(radians(angle))
                    arw_y = -arw_len * cos(radians(angle))
                    # segments = quiver_data_to_segments(0, 0, 0, arw_x, arw_y, 0)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, 0-arw_x, 0-arw_y, 0, 1)
                    update(ax, -arw_x, -arw_y, 0,arw_x, arw_y, 0, arw_len)
                    # segments = quiver_data_to_segments(-arw_x, -arw_y, 0, arw_x, arw_y, 0, 1)
                    # f_vec.set_segments(segments)
                plt.draw()
                plt.pause(0.000001)
            else :
                # update(ax, 0, 0, 0, 0, 0, 0, 0)
                segments = quiver_data_to_segments(0, 0, 0, 0, 0, 0)
                f_vec.set_segments(segments)
                plt.draw()
                plt.pause(0.000001)
        except :
            plt.draw()
            pass
        # rospy.spin()
        r.sleep()

if __name__=="__main__" :
    main()
