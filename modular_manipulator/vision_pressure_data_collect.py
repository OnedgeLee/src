#%%
import time, serial, cv2, math
import pandas as pd
import serial
from math import sqrt

"""
def raw_parsing(_raw) :
    _parsed = _raw.decode().split(',')
    # _parsed = _raw.split(',')
    return _parsed


ser = serial.Serial(port='COM27', baudrate=115200, timeout=0.01)
time.sleep(0.5)

incoming = ser.readline()
print(incoming)

ser.close()

while not ser.inWaiting() :
    time.sleep(0.1)

angle_0 = ser.readline().strip()
ang_0   = raw_parsing(angle_0)
"""

ser_ardu = serial.Serial(port='COM27', baudrate=115200, timeout=0.01)
ser_wemo = serial.Serial(port='COM3', baudrate=115200, timeout=0.01)
time.sleep(0.5)
ser_ardu.close()
ser_wemo.close()
time.sleep(0.5)

ser_ardu.open()
ser_wemo.open()
time.sleep(1)

GRAPHICAL_DEBUG = True
TEXT_DEBUG      = True

p_res_dir = '/Users/shetshield/Desktop/gusu/p_res/'
f_name    = '0'


""" global variable and instance """
import numpy as np
from scipy.spatial.transform import Rotation as R

# rcl1 = R.from_euler('xz', [-90, 180], degrees = True)
rcl1  = R.from_euler('xy', [-90, 180], degrees = True)
vo1a  = np.array([0, 68.7, 0])/1000.
vo1a_ = np.array([0, 48.7, 4])/1000.
vo1b  = np.array([59.5, -34.4, 0])/1000.
vo1b_ = np.array([42.2, -24.4, 4])/1000.
vo1c  = np.array([-59.5, -34.4, 0])/1000.
vo1c_ = np.array([-42.2, -24.4, 4])/1000.

""" initial bellow bottom position vectors """
vc_o1a  = rcl1.apply(vo1a)
vc_o1a_ = rcl1.apply(vo1a_)
vc_o1b  = rcl1.apply(vo1b)
vc_o1b_ = rcl1.apply(vo1b_)
vc_o1c  = rcl1.apply(vo1c)
vc_o1c_ = rcl1.apply(vo1c_)

""" Vector Position L2 Layer """
vo2a  = np.array([0, 68.7, 0])/1000.
vo2a_ = np.array([0, 48.7, 4])/1000.
vo2b  = np.array([59.5, -34.4, 0])/1000.
vo2b_ = np.array([42.2, -24.4, 4])/1000.
vo2c  = np.array([-59.5, -34.4, 0])/1000.
vo2c_ = np.array([-42.2, -24.4, 4])/1000.

import pyrealsense2 as rs

def rs_calc_dist(_intrinsic, _d_frm, _p) :
    _px = _p[0]
    _py = _p[1]
    _pz = _d_frm.get_distance(_px, _py)
    _pt = rs.rs2_deproject_pixel_to_point(_intrinsic, [_px, _py], _pz)
    return _pt

def main() :
    VEC_INIT = False
    fps      = 30
    A_thr    = 300

    """ Green Range """
    lg = np.array([60, 100, 0])
    ug = np.array([90, 255, 255])

    RS_CAM     = list()
    rs_context = rs.context()
    for i in range(len(rs_context.devices)) :
        detected = rs_context.devices[i].get_info(rs.camera_info.serial_number)
        RS_CAM.append(detected)
    if len(RS_CAM) :
        pipe   = rs.pipeline()
        rs_cfg = rs.config()
        rs_cfg.enable_device(RS_CAM[0])
        rs_cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, fps)
        rs_cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, fps)
        pipe.start(rs_cfg)
        time.sleep(1)

        """ cv2 text option """
        align_to  = rs.stream.color
        align     = rs.align(align_to)

        # cv2.namedWindow("detect", cv2.WINDOW_NORMAL)
        count = 0
        step  = 0
        # Get Image once & CAM Parameter
        frames = pipe.wait_for_frames()
        a_fs   = align.process(frames)
        d_f    = a_fs.get_depth_frame()
        c_f    = a_fs.get_color_frame()
        c_intrinsic = d_f.profile.as_video_stream_profile().intrinsics
        time.sleep(1)

        cimg = np.asanyarray(c_f.get_data())
        # cv2.imwrite('/Users/SRBL/Desktop/gusu/img.jpg', cimg)

        hsv   = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)
        mask  = cv2.inRange(hsv, lg, ug)
        c_det = cv2.bitwise_and(cimg, cimg, mask=mask)
        gray  = cv2.cvtColor(c_det, cv2.COLOR_BGR2GRAY)
        gray  = cv2.multiply(gray, 8) # Amplifing data
        ret, img_bin = cv2.threshold(gray, 127, 255, 0)
        cntrs, hierarchy = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imwrite('/Users/shetshield/Desktop/res.png', img_bin)
        k = cv2.waitKey(1) & 0xFF
        if k == 27 :
            cv2.destroyAllWindows()

        # End of Vector Initialize
        pt_list = list()
        while True :
            frms = pipe.wait_for_frames()
            a_fs = align.process(frms)
            d_f  = a_fs.get_depth_frame()
            c_f  = a_fs.get_color_frame()
            cimg = np.asanyarray(c_f.get_data())

            hsv   = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)
            mask  = cv2.inRange(hsv, lg, ug)
            c_det = cv2.bitwise_and(cimg, cimg, mask=mask)
            gray  = cv2.cvtColor(c_det, cv2.COLOR_BGR2GRAY)
            gray  = cv2.multiply(gray, 10) # Amplifing data
            ret, img_bin = cv2.threshold(gray, 127, 255, 0)
            cntrs, hierarchy = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            centroids = list()
            if len(cntrs) :
                for cnt in cntrs :
                    M = cv2.moments(cnt)
                    A = cv2.contourArea(cnt)
                    if A > A_thr :
                        cv2.drawContours(cimg, [cnt], 0, (255, 0, 0), 3)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        centroids.append([cx, cy])
                        if GRAPHICAL_DEBUG :
                            cv2.circle(cimg, (cx, cy), 3, (0, 0, 255), -1)
            if len(centroids) == 2 :
                pt1 = np.round(rs_calc_dist(c_intrinsic, d_f, centroids[0]), 3)
                pt2 = np.round(rs_calc_dist(c_intrinsic, d_f, centroids[1]), 3)
                dist = round(sqrt((pt2[0] - pt1[0])**2+(pt2[1] - pt1[1])**2+(pt2[2] - pt1[2])**2), 6)
            data1 = ser_ardu.readline().rstrip()
            data2 = ser_wemo.readline().rstrip()
            # print(data)
            try :
                data1 = data1.decode('utf-8')
                if len(data1) :
                    if len(data2) :
                        data2 = data2.decode('utf-8')
                        print(dist, ",", data1, ",", data2)
            except :
                pass

            cv2.imshow('detect', cimg)
            k = cv2.waitKey(1) & 0xFF
            if k == 27 :
                pipe.stop()
                cv2.destroyAllWindows()
                break
        try :
            pipe.stop()
            cv2.destroyAllWindows()
        except :
            ser_ardu.close()
            ser_wemo.close()

if __name__=="__main__" :
    main()