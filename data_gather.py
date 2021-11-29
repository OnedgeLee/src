#%%
import time, serial, cv2, math
import pandas as pd

GRAPHICAL_DEBUG = True
TEXT_DEBUG      = True

p_res_dir = '/Users/SRBL/Desktop/gusu/p_res/'

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

            pt = pt1.tolist()
            pt.extend(pt2.tolist())
            
            np.savetxt(p_res_dir+'p_res_0.csv', delimiter=',', newline='\n')
            # cv2.imshow('detect', cimg)
            cv2.imwrite('/Users/SRBL/Desktop/gusu/img.jpg', cimg)
            VEC_INIT = True
            # k = cv2.waitKey(3000) & 0xFF
            # if k == 27 :
            #     cv2.destroyAllWindows()

        # End of Vector Initialize
        pt_list = list()
        if VEC_INIT :
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
                    pt = pt1.tolist()
                    pt.extend(pt2.tolist())
                    pt_list.append(pt)
                    
                    if len(pt_list) > 29 :
                        np.savetxt(p_res_dir + 'p_res.csv', pt_list, delimiter=',', newline='\n')
                        del pt_list[0]

                cv2.imshow('detect', cimg)
                k = cv2.waitKey(1) & 0xFF
                if k == 27 :
                    try :
                        np.savetxt(p_res_dir + 'p_res_term.csv', pt_list, delimiter=',', newline='\n')
                        cv2.destoryAllWindows()
                        break
                    except :
                        break
            try :
                pipe.stop()
                cv2.destoryAllWindows()
            except :
                pass

if __name__=="__main__" :
    main()
