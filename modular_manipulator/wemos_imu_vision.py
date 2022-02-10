#%%
import time, serial, threading, cv2, math
import pyrealsense2 as rs
import numpy as np
from scipy.spatial.transform import Rotation as R

rs_context = rs.context()
for i in range(len(rs_context.devices)) :
    detected = rs_context.devices[i].get_info(rs.camera_info.serial_number)
    print(detected)

def cal_dist(_c_int, _d_f, _p) :
	_px = _p[0]
	_py = _p[1]
	_pz = _d_f.get_distance(_px, _py)
	_pt = rs.rs2_deproject_pixel_to_point(_c_int, [_px, _py], _pz)
	return _pt

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b'\n')
        # print(len(self.buf), i)
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            # i = bytes(reversed(data)).find(b'\n')
            i = data.find(b'\n')
            # print(data, i)

            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)


def raw_parsing(_raw):
    # print(_raw)
    _parsed = _raw.decode().split(',')
    return _parsed


def ser_init(_port, _bdr) :
    _ser = serial.Serial(port=_port, baudrate=_bdr, timeout=0.001)
    _ser.close()
    time.sleep(0.05)
    _ser.open()
    time.sleep(0.05)
    return _ser


def recv_imu(_serIMU):
    global imu_msg
    _buf = bytearray()
    while True:
        # last_received = ser.readline()
        _buf += _serIMU.read(_serIMU.inWaiting())
        if b'\n' in _buf:
            imu_msg, _buf= _buf.split(b'\n')[-2:]


def recv_wemo(_serWemo) :
    global wemo_msg
    _buf = bytearray()
    while True :
        _buf += _serWemo.read(_serWemo.inWaiting())
        if b'\n' in _buf :
            wemo_msg, _buf = _buf.split(b'\n')[-2:]


lg = np.array([55, 130, 0])
ug = np.array([90, 255, 255])

rcl1  = R.from_euler('xz', [-90, 180], degrees = True) # From Inital Setup
# rcl1  = R.from_euler('x', [180], degrees = True) # From Inital Setup
# rl1l2 = R.from_euler('xyz', [45, 45, 45], degrees = True) # From IMU
""" Position Vector with respect to their local frame {L1} & {L2} """
vo1a    = [0, 68.7, 0]
vc_o1a  = rcl1.apply(vo1a)/1000.
vo1a_   = [0, 48.7, 4]
vc_o1a_ = rcl1.apply(vo1a_)/1000.
vo1b    = [59.5, -34.4, 0]
vc_o1b  = rcl1.apply(vo1b)/1000.
vo1b_   = [42.2, -24.4, 4]
vc_o1b_ = rcl1.apply(vo1b_)/1000.
vo1c    = [-59.5, -34.4, 0]
vc_o1c  = rcl1.apply(vo1c)/1000.
vo1c_   = [-42.2, -24.4,  4]
vc_o1c_ = rcl1.apply(vo1c_)/1000.

vo2a    = [0, 68.7/1000., 0]
vo2a_   = [0, 48.7/1000., -4/1000.]
vo2b    = [59.5/1000., -34.4/1000., 0]
vo2b_   = [42.2/1000., -24.4/1000., -4/1000.]
vo2c    = [-59.5/1000., -34.4/1000., 0]
vo2c_   = [-42.2/1000., -24.4/1000., -4/1000.]
# Angle Initialize

