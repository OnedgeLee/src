#%%
import serial, time
import numpy as np

def raw_to_data(_raw) :
    '''
        # _raw: raw data(Euler Angle) from IMU
    '''
    _index = list()
    _raw = _raw.rstrip("\\r\\n")
    for i in range(5, len(_raw)) :
        _temp = _raw[i]
        if _temp == ',' :
            _index.append(i)
    _roll  = float(_raw[_index[0]+1:_index[1]])
    _pitch = float(_raw[_index[1]+1:_index[2]])
    _yaw   = float(_raw[_index[2]+1:_index[3]])
    _ax    = float(_raw[_index[3]+1:_index[4]])
    _ay    = float(_raw[_index[4]+1:_index[5]])
    _az    = float(_raw[_index[5]+1:len(_raw)-2])
    return [_roll, _pitch, _yaw], [_ax, _ay, _az]

def main() :
    serImu = serial.Serial(port='COM11', baudrate=921600, timeout=0.001)
    serImu.close()
    time.sleep(0.5)
    serImu.open()
    time.sleep(0.5)

    try :
        roll0  = 0
        pitch0 = 0
        yaw0   = 0
        moving_avg = 5
        fname_euler = '/Users/shetshield/Desktop/python_ws/euler_'
        fname_accel = '/Users/shetshield/Desktop/python_ws/accel_'
        cnt = 1

        print("press 'i' to start streaming")
        keyIn = input()
        while keyIn != 'i' :
            keyIn = input()
        print('start')

        for _ in range(moving_avg) :
            raw_data = serImu.readline()
            print(raw_data)
            euler, accel = raw_to_data(raw_data.decode('ascii'))
            roll0  += euler[0]
            pitch0 += euler[1]
            yaw0   += euler[2]
        roll0  /= float(moving_avg)
        pitch0 /= float(moving_avg)
        yaw0   /= float(moving_avg)
        serImu.reset_input_buffer()
        time.sleep(0.001)
        
        # _st = time.time()
        arr1 = list()
        arr2 = list()
        buffer = b''
        while True :
            try :
                waiting = serImu.in_waiting
                # print(waiting)
                if waiting > 0 :
                    buffer += serImu.read(waiting)
                    euler, accel = raw_to_data(buffer.decode('ascii'))
                    arr1.append(euler)
                    arr2.append(accel)
                    # print(euler)
                buffer = b''
                if len(arr1) > 199 :
                    # print(time.time()-_st)
                    np.savetxt(fname_euler + str(cnt) + '.csv', arr1, delimiter=',')
                    np.savetxt(fname_accel + str(cnt) + '.csv', arr2, delimiter=',')
                    arr1 = list()
                    arr2 = list()
                    print("count", cnt)
                    cnt += 1
                    if cnt == 10 :
                        break
            except KeyboardInterrupt :
                break
            except :
                pass
        print("serial close")
        serImu.close()
    except :
        serImu.close()
        print("\nExit")

if __name__=="__main__" :
    main()