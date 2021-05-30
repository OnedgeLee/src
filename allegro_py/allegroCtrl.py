#%%
import sys
sys.path.append("/Users/user/Downloads/PCAN-Basic API/samples/python")
from PCANBasic import *
from math import pi, degrees, radians
import threading, time, struct
import numpy as np

# CAN Comm. Instance
pcan = PCANBasic()

# Define CAN Channel
PCAN_CH = PCAN_USBBUS1
CAN_ID  = 0

# Define Baud-Rate
PCAN_BAUD = PCAN_BAUD_1M

# Define ID
SET_TORQUE_1 = 0x60+0
SET_TORQUE_2 = 0x60+1
SET_TORQUE_3 = 0x60+2
SET_TORQUE_4 = 0x60+3
SET_PERIOD   = 0x81
SET_POSE_1   = 0xE0+0
SET_POSE_2   = 0xE0+1
SET_POSE_3   = 0xE0+2
SET_POSE_4   = 0xE0+3
CMD_SYS_ON   = 0x40
CMD_SYS_OFF  = 0x41
FINGER_POS_1 = 0x20+0
FINGER_POS_2 = 0x20+1
FINGER_POS_3 = 0x20+2
FINGER_POS_4 = 0x20+3
# ID List
FINGER_IDS   = [FINGER_POS_1, FINGER_POS_2, FINGER_POS_3, FINGER_POS_4]
POSE_IDS     = [SET_POSE_1, SET_POSE_2, SET_POSE_3, SET_POSE_4]
TORQUE_IDS   = [SET_TORQUE_1, SET_TORQUE_2, SET_TORQUE_3, SET_TORQUE_4]

# Define MSG Type
RTR_MSG = PCAN_MESSAGE_RTR
STD_MSG = PCAN_MESSAGE_STANDARD

# Define Constant
MAX_BUS = 256 # 256
MAX_DOF = 16  # 16
HZ      = 333.3
RESOL   = 65536.0

# Define PWM Limit for Fingers except Thumb
PWM_LIMIT_ROLL = 250.0 * 1.5
PWM_LIMIT_NEAR = 450.0 * 1.5
PWM_LIMIT_MID  = 300.0 * 1.5
PWM_LIMIT_FAR  = 190.0 * 1.5

# PWM Limit For Thumb
PWM_LIMIT_T_ROLL = 350.0 * 1.5
PWM_LIMIT_T_NEAR = 270.0 * 1.5
PWM_LIMIT_T_MID  = 180.0 * 1.5
PWM_LIMIT_T_FAR  = 180.0 * 1.5

# Torque Conversion Constant
TAU_CONV_CONST   = 1200.0
PWM_ABS_LIMIT    = 1200.0


# Initializing CAN Comm.
res = pcan.Initialize(PCAN_CH, PCAN_BAUD)

homePos = [ 0,  10, 45, 45,
            0, -10, 45, 45,
            5,  -5, 50, 45,
           60,  25, 15, 45]

