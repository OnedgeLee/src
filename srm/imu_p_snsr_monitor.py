import time, serial, threading

start = 0
r_init = 0
p_init = 0
y_init = 0


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


def ser_init() :
    _ser = serial.Serial(port='/dev/tty.usbserial-0001', baudrate=921600, timeout=0.01)
    _ser.close()
    time.sleep(0.05)
    _ser.open()
    time.sleep(0.05)
    return _ser


def receiving(ser):
    global last_received
    buffer = bytearray()
    while True:
        # last_received = ser.readline()
        buffer += ser.read(ser.inWaiting())
        if b'\n' in buffer:
            last_received, buffer = buffer.split(b'\n')[-2:]


ser = ser_init()
serWemo = serial.Serial(port='/dev/tty.usbserial-1130', baudrate=115200, timeout=0.001)
last_received = bytearray()
threading.Thread(target=receiving, args=(ser,)).start()

f = open("/Users/shetshield/Desktop/res/220209_pd/p_sine_2_0.txt", "w")
rl = ReadLine(serWemo)
while True :
    try:
        _temp = last_received.decode('utf-8').rstrip().split(",")
        if start == 0:
            r_init = float(_temp[1])
            p_init = float(_temp[2])
            y_init = float(_temp[3])
            start = 1
        # _r = float(_temp[1])
        _p = float(_temp[2])
        # _y = float(_temp[3])
        # _r_ = round(_r - r_init, 3)
        # _p_ = round(_p - p_init, 3)
        # _y_ = round(_y - y_init, 3)
        raw = rl.readline()
        parsed = raw_parsing(raw)
        f.write(parsed[0]+","+parsed[1]+","+parsed[2]+","+parsed[3]+
                ","+parsed[4]+","+parsed[5]+","+parsed[6]+","+str(_p)+"\n")
        print(parsed)
    except KeyboardInterrupt:
        serWemo.close()
        ser.close()
        print("\nclose")
        f.close()
        break
    except :
        pass