A_THR = 130
VEC_INIT = False
if detected :
    serIMU  = ser_init('COM3', 921600)
    serWemo = ser_init('COM4', 115200)
    threading.Thread(target=recv_imu, args=(serIMU,)).start()
    threading.Thread(target=recv_wemo, args=(serWemo,)).start()

    _imu = imu_msg.decode('utf-8').rstrip().split(",")
    r0 = float(_imu[1])
    p0 = float(_imu[2])
    y0 = float(_imu[3])

    f = open("/Users/srbl/Desktop/gusu/220209/pp15.txt", "w")
    # rl = ReadLine(serWemo)
    pp = rs.pipeline()
    cfg = rs.config()
    cfg.enable_device(detected)
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    cfg.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    pp.start(cfg)

    time.sleep(1)
    align_to = rs.stream.color
    align    = rs.align(align_to)

    frs = pp.wait_for_frames()
    afs = align.process(frs)
    df = afs.get_depth_frame()
    intr = df.profile.as_video_stream_profile().intrinsics

    cv2.namedWindow("dst", cv2.WINDOW_NORMAL)
    while True :
        try:
            frs = pp.wait_for_frames()
            afs = align.process(frs)
            df  = afs.get_depth_frame()
            cf  = afs.get_color_frame()
            cimg = np.asanyarray(cf.get_data())
            _tmpIMU = imu_msg.decode('utf-8').rstrip().split(",")
            _r = float(_tmpIMU[1])
            _p = float(_tmpIMU[2])
            _y = float(_tmpIMU[3])

            hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)
            msk = cv2.inRange(hsv, lg, ug)
            cdet = cv2.bitwise_and(cimg, cimg, mask=msk)
            cgry = cv2.cvtColor(cdet, cv2.COLOR_BGR2GRAY)
            cgry = cv2.multiply(cgry, 12)
            ret, ibin = cv2.threshold(cgry, 127, 255, 0)
            cntrs, _ = cv2.findContours(ibin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            ctrd = list()
            if len(cntrs) :
                for cnt in cntrs :
                    M = cv2.moments(cnt)
                    area = cv2.contourArea(cnt)
                    if area > A_THR :
                        cv2.drawContours(cdet, [cnt], 0, (255, 0, 0), 3)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        # print("center", cx, cy)
                        ctrd.append([cx, cy])
                        cv2.circle(cdet, (cx, cy), 3, (0, 0, 255), -1)
            k = cv2.waitKey(2) & 0xFF
            if k == 27 :
                cv2.destroyAllWindows()
                f.close()
                pp.stop()
                serWemo.close()
                serIMU.close()
                break
            cv2.imshow("dst", cdet)
            if len(ctrd) == 2 :
                pt1 = np.round(cal_dist(intr, df, ctrd[0]), 3)
                pt2 = np.round(cal_dist(intr, df, ctrd[1]), 3)
                dist = round(math.hypot(pt2[0]- pt1[0], pt2[1]- pt1[1], pt2[2]- pt1[2]), 4)
                if not VEC_INIT :
                    if pt2[1] > pt1[1] :
                        vc_o1 = pt2 - vc_o1a
                    else :
                        vc_o1 = pt1 - vc_o1a
                    print(pt1, pt2)
                    vc_a1_ = vc_o1 + vc_o1a_
                    vc_b1_ = vc_o1 + vc_o1b_
                    vc_c1_ = vc_o1 + vc_o1c_
                    VEC_INIT = True
                    f.write("i,"+str(vc_o1)+","+str(vc_a1_)+","+str(vc_b1_)+str(vc_c1_)+"," +"\n")
                _imu = imu_msg.decode('utf-8').rstrip().split(",")
                if len(_imu) > 3 :
                    r = float(_imu[1])
                    p = float(_imu[2])
                    y = float(_imu[3])
                    rl1l2 = R.from_euler('xyz', [r-r0, p-p0, y-y0], degrees=True)
                    if pt2[1] > pt1[1] :
                        vc_o2 = pt1 - rcl1.apply(rl1l2.apply(vo2a))
                    else :
                        vc_o2 = pt2 - rcl1.apply(rl1l2.apply(vo2a))
                    vc_a2_ = vc_o2 + rcl1.apply(rl1l2.apply(vo2a_))
                    vc_b2_ = vc_o2 + rcl1.apply(rl1l2.apply(vo2b_))
                    vc_c2_ = vc_o2 + rcl1.apply(rl1l2.apply(vo2c_))
                    _tmp_str = "v,"
                    for _m in vc_a2_ :
                        _tmp_str = _tmp_str + str(_m) + ","
                    for _m in vc_b2_ :
                        _tmp_str = _tmp_str + str(_m) + ","
                    for _m in vc_c2_ :
                        _tmp_str = _tmp_str + str(_m) + ","
                    f.write(_tmp_str + "\n")
                    _tmpWemo = wemo_msg.decode('utf-8').rstrip().split(",")

                    f.write("c,"+_tmpWemo[0]+","+_tmpWemo[1]+","+_tmpWemo[2]+","+_tmpWemo[3]+
                            ","+_tmpWemo[4]+","+_tmpWemo[5]+","+_tmpWemo[6]+","+str(_p)+"\n")
        except KeyboardInterrupt:
            pp.stop()
            serWemo.close()
            serIMU.close()
            print("\nclose")
            f.close()
            break
        except :
            pass
