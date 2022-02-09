import serial, time


class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b'\n')
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b'\n')

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
    _ser = serial.Serial(port='/dev/tty.usbserial-0001', baudrate=921600, timeout=0.001)
    _ser.close()
    time.sleep(0.2)
    _ser.open()
    time.sleep(0.2)

    return _ser

def main() :
    ser = ser_init()
    rl  = ReadLine(ser)

    while True :
        try :
            raw    = rl.readline()
            parsed = raw_parsing(raw)
            print(parsed)
        except KeyboardInterrupt :
            ser.close()
            print("\nclose")
            break
        except :
            pass

if __name__ == "__main__" :
    main()