""" Define Function """
def cmd_req_finger_pose(_ch, _ind) :
    if _ind == "a" :
        _j = np.zeros((4, 4))
    else :
        _j = np.zeros((1, 4))
    if _ind == "a" :
        for _i, _ID in enumerate(FINGER_IDS) :
            _msg = TPCANMsg()
            _msg.ID  = (_ID << 2) | CAN_ID
            _msg.LEN = 0
            _msg.MSGTYPE = RTR_MSG
            _res = pcan.Write(_ch, _msg)
            _res = pcan.Read(_ch)
            # if _res[0] != PCAN_ERROR_QRCVEMPTY :
            if _res[1].LEN > 0 :
                # print("LENGTH", _res[1].LEN)
                _data1 = round((_res[1].DATA[0] | (_res[1].DATA[1] << 8))*HZ/RESOL, 2)
                _data2 = round((_res[1].DATA[2] | (_res[1].DATA[3] << 8))*HZ/RESOL, 2)
                _data3 = round((_res[1].DATA[4] | (_res[1].DATA[5] << 8))*HZ/RESOL, 2)
                _data4 = round((_res[1].DATA[6] | (_res[1].DATA[7] << 8))*HZ/RESOL, 2)
                print("FINGER_%s" %(_ID-31), "%6.2f deg" %(_data1), 
                      "%6.2f deg" %(_data2), "%6.2f deg" %(_data3), "%6.2f deg" %(_data4))
                _j[_i, 0] = _data1
                _j[_i, 1] = _data2
                _j[_i, 2] = _data3
                _j[_i, 3] = _data4
    else :
        _msg = TPCANMsg()
        _ID  = FINGER_POS_1
        _msg.ID  = (_ID << 2) | CAN_ID
        _msg.LEN = 0
        _msg.MSGTYPE = RTR_MSG
        _res = pcan.Write(_ch, _msg)
        _res = pcan.Read(_ch)
        # if _res[0] != PCAN_ERROR_QRCVEMPTY :
        if _res[1].LEN > 0 :
            # print("LENGTH", _res[1].LEN)
            _data1 = round((_res[1].DATA[0] | (_res[1].DATA[1] << 8))*HZ/RESOL, 2)
            _data2 = round((_res[1].DATA[2] | (_res[1].DATA[3] << 8))*HZ/RESOL, 2)
            _data3 = round((_res[1].DATA[4] | (_res[1].DATA[5] << 8))*HZ/RESOL, 2)
            _data4 = round((_res[1].DATA[6] | (_res[1].DATA[7] << 8))*HZ/RESOL, 2)
            # print("FINGER_%s" %(_ID-31), "%6.2f deg" %(_data1), 
            #      "%6.2f deg" %(_data2), "%6.2f deg" %(_data3), "%6.2f deg" %(_data4))
            _j[0, 0] = _data1
            _j[0, 1] = _data2
            _j[0, 2] = _data3
            _j[0, 3] = _data4
            # _j.append(_tmp)
    return _j

def cmd_set_finger_pose(_ch, _fP) :
    # _fP : Finger Pose Vector
    for _ID in POSE_IDS :
        # MSG Structure
        _msg = TPCANMsg()
        _msg.ID  = (_ID << 2) | CAN_ID
        _msg.LEN = 8
        _msg.MSGTYPE = STD_MSG

        # Finger Pose Set
        _msg.DATA[0] = ((_fP[0])      & 0x00ff)
        _msg.DATA[1] = ((_fP[0] >> 8) & 0x00ff)

        _msg.DATA[2] = ((_fP[1])      & 0x00ff)
        _msg.DATA[3] = ((_fP[1] >> 8) & 0x00ff)

        _msg.DATA[4] = ((_fP[2])      & 0x00ff)
        _msg.DATA[5] = ((_fP[2] >> 8) & 0x00ff)

        _msg.DATA[6] = ((_fP[3])      & 0x00ff)
        _msg.DATA[7] = ((_fP[3] >> 8) & 0x00ff)

        _ = pcan.Write(_ch, _msg)

def cmd_set_finger_torque(_ch, _tq, _ind) :
    if _ind == "a" :
        for _ID in TORQUE_IDS :
            # MSG Structure
            _msg = TPCANMsg()
            _msg.ID  = (_ID << 2) | CAN_ID
            _msg.LEN = 8
            _msg.MSGTYPE = STD_MSG

            # Finger Pose Set
            _msg.DATA[0] = ((_tq[0])      & 0x00ff)
            _msg.DATA[1] = ((_tq[0] >> 8) & 0x00ff)

            _msg.DATA[2] = ((_tq[1])      & 0x00ff)
            _msg.DATA[3] = ((_tq[1] >> 8) & 0x00ff)

            _msg.DATA[4] = ((_tq[2])      & 0x00ff)
            _msg.DATA[5] = ((_tq[2] >> 8) & 0x00ff)

            _msg.DATA[6] = ((_tq[3])      & 0x00ff)
            _msg.DATA[7] = ((_tq[3] >> 8) & 0x00ff)

            _ = pcan.Write(_ch, _msg)
    else :
        # Set 1 Finger
        _msg     = TPCANMsg()
        _ID      = SET_TORQUE_1
        _msg.ID  = (_ID << 2) | CAN_ID
        _msg.LEN = 8
        _msg.MSGTYPE = STD_MSG

        _msg.DATA[0] = ((_tq[0])      & 0x00ff)
        _msg.DATA[1] = ((_tq[0] >> 8) & 0x00ff)

        _msg.DATA[2] = ((_tq[1])      & 0x00ff)
        _msg.DATA[3] = ((_tq[1] >> 8) & 0x00ff)

        _msg.DATA[4] = ((_tq[2])      & 0x00ff)
        _msg.DATA[5] = ((_tq[2] >> 8) & 0x00ff)

        _msg.DATA[6] = ((_tq[3])      & 0x00ff)
        _msg.DATA[7] = ((_tq[3] >> 8) & 0x00ff)

        _ = pcan.Write(_ch, _msg)

