#%%
import time, serial, cv2, math
import pandas as pd

GRAPHICAL_DEBUG = True
TEXT_DEBUG      = True

class ReadLine :
    def __init__(self, s) :
        self.buf = bytearray()
        self.s   = s
    def readline(self) :
        i = self.buf.find(b'\n')
        if i >= 0 :
            r        = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True :
            i    = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i    = data.find(b'\n')
            if i >= 0 :
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else :
                self.buf.extend(data)

def ser_init() :
    _ser = serial.Serial(port='COM29', baudrate=115200, timeout=0.01)
    _ser.close()
    time.sleep(0.5)
    _ser.open()
    time.sleep(0.5)
    return _ser

def raw_byte_parsing(_raw) :
    _parsed = _raw.decode().split(",")
    return _parsed

def raw_string_parsing(_raw) :
    _parsed = _raw.split(",")
    return _parsed

def angle_init(_rl, _num) :
    time.sleep(0.5)
    _r, _p, _y = 0., 0., 0.
    while True :
        if len(_rl.readline()) > 0 :
            break
    for _ in range(_num) :
        _dat = raw_byte_parsing(_rl.readline())
        _r += float(_dat[6])
        _p += float(_dat[7])
        _y += float(_dat[8])
    _r = round(_r/_num, 4)
    _p = round(_p/_num, 4)
    _y = round(_y/_num, 4)    
    return _r, _p, _y


""" global variable and instance """
ser = ser_init()
rl  = ReadLine(ser)
# r0, p0, y0 = angle_init(rl, 10)

import numpy as np
from scipy.spatial.transform import Rotation as R

# rcl1 = R.from_euler('xz', [-90, 180], degrees = True)
rcl1 = R.from_euler('xy', [-90, 180], degrees = True)
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
    A_thr    = 500

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
            if not VEC_INIT :
                if pt2[1] > pt1[1] :
                    vc_o1 = pt2 - vc_o1a
                else :
                    vc_o1 = pt1 - vc_o1a

            vc_a1_ = vc_o1 + vc_o1a_
            vc_b1_ = vc_o1 + vc_o1b_
            vc_c1_ = vc_o1 + vc_o1c_

            df = pd.DataFrame(data=np.array([0., 0., 0., 0., 0., 0., vc_o1[0], vc_o1[1], vc_o1[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
            da = pd.DataFrame(data=np.array([0., 0., 0., 0., 0., 0., vc_a1_[0], vc_a1_[1], vc_a1_[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
            db = pd.DataFrame(data=np.array([0., 0., 0., 0., 0., 0., vc_b1_[0], vc_b1_[1], vc_b1_[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
            dc = pd.DataFrame(data=np.array([0., 0., 0., 0., 0., 0., vc_c1_[0], vc_c1_[1], vc_c1_[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
            df = df.append(da)
            df = df.append(db)
            df = df.append(dc)
            df = df.reset_index(drop = True)
            print("Check")
            # cv2.imshow('detect', cimg)
            cv2.imwrite('/Users/SRBL/Desktop/gusu/img.jpg', cimg)
            VEC_INIT = True
            # k = cv2.waitKey(3000) & 0xFF
            # if k == 27 :
            #     cv2.destroyAllWindows()

        # End of Vector Initialize
        if VEC_INIT :
            while True :
                if ser.in_waiting :
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
                        parsed = raw_byte_parsing(rl.readline())
                        if len(parsed) > 2 :
                            v0 = float(parsed[0])
                            v1 = float(parsed[1])
                            v2 = float(parsed[2])
                            v3 = float(parsed[3])
                            v6 = float(parsed[4])
                            v7 = float(parsed[5])
                            r = float(parsed[6])
                            p = float(parsed[7])
                            y = float(parsed[8])
                            # Rotation Matrix
                            rl1l2 = R.from_euler('xyz', [r-r0, p-p0, y-y0], degrees=True)
                            if pt2[1] > pt1[1] :
                                vc_o2 = pt1 - rcl1.apply(rl1l2.apply(vo2a))
                            else :
                                vc_o2 = pt2 - rcl1.apply(rl1l2.apply(vo2a))
                            vc_a2_ = vc_o2 + rcl1.apply(rl1l2.apply(vo2a_))
                            vc_b2_ = vc_o2 + rcl1.apply(rl1l2.apply(vo2b_))
                            vc_c2_ = vc_o2 + rcl1.apply(rl1l2.apply(vo2c_))

                            # Make DataFrame using Pandas
                            do = pd.DataFrame(data=np.array([v0, v1, v2, v3, v6, v7, vc_o2[0], vc_o2[1], vc_o2[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
                            da = pd.DataFrame(data=np.array([v0, v1, v2, v3, v6, v7, vc_a2_[0], vc_a2_[1], vc_a2_[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
                            db = pd.DataFrame(data=np.array([v0, v1, v2, v3, v6, v7, vc_b2_[0], vc_b2_[1], vc_b2_[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
                            dc = pd.DataFrame(data=np.array([v0, v1, v2, v3, v6, v7, vc_c2_[0], vc_c2_[1], vc_c2_[2]]), columns=['v0', 'v1', 'v2', 'v3', 'v6', 'v7', 'x', 'y', 'z'])
                            df = df.append(do)
                            df = df.append(da)
                            df = df.append(db)
                            df = df.append(dc)
                            df = df.reset_index(drop = True)
                            fname = '/Users/SRBL/Desktop/gusu/srm_data_plot/' + str(step) + '.csv'
                            img_f = '/Users/SRBL/Desktop/gusu/srm_data_plot/img/' + str(count) + '.jpg'
                            cv2.imwrite(img_f, cimg)
                            df.to_csv(fname, sep=',', na_rep = 'NaN')
                            count += 1
                            """
                            if count == 200 :
                                count = 0
                                step += 1
                                fname = '/Users/SRBL/Desktop/gusu/srm_data_plot/' + str(step) + '.csv'
                                df.to_csv(fname, sep=',', na_rep = 'NaN')
                                dr_list = np.arange(4, len(df))
                                df = df.drop(dr_list)
                                df = df.reset_index(drop = True)
                            """
                        # cv2.imshow('detect', cimg)
                        k = cv2.waitKey(1) & 0xFF
                        if k == 27 :
                            try :
                                ser.close()
                                cv2.destoryAllWindows()
                                break
                            except :
                                break
            try :
                ser.close()
                pipe.stop()
                cv2.destoryAllWindows()
            except :
                pass

if __name__=="__main__" :
    main()