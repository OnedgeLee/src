#!/usr/bin/env python
import serial, time, rospy
from std_msgs.msg import String
from math import degrees, atan, sqrt

mv_avg   = 30
time_thr = 0.004
min_angle_diff = 0.01
r   = 1
p   = 2
y   = 3
ax  = 4
ay  = 5
az  = 6
WIN = False

rospy.init_node("imu_processing", anonymous=False)
rate = rospy.Rate(1000)
class ReadLine:
    def __init__(self, s) :
        self.buf = bytearray()
        self.s   = s
        
    def readline(self) :
        i = self.buf.find(b'\n')
        if i >= 0 :
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True :
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b'\n')
            
            if i >= 0 :
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else :
                self.buf.extend(data)


def raw_parsing(_raw) :
    # print(_raw)
    _parsed = _raw.decode().split(',')
    return _parsed

def ser_init() :
    if WIN :
        _ser = serial.Serial(port='COM5', baudrate=921600)
    else :
        _ser = serial.Serial(port='/dev/ttyUSB1', baudrate=921600)
    _ser.close()
    time.sleep(0.3)
    _ser.open()
    time.sleep(0.3)
    return _ser

def angle_init(_rl, _mvavg) :
    time.sleep(1)
    # _r, _p, _y = 0, 0, 0
    _r, _p = 0, 0
    while True :
        if len(_rl.readline()) > 0 :
            break
    for _ in range(_mvavg) :
        _parsed = raw_parsing(_rl.readline())
        _r += float(_parsed[r])
        _p += float(_parsed[p])
        # _y += float(_parsed[y])
    _r = _r/_mvavg
    _p = _p/_mvavg
    # _y = _y/_mvavg
    # return _r, _p, _y
    return _r, _p

def main() :
    pub_imu_data = rospy.Publisher('imu_data', String, queue_size=10)
    ser = ser_init()
    rl  = ReadLine(ser)
    r0, p0 = angle_init(rl, mv_avg)
    f_dir  = 0
    # r0, p0, y0 = angle_init(rl, mv_avg)
    # print("r, p init value", r0, p0)
    R0, P0 = r0, p0
    t0 = time.time()
    while not rospy.is_shutdown() :
        try :
            raw        = rl.readline()
            parsed     = raw_parsing(raw)
            # R, P, Y    = float(parsed[r]), float(parsed[p]), float(parsed[y])
            t1 = time.time()
            elapsed = t1 - t0
            # print("elapsed", elapsed)
            R, P       = float(parsed[r]), float(parsed[p])
            aX, aY, aZ = float(parsed[ax]), float(parsed[ay]), float(parsed[az])
            if elapsed > time_thr :
                r_diff, p_diff = R-R0, P-P0
                r_rate, p_rate = r_diff/elapsed, p_diff/elapsed
                # print("rp, %.4f, %.4f, %.4f, %.4f" %(R, P, round(r_rate, 2), round(p_rate, 2)))
                try :
                    angle = degrees(atan(abs(r_diff/p_diff)))
                    if p_diff > min_angle_diff :
                        if r_diff > min_angle_diff :
                            f_dir = 4
                        elif r_diff < -min_angle_diff :
                            f_dir = 3
                        elif r_diff > 0 :
                            f_dir = 4
                        else :
                            f_dir = 3
                    elif p_diff < -min_angle_diff :
                        if r_diff > min_angle_diff :
                            f_dir = 1
                        elif r_diff < -min_angle_diff :
                            f_dir = 2
                        elif r_diff > 0 :
                            f_dir = 1
                        else :
                            f_dir = 2
                    elif p_diff > 0 :
                        if r_diff > min_angle_diff :
                            f_dir = 4
                        elif r_diff < -min_angle_diff :
                            f_dir = 3
                    elif p_diff < 0 :
                        if r_diff > min_angle_diff :
                            f_dir = 1
                        elif r_diff < -min_angle_diff :
                            f_dir = 2
                        # put elif here for abs(r_diff) < 0 ?

                    magnitude = round(sqrt(r_rate**2 + p_rate**2), 2)
                    pub_msg   = str(f_dir) + "," + str(R-r0) + "," + str(P-p0) + "," + str(round(angle, 2)) + "," + str(magnitude)
                    # print(pub_msg)
                    pub_imu_data.publish(pub_msg)
                    print("angle", round(angle, 2), round((R-R0), 2), round((P-P0), 2), "magnitude", magnitude)
                except ZeroDivisionError :
                    if p_diff < 0 :
                        f_dir = 2
                        angle = 0
                        magnitude = round(abs(p_diff/elapsed), 2)
                        pub_msg   = str(f_dir) + "," + str(R-r0) + "," + str(P-p0) + "," + str(round(angle, 2)) + "," + str(magnitude)
                        pub_imu_data.publish(pub_msg)
                    else :
                        f_dir = 4
                        angle = 0
                        magnitude = round(abs(p_diff/elapsed), 2)
                        pub_msg   = str(f_dir) + "," + str(R-r0) + "," + str(P-p0) + "," + str(round(angle, 2)) + "," + str(magnitude)
                        pub_imu_data.publish(pub_msg)
                # R0, P0 and time Update
                R0, P0 = R, P
                t0 = t1
                rate.sleep()

        except KeyboardInterrupt :
            ser.close()
            print("\nclose")
            break
        except :
            pass

if __name__=="__main__" :
    main()