def cmd_set_period(_ch) :
    _ID  =  SET_PERIOD
    _msg = TPCANMsg()
    _msg.ID  = (_ID << 2) | CAN_ID
    _msg.LEN = 6
    _period  = [3, 0, 0]
    _msg.MSGTYPE = STD_MSG
    _msg.DATA[0] = ((_period[0])      & 0x00ff)
    _msg.DATA[1] = ((_period[0] >> 8) & 0x00ff)
    _msg.DATA[2] = ((_period[1])      & 0x00ff)
    _msg.DATA[3] = ((_period[1] >> 8) & 0x00ff)
    _msg.DATA[4] = ((_period[2])      & 0x00ff)
    _msg.DATA[5] = ((_period[2] >> 8) & 0x00ff)
    _ = pcan.Write(_ch, _msg)
    print("Period Set - Done", _period)

def cmd_servo_on(_ch) :
    _ID  = CMD_SYS_ON
    _msg = TPCANMsg()
    _msg.ID  = (_ID << 2) | CAN_ID
    _msg.LEN = 0
    _msg.MSGTYPE = STD_MSG
    _ = pcan.Write(_ch, _msg)
    print("Servo On - Done")

def cmd_servo_off(_ch) :
    _ID  = CMD_SYS_OFF
    _msg = TPCANMsg()
    _msg.ID  = (_ID << 2) | CAN_ID
    _msg.LEN = 0
    _msg.MSGTYPE = STD_MSG
    _ = pcan.Write(_ch, _msg)
    print("Servo Off - Done")

def cmd_hand_preprocess(_ch) :
    cmd_servo_on(_ch)
    print("Hand Ready")

try :
    # cmd_hand_preprocess(PCAN_CH)
    cmd_set_period(PCAN_CH)
    prev_pos          = np.zeros((1, 4))
    cur_pos_filtered  = np.zeros((1, 4))
    prev_pos_filtered = np.zeros((1, 4))
    prev_vel          = np.zeros((1, 4))
    cur_vel           = np.zeros((1, 4))

    counter = 0
    while abs(prev_pos[0][0]) < 0.01 :
        prev_pos = np.radians(cmd_req_finger_pose(PCAN_CH, "b"))
        counter += 1
    t1 = time.time()
    print(prev_pos, counter)
    while True :
        cur_pos = np.radians(cmd_req_finger_pose(PCAN_CH, "b"))
        if len(cur_pose) > 0 :
            t2 = time.time()
            elapsed = t2 - t1
            if elapsed > 0.005 :
                t1 = t2
                print(cur_pos, prev_pos, elapsed)
                for i in range(len(cur_pos_filtered.shape[1])) :
                    cur_pos_filtered[0, i] = 0.6 * cur_pos_filtered[0, i] \
                                          + 0.198 * prev_pos[0, i] + 0.198 * cur_pos[0, i]
                    cur_vel[0, i] = (cur_pos_filtered[0, i] - prev_pos_filtered[0, i])/elapsed
                    cur_vel_filtered[0, i] = (0.6 * cur_vel_filtered[0, i]) + \
                                          + (0.198 * prev_vel[0, i]) + (0.198 * cur_vel[0, i])
                    cur_vel[0, i] = (cur_pos[0, i] - prev_pos[0, i])/elapsed

                    # previous attribute update
                    prev_pos[0, i] = cur_pos[0, i]
                    prev_pos_filtered[0, i] = cur_pos_filtered[0, i]
                    prev_vel[0, i] = cur_vel[0, i]
        else :
            pass
    """
    key = input()
    if key == "1" :
        st = time.time()
        cmd_servo_on(PCAN_CH)
        while time.time() - st < 10 :
            desired_torque = [100, -250, 250, 50]
            cmd_set_finger_torque(PCAN_CH, desired_torque, "a")
    elif key == "2" :
        desried_torque = [0, 0, 0, 0]
        cmd_set_finger_torque(PCAN_CH, desired_torque, "a")
    """
except :
    print("Closed")
    cmd_servo_off(PCAN_CH)
    pcan.Uninitialize(PCAN_CH)
