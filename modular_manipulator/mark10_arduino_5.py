import serial
import time
import re

## Mark10
mark = serial.Serial('COM5', 115200, timeout=1)
ardu = serial.Serial('COM12', 115200, timeout=0.05)
mark.write(b's')
time.sleep(0.1)
mark.write(b'e0100.0') #mark.write(b'e0225.0')
time.sleep(0.5)
mark.write(b'a')
speed = float(re.sub("[^0-9.\-]","",mark.readline().decode('utf8')))
print(speed)

mark.write(b'z')
time.sleep(0.1)


## Mark10 - force
#markF = serial.Serial('COM4', 115200, timeout=1)
#time.sleep(0.1)


## Arduino
"""
arduino = serial.Serial('COM10', 250000, timeout=1)
arduino.reset_input_buffer()
time.sleep(3.0)
for i in range(20):
    arduino.write("A".encode("utf-8"))
    res = arduino.readline().decode("utf-8").strip()
    print(res)
    time.sleep(0.1)
"""

## Log
f = open("strain.txt", "w")

## Setup
target_dist = 10.0
num=0

## Start
startTime = time.time()
try:
    dist = 0
    force = 0    
    for i in range(20): #cycle number
        print(i)
        mark.write(b'u')
        #while(dist > target_dist): # travel distance
        while(dist < target_dist): # travel distance
            #mark.write(b'x')
            mark.write(b'n')
            #markF.write(b'?\r\n')
            #arduino.write("A".encode("utf-8"))
            # print(markF.readline().decode('utf8'))

            force= float(re.sub("[^0-9.\-]","",mark.readline().decode('utf8')))
            dist = float(re.sub("[^0-9.\-]","",mark.readline().decode('utf8')))
            res = ardu.readline().decode("utf-8").strip()
            
            # res = arduino.readline().decode("utf-8").strip()
            print(dist, force, res)

            time_ = time.time() - startTime
            f.write(str(time_) + "," + str(dist) + "," + str(force) +  "," + str(res) + "\n")
        mark.write(b's')
        for i in range(3):
            # mark.write(b'x') # mark.write(b'n')
            # markF.write(b'?\r\n')
            mark.write(b'n')            
            # arduino.write("A".encode("utf-8"))

            force = float(re.sub("[^0-9.\-]","",mark.readline().decode('utf8')))
            dist = float(re.sub("[^0-9.\-]","",mark.readline().decode('utf8')))
            res = ardu.readline().decode("utf-8").strip()

            # res = arduino.readline().decode("utf-8").strip()
            print("s", dist, force, res)

            time_ = time.time() - startTime
            f.write(str(time_) + "," + str(dist) + "," + str(force) +  "," + str(res) + "\n")


        mark.write(b'd')
        #while(dist < 0):
        while(dist > 0):
            mark.write(b'n') # mark.write(b'n')
            # markF.write(b'?\r\n')
            # arduino.write("A".encode("utf-8"))

            force = float(re.sub("[^0-9.\-]","",mark.readline().decode('utf8')))
            dist = float(re.sub("[^0-9.\-]","",mark.readline().decode('utf8')))
            res = ardu.readline().decode("utf-8").strip()

            # res = arduino.readline().decode("utf-8").strip()
            print(dist, force, res)

            time_ = time.time() - startTime
            f.write(str(time_) + "," + str(dist) + "," + str(force) +  "," + str(res) + "\n")

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
