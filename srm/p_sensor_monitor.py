import serial, time

ser_ardu = serial.Serial(port='/dev/cu.usbmodem111201', baudrate=115200, timeout=0.01)
ser_wemo = serial.Serial(port='/dev/cu.usbserial-11130', baudrate=115200, timeout=0.01)
time.sleep(0.5)
ser_ardu.close()
ser_wemo.close()
time.sleep(0.5)

ser_ardu.open()
ser_wemo.open()
time.sleep(1)

try :
    while True :
        t1 = time.time()
        data1 = ser_ardu.readline().rstrip()
        data2 = ser_wemo.readline().rstrip()
        # print(data)
        try :
            data1 = data1.decode('utf-8')
            if len(data1) :
                if len(data2) :
                    t2 = time.time()
                    elapsed = round(t2 - t1, 4)
                    data2 = data2.decode('utf-8')
                    print(elapsed, ",", data1, ",", data2)
                    t1 = t2
        except :
            pass
except :
    ser_ardu.close()
    ser_wemo.close()
