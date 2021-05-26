# !/usr/bin/env python

import sys
sys.path.append("/home/robot/Downloads/PCAN-Basic_Linux-4.4.2/libpcanbasic/examples/python")
from PCANBasic import *
pcan = PCANBasic()
res  = pcan.Initialize(PCAN_USBBUS1, PCAN_BAUD_1M)

msg = TPCANMsg()
msg.ID  = (0x88<<2) | 0
msg.LEN = 0
msg.MSGTYPE = TPCANMessageType(0x01)

try :
    while True :
        res = pcan.Write(PCAN_USBBUS1, msg)
        res = pcan.Read(PCAN_USBBUS1)
        if res[0] != PCAN_ERROR_QRCVEMPTY :
            res = pcan.Read(PCAN_USBBUS1)
            if res[1].LEN > 0 :
                for i in range(res[1].LEN) :
                    _tmp = bytes(res[1].DATA[i])
                    # print(_tmp)
                    print(_tmp.decode('ascii'), res[1].DATA[i])
                print("")
        else :
            pass
except :
    print("Closed")
    pcan.Uninitialize(PCAN_USBBUS1)