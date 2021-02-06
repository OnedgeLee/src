#%%
import serial, time
import matplotlib.pyplot as plt
from math import degrees, atan

mv_avg   = 30
time_thr = 0.004
r  = 1
p  = 2
y  = 3
ax = 4
ay = 5
az = 6

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
    _ser = serial.Serial(port='COM5', baudrate=921600)
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
    ser = ser_init()
    rl  = ReadLine(ser)
    r0, p0 = angle_init(rl, mv_avg)
    # r0, p0, y0 = angle_init(rl, mv_avg)
    # print("r, p init value", r0, p0)
    R0, P0 = r0, p0
    t0 = time.time()
    while True :
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
                r_rate = (R - R0)
                p_rate = (P - P0)
                # print("rp, %.4f, %.4f, %.4f, %.4f" %(R, P, round(r_rate, 2), round(p_rate, 2)))
                try :
                    angle = degrees(atan(p_rate/r_rate))
                    print("angle", round(angle, 2))
                except ZeroDivisionError :
                    if abs(p_rate) > 0 :
                        angle = 90
                        # print(angle)
                # R0, P0 and time Update
                R0, P0 = R, P
                t0 = t1

        except KeyboardInterrupt :
            ser.close()
            print("\nclose")
            break
        except :
            pass

if __name__=="__main__" :
    main()