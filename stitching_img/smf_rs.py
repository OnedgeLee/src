#!/usr/bin/env python

# . ~/catkin_ws/devel/setup.bash (source)
## qr usage (create qr image)
# qr "some text" > "filename.png"

import pyrealsense2 as rs
import numpy as np
from math import pow, sqrt, pi
from copy import deepcopy
import cv2, rospy, sys, time, moveit_commander, moveit_msgs.msg
"""
from std_msgs.msg import String
sys.path.append("/home/robot/Downloads/pyzbar-master/")
import pyzbar.pyzbar as zbar
"""

""" S/N for Realsense """
# RS = '543'
RS = '199'


""" Define Parameter """


def cal_dist(_c_int, _d_f, _p) :
	_px = _p[0]
	_py = _p[1]
	_pz = _d_f.get_distance(_px, _py)
	_pt = rs.rs2_deproject_pixel_to_point(_c_int, [_px, _py], _pz)
	return _pt


def main() :
	""" Define Parameter """
	width  = 1280
	height = 720
	roi    = 80 # +, - roi pixel

	rospy.init_node('rs', anonymous=False)
	r = rospy.Rate(30)

	Conn 	   = False # Flag for RS Connection
	rs_context = rs.context()
	# print(rs_context.devices[0].get_info(rs.camera_info.serial_number))
	for i in range(len(rs_context.devices)) :
		detected   = rs_context.devices[i].get_info(rs.camera_info.serial_number)
		print(detected)
		sn_partial = detected[len(detected)-3:]
		if sn_partial == RS :
			Rs   = detected
			Conn = True
	if Conn :
		Pipe = rs.pipeline()
		Cfg  = rs.config()
		Cfg.enable_device(Rs)
		Cfg.enable_stream(rs.stream.depth,  640, 480,  rs.format.z16, 30)
		Cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
		Pipe.start(Cfg)
		time.sleep(1)

		ref_img  = 30
		img_cnt  = 0
		try :
			font	 = cv2.FONT_HERSHEY_COMPLEX
			align_to = rs.stream.color
			align    = rs.align(align_to)
			frames    = Pipe.wait_for_frames()
			a_frames  = align.process(frames)
			d_frame   = a_frames.get_depth_frame()
			c_frame   = a_frames.get_color_frame()
			c_intrin  = d_frame.profile.as_video_stream_profile().intrinsics
			c_intrin.model = rs.distortion.modified_brown_conrady # modified_brown_conrady as distortion model

			while not rospy.is_shutdown() :
				frames    = Pipe.wait_for_frames()
				a_frames  = align.process(frames)
				d_frame   = a_frames.get_depth_frame()
				c_frame   = a_frames.get_color_frame()
				color_img = np.asanyarray(c_frame.get_data())
				c_img     = deepcopy(color_img)
				gray_img  = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
				canny     = cv2.Canny(gray_img, 100, 140)
				# lines     = cv2.HoughLinesP(canny, 1, pi/180, 40, minLineLength=50, maxLineGap=40)
				# for i, line in enumerate(lines) :
				# 	if width/2 - roi < line[0][0] < width/2 + roi and width/2 - roi < line[0][2] < width/2 + roi : 
				# 		cv2.line(color_img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), 1)
				cv2.line(color_img, (int(width/2), 0), (int(width/2), height), (255, 0, 0), 2)
				cv2.line(color_img, (int(width/2)-roi, 0), (int(width/2)-roi, height), (255, 255, 255), 2)
				cv2.line(color_img, (int(width/2)+roi, 0), (int(width/2)+roi, height), (255, 255, 255), 2)
				cv2.imshow('img', color_img)
				k = cv2.waitKey(1) & 0xFF
				if k == 27 : # ESC
					Conn = False
					cv2.destroyAllWindows()
					break
				if k == 48 : # 0
					cv2.imwrite('/home/robot/python_ws/saved_pic.jpg', color_img)
					cv2.imwrite('/home/robot/python_ws/original.jpg', c_img)
				r.sleep()
			Pipe.stop()
		except :
			if Conn :
				print("closed")
				cv2.destroyAllWindows()
				Pipe.stop()
	else :
		print("Realsense should be connected")

if __name__=="__main__" :
	main()
