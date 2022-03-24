import re
import time, serial, threading


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
    _ser = serial.Serial(port='/dev/tty.usbmodem11201', baudrate=115200, timeout=0.01)
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
# serWemo = serial.Serial(port='/dev/tty.usbserial-1130', baudrate=115200, timeout=0.001)
last_received = bytearray()
threading.Thread(target=receiving, args=(ser,)).start()

f_dir = "/Users/shetshield/Desktop/res/220324_string_calibration/"
snsr_num = 1
f_name = "snsr_" + str(snsr_num) + ".txt"
f = open(f_dir+f_name, "w")

## Mark10
mark = serial.Serial('COM5', 115200, timeout=1)
# ardu = serial.Serial('COM12', 115200, timeout=0.05)
mark.write(b's')
time.sleep(0.1)
mark.write(b'e0330.0')  # mark.write(b'e0225.0')
time.sleep(0.5)
mark.write(b'a')
speed = float(re.sub("[^0-9.\-]", "", mark.readline().decode('utf8')))
print(speed)

mark.write(b'z')
time.sleep(3)

target_dist = 70.0
cycle_num = 11

## Start
startTime = time.time()
try:
    dist = 0
    force = 0
    for i in range(cycle_num):  # cycle number
        print(i)
        mark.write(b'u')
        # while(dist > target_dist): # travel distance
        while (dist < target_dist):  # travel distance
            # mark.write(b'x')
            mark.write(b'n')
            # markF.write(b'?\r\n')
            # arduino.write("A".encode("utf-8"))
            # print(markF.readline().decode('utf8'))

            force = float(re.sub("[^0-9.\-]", "", mark.readline().decode('utf8')))
            dist = float(re.sub("[^0-9.\-]", "", mark.readline().decode('utf8')))
            _temp = last_received.decode('utf-8').rstrip().split(",")
            _tmp = _temp[0]

            # res = arduino.readline().decode("utf-8").strip()
            print(i, dist, force, _tmp)

            time_ = time.time() - startTime
            f.write(str(i) + "," + str(time_) + "," + str(dist) + "," + str(force) + "," + str(_tmp) + "\n")
        mark.write(b's')
        for j in range(3):
            # mark.write(b'x') # mark.write(b'n')
            # markF.write(b'?\r\n')
            mark.write(b'n')
            # arduino.write("A".encode("utf-8"))

            force = float(re.sub("[^0-9.\-]", "", mark.readline().decode('utf8')))
            dist = float(re.sub("[^0-9.\-]", "", mark.readline().decode('utf8')))
            _temp = last_received.decode('utf-8').rstrip().split(",")
            _tmp = _temp[0]

            # res = arduino.readline().decode("utf-8").strip()
            print(i, dist, force, _tmp)

            time_ = time.time() - startTime
            f.write(str(i) + "," + str(time_) + "," + str(dist) + "," + str(force) + "," + str(_tmp) + "\n")

        mark.write(b'd')
        # while(dist < 0):
        while (dist > 0):
            mark.write(b'n')  # mark.write(b'n')
            # markF.write(b'?\r\n')
            # arduino.write("A".encode("utf-8"))

            force = float(re.sub("[^0-9.\-]", "", mark.readline().decode('utf8')))
            dist = float(re.sub("[^0-9.\-]", "", mark.readline().decode('utf8')))
            _temp = last_received.decode('utf-8').rstrip().split(",")
            _tmp = _temp[0]


            # res = arduino.readline().decode("utf-8").strip()
            print(i, dist, force, _tmp)

            time_ = time.time() - startTime
            f.write(str(i) + "," + str(time_) + "," + str(dist) + "," + str(force) + "," + str(_tmp) + "\n")

        mark.write(b's')
        time.sleep(0.1)

    f.close()

except KeyboardInterrupt:
    mark.write(b's')
    f.close()
    mark.close()
    raise

except:
    mark.write(b's')
    f.close()
    mark.close()
