from tkinter import *
import socket, serial, threading, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np

AT_HOME = True

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
    time.sleep(0.2)
    _ser.open()
    time.sleep(0.2)
    return _ser


def receiving(ser):
    global last_received
    buffer = bytearray()
    while True:
        # last_received = ser.readline()
        buffer += ser.read(ser.inWaiting())
        if b'\n' in buffer:
            last_received, buffer = buffer.split(b'\n')[-2:]

try :
    ser = ser_init()
    last_received = bytearray()
    threading.Thread(target=receiving, args=(ser,)).start()
except :
    pass


class BackgroundTask() :
    def __init__(self, taskFuncPointer) :
        self.__taskFuncPointer_ = taskFuncPointer
        self.__workerThread_ = None
        self.__isRunning_ = False

    def taskFuncPointer(self) :
        return self.__taskFuncPointer_

    def isRunning(self) :
        return self.__isRunning_ and self.__workerThread_.is_alive()

    def start(self) :
        if not self.__isRunning_ :
            self.__isRunning_ = True
            self.__workerThread_ = self.WorkerThread(self)
            self.__workerThread_.start()

    def stop(self) :
        self.__isRunning_ = False

    class WorkerThread(threading.Thread) :
        def __init__(self, bgTask) :
            threading.Thread.__init__(self)
            self.__bgTask_ = bgTask

        def run(self) :
            try:
                self.__bgTask_.taskFuncPointer()(self.__bgTask_.isRunning)
            except Exception as e:
                print(repr(e))
            self.__bgTask_.stop()

def ControlPanel():
    from tkinter import Tk, Label, Button, StringVar, Canvas
    from time import sleep

    class UnitTestGUI:

        def __init__(self, master):
            # self.ser = ser_init()
            # self.rl = ReadLine(self.ser)
            self.master = master
            master.title("Control Panel")
            self.start = 0
            if AT_HOME :
                self._r_ = 171.5
                self._p_ = 171.5
                self._y_ = 171.5
            else :
                self._r_ = 0
                self._p_ = 0
                self._y_ = 0

            # self.wemos_IP = "192.168.0.130"
            # self.wemos_IP = "192.168.0.12"
            self.m1_IP = "192.168.0.130"
            self.m2_IP = "192.168.0.12"

            self.canvas = Canvas(master, width=60)
            '''
                Solenoid Valve Control Button
                2 6 10 / +0.001 +0.01 -0.001 -0.001 
            '''
            self.mod_ctrlL = Label(
                self.master, text="Controller", width=10, height=2, fg='black',
                font=("Times New Roman", 12, "bold"), relief='solid', bg='white'
            )
            self.mod_ctrlL.grid(column=0, row=0)
            self.mod_comm_startB = Button(
                self.master, text="start", command=self.mod_comm_startClicked,
                width=6, height=2, fg='blue', font=("Times New Roman", 12, "bold"))
            self.mod_comm_startB.grid(column=1, row=0)
            self.mod_comm_stopB = Button(
                self.master, text="stop", command=self.mod_comm_stopClicked, width=6, height=2,
                fg='red', font=("Times New Roman", 12, "bold"))
            self.mod_comm_stopB.grid(column=2, row=0)

            # Module1 Sol. Valve Group 2
            self.m1_2p1B = Button(
                self.master, text="+1", command=self.m1_2p1Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_2p1B.grid(column=0, row=1)
            self.m1_2m1B = Button(
                self.master, text="-1", command=self.m1_2m1Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_2m1B.grid(column=0, row=2)
            self.m1_2p10B = Button(
                self.master, text="+10", command=self.m1_2p10Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_2p10B.grid(column=0, row=3)
            self.m1_2m10B = Button(
                self.master, text="-10", command=self.m1_2m10Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_2m10B.grid(column=0, row=4)
            self.m1_2p100B = Button(
                self.master, text="+100", command=self.m1_2p100Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_2p100B.grid(column=0, row=5)
            self.m1_2p1000B = Button(
                self.master, text="+1000", command=self.m1_2p1000Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_2p1000B.grid(column=0, row=6)

            # Module1 Sol. Valve Group 6
            self.m1_6p1B = Button(
                self.master, text="+1", command=self.m1_6p1Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_6p1B.grid(column=1, row=1)
            self.m1_6m1B = Button(
                self.master, text="-1", command=self.m1_6m1Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_6m1B.grid(column=1, row=2)
            self.m1_6p10B = Button(
                self.master, text="+10", command=self.m1_6p10Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_6p10B.grid(column=1, row=3)
            self.m1_6m10B = Button(
                self.master, text="-10", command=self.m1_6m10Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_6m10B.grid(column=1, row=4)
            self.m1_6p100B = Button(
                self.master, text="+100", command=self.m1_6p100Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_6p100B.grid(column=1, row=5)
            self.m1_6p1000B = Button(
                self.master, text="+1000", command=self.m1_6p1000Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_6p1000B.grid(column=1, row=6)

            # Module1 Sol. Valve Group 10
            self.m1_10p1B = Button(
                self.master, text="+1", command=self.m1_10p1Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_10p1B.grid(column=2, row=1)
            self.m1_10m1B = Button(
                self.master, text="-1", command=self.m1_10m1Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_10m1B.grid(column=2, row=2)
            self.m1_10p10B = Button(
                self.master, text="+10", command=self.m1_10p10Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_10p10B.grid(column=2, row=3)
            self.m1_10m10B = Button(
                self.master, text="-10", command=self.m1_10m10Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_10m10B.grid(column=2, row=4)
            self.m1_10p100B = Button(
                self.master, text="+100", command=self.m1_10p100Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_10p100B.grid(column=2, row=5)
            self.m1_10p1000B = Button(
                self.master, text="+1000", command=self.m1_10p1000Clicked, width=6, height=2,
                font=("Times New Roman", 11, "bold")
            )
            self.m1_10p1000B.grid(column=2, row=6)

            # Variable to display applied voltage of M1
            self.m1_2pV = StringVar()
            self.m1_2mV = StringVar()
            self.m1_6pV = StringVar()
            self.m1_6mV = StringVar()
            self.m1_10pV = StringVar()
            self.m1_10mV = StringVar()
            self.m1_2pVL = Label(self.master, textvariable=self.m1_2pV,
                                 width=6, height=2, fg='blue', font=("Times New Roman", 12, "bold"))
            self.m1_2pVL.grid(column=0, row=7)
            self.m1_2mVL = Label(self.master, textvariable=self.m1_2mV,
                                 width=6, height=2, fg='red', font=("Times New Roman", 12, "bold"))
            self.m1_2mVL.grid(column=0, row=8)
            self.m1_6pVL = Label(self.master, textvariable=self.m1_6pV,
                                 width=6, height=2, fg='blue', font=("Times New Roman", 12, "bold"))
            self.m1_6pVL.grid(column=1, row=7)
            self.m1_6mVL = Label(self.master, textvariable=self.m1_6mV,
                                 width=6, height=2, fg='red', font=("Times New Roman", 12, "bold"))
            self.m1_6mVL.grid(column=1, row=8)
            self.m1_10pVL = Label(self.master, textvariable=self.m1_10pV,
                                  width=6, height=2, fg='blue', font=("Times New Roman", 12, "bold"))
            self.m1_10pVL.grid(column=2, row=7)
            self.m1_10mVL = Label(self.master, textvariable=self.m1_10mV,
                                  width=6, height=2, fg='red', font=("Times New Roman", 12, "bold"))
            self.m1_10mVL.grid(column=2, row=8)

            self.m1_p2_snsr = StringVar()
            self.m1_p2_snsrL = Label(self.master, textvariable=self.m1_p2_snsr,
                                     width=8, height=2, fg='blue', font=("Times New Roman", 12, 'bold'))
            self.m1_p2_snsrL.grid(column=0, row=9)
            self.m1_p6_snsr = StringVar()
            self.m1_p6_snsrL = Label(self.master, textvariable=self.m1_p6_snsr,
                                     width=8, height=2, fg='blue', font=("Times New Roman", 12, 'bold'))
            self.m1_p6_snsrL.grid(column=1, row=9)
            self.m1_p10_snsr = StringVar()
            self.m1_p10_snsrL = Label(self.master, textvariable=self.m1_p10_snsr,
                                      width=8, height=2, fg='blue', font=("Times New Roman", 12, 'bold'))
            self.m1_p10_snsrL.grid(column=2, row=9)

            self.m1_2p_goal = Text(
                self.master, width=12, height=2, font=('Times New Roman', 11, "bold")
            )
            self.m1_2p_goal.grid(column=0, row=10)
            self.m1_6p_goal = Text(
                self.master, width=12, height=2, font=('Times New Roman', 11, "bold")
            )
            self.m1_6p_goal.grid(column=1, row=10)
            self.m1_10p_goal = Text(
                self.master, width=12, height=2, font=('Times New Roman', 11, "bold")
            )
            self.m1_10p_goal.grid(column=2, row=10)
            self.m1_2p_goalSendB = Button(
                self.master, text='send', command=self.m1_2p_sendBClicked,
                width=8, height=2, fg='blue', font=('Times New Roman', 12, 'bold')
            )
            self.m1_2p_goalSendB.grid(column=0, row=11)
            self.m1_6p_goalSendB = Button(
                self.master, text='stop', command=self.m1_6p_sendBClicked,
                width=8, height=2, fg='blue', font=('Times New Roman', 12, 'bold')
            )
            self.m1_6p_goalSendB.grid(column=1, row=11)
            self.m1_10p_goalSendB = Button(
                self.master, text='send', command=self.m1_10p_sendBClicked,
                width=8, height=2, fg='blue', font=('Times New Roman', 12, 'bold')
            )
            self.m1_10p_goalSendB.grid(column=2, row=11)
            self.m1_2p_stopB = Button(
                self.master, text='stop', command=self.m1_2p_stopBClicked, fg='red',
                width=8, height=2, font=('Times New Roman', 11, 'bold')
            )
            self.m1_2p_stopB.grid(column=0, row=12)
            self.m1_6p_stopB = Button(
                self.master, text='send', command=self.m1_6p_stopBClicked, fg='red',
                width=8, height=2, font=('Times New Roman', 11, 'bold')
            )
            self.m1_6p_stopB.grid(column=1, row=12)
            self.m1_10p_stopB = Button(
                self.master, text='stop', command=self.m1_10p_stopBClicked, fg='red',
                width=8, height=2, font=('Times New Roman', 11, 'bold')
            )
            self.m1_10p_stopB.grid(column=2, row=12)

            self.m1_r = StringVar()
            self.m1_rL = Label(self.master, textvariable=self.m1_r,
                               width=8, height=2, fg='red', font=("Times New Roman", 12, 'bold'))
            self.m1_rL.grid(column=0, row=13)
            self.m1_p = StringVar()
            self.m1_pL = Label(self.master, textvariable=self.m1_p,
                               width=8, height=2, fg='red', font=("Times New Roman", 12, 'bold'))
            self.m1_pL.grid(column=1, row=13)
            self.m1_y = StringVar()
            self.m1_yL = Label(self.master, textvariable=self.m1_y,
                               width=8, height=2, fg='red', font=("Times New Roman", 12, 'bold'))
            self.m1_yL.grid(column=2, row=13)

            # Module2 Sol. Valve Group 2
            self.m2_2p1B = Button(
                self.master, text="+1", command=self.m2_2p1Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_2p1B.grid(column=3, row=1)
            self.m2_2m1B = Button(
                self.master, text="-1", command=self.m2_2m1Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_2m1B.grid(column=3, row=2)
            self.m2_2p10B = Button(
                self.master, text="+10", command=self.m2_2p10Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_2p10B.grid(column=3, row=3)
            self.m2_2m10B = Button(
                self.master, text="-10", command=self.m2_2m10Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_2m10B.grid(column=3, row=4)
            self.m2_2p100B = Button(
                self.master, text="+100", command=self.m2_2p100Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_2p100B.grid(column=3, row=5)
            self.m2_2p1000B = Button(
                self.master, text="+1000", command=self.m2_2p1000Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_2p1000B.grid(column=3, row=6)

            # Module2 Sol. Valve Group 6
            self.m2_6p1B = Button(
                self.master, text="+1", command=self.m2_6p1Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_6p1B.grid(column=4, row=1)
            self.m2_6m1B = Button(
                self.master, text="-1", command=self.m2_6m1Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_6m1B.grid(column=4, row=2)
            self.m2_6p10B = Button(
                self.master, text="+10", command=self.m2_6p10Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_6p10B.grid(column=4, row=3)
            self.m2_6m10B = Button(
                self.master, text="-10", command=self.m2_6m10Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_6m10B.grid(column=4, row=4)
            self.m2_6p100B = Button(
                self.master, text="+100", command=self.m2_6p100Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_6p100B.grid(column=4, row=5)
            self.m2_6p1000B = Button(
                self.master, text="+1000", command=self.m2_6p1000Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_6p1000B.grid(column=4, row=6)

            # Module2 Sol. Valve Group 10
            self.m2_10p1B = Button(
                self.master, text="+1", command=self.m2_10p1Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_10p1B.grid(column=5, row=1)
            self.m2_10m1B = Button(
                self.master, text="-1", command=self.m2_10m1Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_10m1B.grid(column=5, row=2)
            self.m2_10p10B = Button(
                self.master, text="+10", command=self.m2_10p10Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_10p10B.grid(column=5, row=3)
            self.m2_10m10B = Button(
                self.master, text="-10", command=self.m2_10m10Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_10m10B.grid(column=5, row=4)
            self.m2_10p100B = Button(
                self.master, text="+100", command=self.m2_10p100Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_10p100B.grid(column=5, row=5)
            self.m2_10p1000B = Button(
                self.master, text="+1000", command=self.m2_10p1000Clicked, width=6, height=2,
                font=("Times New Roman", 12, "bold")
            )
            self.m2_10p1000B.grid(column=5, row=6)

            # Variable to display applied voltage of M2
            self.m2_2pV = StringVar()
            self.m2_2mV = StringVar()
            self.m2_6pV = StringVar()
            self.m2_6mV = StringVar()
            self.m2_10pV = StringVar()
            self.m2_10mV = StringVar()
            self.m2_2pVL = Label(self.master, textvariable=self.m2_2pV,
                                 width=6, height=2, fg='blue', font=("Times New Roman", 12, "bold"))
            self.m2_2pVL.grid(column=3, row=7)
            self.m2_2mVL = Label(self.master, textvariable=self.m2_2mV,
                                 width=6, height=2, fg='red', font=("Times New Roman", 12, "bold"))
            self.m2_2mVL.grid(column=3, row=8)
            self.m2_6pVL = Label(self.master, textvariable=self.m2_6pV,
                                 width=6, height=2, fg='blue', font=("Times New Roman", 12, "bold"))
            self.m2_6pVL.grid(column=4, row=7)
            self.m2_6mVL = Label(self.master, textvariable=self.m2_6mV,
                                 width=6, height=2, fg='red', font=("Times New Roman", 12, "bold"))
            self.m2_6mVL.grid(column=4, row=8)
            self.m2_10pVL = Label(self.master, textvariable=self.m2_10pV,
                                  width=6, height=2, fg='blue', font=("Times New Roman", 12, "bold"))
            self.m2_10pVL.grid(column=5, row=7)
            self.m2_10mVL = Label(self.master, textvariable=self.m2_10mV,
                                  width=6, height=2, fg='red', font=("Times New Roman", 12, "bold"))
            self.m2_10mVL.grid(column=5, row=8)

            self.m2_p2_snsr = StringVar()
            self.m2_p2_snsrL = Label(self.master, textvariable=self.m2_p2_snsr,
                                     width=8, height=2, fg='blue', font=("Times New Roman", 12, 'bold'))
            self.m2_p2_snsrL.grid(column=3, row=9)
            self.m2_p6_snsr = StringVar()
            self.m2_p6_snsrL = Label(self.master, textvariable=self.m2_p6_snsr,
                                     width=8, height=2, fg='blue', font=("Times New Roman", 12, 'bold'))
            self.m2_p6_snsrL.grid(column=4, row=9)
            self.m2_p10_snsr = StringVar()
            self.m2_p10_snsrL = Label(self.master, textvariable=self.m2_p10_snsr,
                                      width=8, height=2, fg='blue', font=("Times New Roman", 12, 'bold'))
            self.m2_p10_snsrL.grid(column=5, row=9)

            self.m2_2p_goal = Text(
                self.master, width=12, height=2, font=('Times New Roman', 11, "bold")
            )
            self.m2_2p_goal.grid(column=3, row=10)
            self.m2_6p_goal = Text(
                self.master, width=12, height=2, font=('Times New Roman', 11, "bold")
            )
            self.m2_6p_goal.grid(column=4, row=10)
            self.m2_10p_goal = Text(
                self.master, width=12, height=2, font=('Times New Roman', 11, "bold")
            )
            self.m2_10p_goal.grid(column=5, row=10)
            self.m2_2p_goalSendB = Button(
                self.master, text='send', command=self.m2_2p_sendBClicked,
                width=8, height=2, fg='blue', font=('Times New Roman', 12, 'bold')
            )
            self.m2_2p_goalSendB.grid(column=3, row=11)
            self.m2_6p_goalSendB = Button(
                self.master, text='stop', command=self.m2_6p_sendBClicked,
                width=8, height=2, fg='blue', font=('Times New Roman', 12, 'bold')
            )
            self.m2_6p_goalSendB.grid(column=4, row=11)
            self.m2_10p_goalSendB = Button(
                self.master, text='send', command=self.m2_10p_sendBClicked,
                width=8, height=2, fg='blue', font=('Times New Roman', 12, 'bold')
            )
            self.m2_10p_goalSendB.grid(column=5, row=11)
            self.m2_2p_stopB = Button(
                self.master, text='stop', command=self.m2_2p_stopBClicked, fg='red',
                width=8, height=2, font=('Times New Roman', 12, 'bold')
            )
            self.m2_2p_stopB.grid(column=3, row=12)
            self.m2_6p_stopB = Button(
                self.master, text='send', command=self.m2_6p_stopBClicked, fg='red',
                width=8, height=2, font=('Times New Roman', 12, 'bold')
            )
            self.m2_6p_stopB.grid(column=4, row=12)
            self.m2_10p_stopB = Button(
                self.master, text='stop', command=self.m2_10p_stopBClicked, fg='red',
                width=8, height=2, font=('Times New Roman', 12, 'bold')
            )
            self.m2_10p_stopB.grid(column=5, row=12)

            self.m2_r = StringVar()
            self.m2_rL = Label(self.master, textvariable=self.m2_r,
                               width=8, height=2, fg='red', font=("Times New Roman", 12, 'bold'))
            self.m2_rL.grid(column=3, row=13)
            self.m2_p = StringVar()
            self.m2_pL = Label(self.master, textvariable=self.m2_p,
                               width=8, height=2, fg='red', font=("Times New Roman", 12, 'bold'))
            self.m2_pL.grid(column=4, row=13)
            self.m2_y = StringVar()
            self.m2_yL = Label(self.master, textvariable=self.m2_y,
                               width=8, height=2, fg='red', font=("Times New Roman", 12, 'bold'))
            self.m2_yL.grid(column=5, row=13)

            self.fig = plt.figure()
            self.ax  = self.fig.add_subplot(111, projection='3d')
            self.ax.set_title('Module Pose')
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')
            line6  = self.ax.plot([0, 0], [48.735, 48.735], [0, 171.5], c='black')[0]
            line10 = self.ax.plot([-42.206, -42.206], [-24.368, -24.368], [0, 171.5], c='black')[0]
            line2  = self.ax.plot([42.206, 42.206], [-24.368, -24.368], [0, 171.5], c='black')[0]
            self.lines = [line6, line10, line2]
            # self.lines = [self.ax.plot([], [], [])[0] for _ in range(3)]
            # self.lines[0].set_data_3d([0,0], [48.735,48.735], [0,171.5])
            # self.lines = [line6, line10, line2]

            # Creating fifty line objects.
            # NOTE: Can't pass empty arrays into 3d version of plot()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
            self.canvas.get_tk_widget().grid(column=6, row=0, rowspan=12)

            self.line_ani = animation.FuncAnimation(self.fig, self.update_module_pose, 33, fargs=[self.lines],
                                                    interval=50, blit=False)

            # self.quitB = Button(self.master, text='Quit', command=self.quitB, width=10, height=3, fg='red', font=("Arial", 15))
            # self.quitB.grid(column=2, row=0)
            self.bgTask = BackgroundTask(self.myLongProcess)

            # server_IP = "192.168.0.99"  # this computer
            server_IP = "192.168.0.3"
            server_PORT = 8080  # the port that the wemos should connect to

            # self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # UDP
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try :
                self.server_sock.bind((server_IP, server_PORT))
                self.client_sock = self.server_sock
            except :
                pass
            # self.server_sock.listen(3) # TCP
            # self.client_sock, addr = self.server_sock.accept() # TCP

        def update_module_pose(self, _, lines):
            line6  = lines[0]
            line10 = lines[1]
            line2  = lines[2]
            # print(self._r_, self._p_, self._y_)
            if 135 < self._r_ < 150 :
                line6.set_color('red')
            elif 90 < self._r_ < 135 :
                line6.set_color('blue')
            else :
                line6.set_color('black')
            if 140 < self._p_ < 150 :
                line10.set_color('green')
            elif 110 < self._p_ < 140 :
                line10.set_color('violet')
            else :
                line10.set_color('black')
            line6.set_data_3d(line6.get_data_3d()[0], line6.get_data_3d()[1], [0, self._r_])

            line10.set_data_3d(line10.get_data_3d()[0], line10.get_data_3d()[1], [0, self._p_])
            line2.set_data_3d(line2.get_data_3d()[0], line2.get_data_3d()[1], [0, self._y_])
            return lines

        def close(self) :
            print("close")
            try:
                self.bgTask.stop()
            except:
                pass
            self.master.quit()

        def mod_comm_startClicked(self):
            print ("Sensor Read Start")
            try:
                self.bgTask.start()
            except:
                pass

        def mod_comm_stopClicked(self) :
            print ("Sensor Read Stop")
            try:
                self.bgTask.stop()
            except:
                pass

        def myLongProcess(self, isRunningFunc=None) :
            print("starting myLongProcess")
            # WORKING THREAD
            while True :
                try:
                    if not isRunningFunc() :
                        self.onMyLongProcessUpdate("Stopped!")
                        return
                except :
                    pass
                data, addr = self.client_sock.recvfrom(1024)  # buffer size is 1024 bytes
                # data, addr = self.server_sock.recvfrom(1024)
                data = data.decode('utf-8').rstrip()
                # print(data)
                if len(data):
                    self.onMyLongProcessUpdate(data)
                else :
                    self.onMyLongProcessUpdate("N/A")
                # update rate : every 30 ms
                sleep(0.03) # simulate doing work
            # self.onMyLongProcessUpdate("Done!")

        def onMyLongProcessUpdate(self, snsrVal) :
            # print("Process Update: %s" %(snsrVal,))
            # print(snsrVal.rstrip())
            if not AT_HOME :
                _temp = last_received.decode('utf-8').rstrip().split(",")
                _val = snsrVal.split(",")
            else :
                _temp = [0.0, 0.0, 0.0, 0.0]
                _val = snsrVal.split(",")
            if self.start == 0 :
                self.r_init = float(_temp[1])
                self.p_init = float(_temp[2])
                self.y_init = float(_temp[3])
                self.start  = 1
            _r = float(_temp[1])
            _p = float(_temp[2])
            _y = float(_temp[3])
            _r_ = round(_r - self.r_init, 3)
            _p_ = round(_p - self.p_init, 3)
            _y_ = round(_y - self.y_init, 3)
            self._r_ = float(_val[3])
            self._p_ = float(_val[4])
            self._y_ = float(_val[5])
            # _val  =_temp[1].decode('utf-8').rstrip().split(",")
            if len(_val) == 9 :
                self.p1_snsr.set(str(_val[0]))
                self.p2_snsr.set(str(_val[1]))
                self.p3_snsr.set(str(_val[2]))
                # self.r.set(str(_val[3]))
                # self.p.set(str(_val[4]))
                # self.y.set(str(_val[5]))
                self.r.set(str(_r_))
                self.p.set(str(_p_))
                self.y.set(str(_y_))
                self.SV2_V.set(str(_val[6]))
                self.SV6_V.set(str(_val[7]))
                self.SV10_V.set(str(_val[8]))
                # print(_val[1], ",", _p_)
            else :
                pass
        '''
            Solenoid Valve Control Callback (command)
        '''
        def m1_2p1Clicked(self) :
            self.client_sock.sendto("2p0001".encode(), (self.m1_IP, 8080))
        def m1_2p10Clicked(self) :
            self.client_sock.sendto("2p0010".encode(), (self.m1_IP, 8080))
        def m1_2p100Clicked(self) :
            self.client_sock.sendto("2p0100".encode(), (self.m1_IP, 8080))
        def m1_2p1000Clicked(self) :
            self.client_sock.sendto("2p1000".encode(), (self.m1_IP, 8080))
        def m1_2m1Clicked(self) :
            self.client_sock.sendto("2m0001".encode(), (self.m1_IP, 8080))
        def m1_2m10Clicked(self) :
            self.client_sock.sendto("2m0010".encode(), (self.m1_IP, 8080))

        def m1_6p1Clicked(self) :
            self.client_sock.sendto("6p0001".encode(), (self.m1_IP, 8080))
        def m1_6p10Clicked(self) :
            self.client_sock.sendto("6p0010".encode(), (self.m1_IP, 8080))
        def m1_6p100Clicked(self) :
            self.client_sock.sendto("6p0100".encode(), (self.m1_IP, 8080))
        def m1_6p1000Clicked(self) :
            self.client_sock.sendto("6p1000".encode(), (self.m1_IP, 8080))
        def m1_6m1Clicked(self) :
            self.client_sock.sendto("6m0001".encode(), (self.m1_IP, 8080))
        def m1_6m10Clicked(self) :
            self.client_sock.sendto("6m0010".encode(), (self.m1_IP, 8080))

        def m1_10p1Clicked(self) :
            self.client_sock.sendto("10p0001".encode(), (self.m1_IP, 8080))
        def m1_10p10Clicked(self) :
            self.client_sock.sendto("10p0010".encode(), (self.m1_IP, 8080))
        def m1_10p100Clicked(self) :
            self.client_sock.sendto("10p0100".encode(), (self.m1_IP, 8080))
        def m1_10p1000Clicked(self) :
            self.client_sock.sendto("10p1000".encode(), (self.m1_IP, 8080))
        def m1_10m1Clicked(self) :
            self.client_sock.sendto("10m0001".encode(), (self.m1_IP, 8080))
        def m1_10m10Clicked(self) :
            self.client_sock.sendto("10m0010".encode(), (self.m1_IP, 8080))

        def m2_2p1Clicked(self) :
            self.client_sock.sendto("2p0001".encode(), (self.m2_IP, 8080))
        def m2_2p10Clicked(self) :
            self.client_sock.sendto("2p0010".encode(), (self.m2_IP, 8080))
        def m2_2p100Clicked(self) :
            self.client_sock.sendto("2p0100".encode(), (self.m2_IP, 8080))
        def m2_2p1000Clicked(self) :
            self.client_sock.sendto("2p1000".encode(), (self.m2_IP, 8080))
        def m2_2m1Clicked(self) :
            self.client_sock.sendto("2m0001".encode(), (self.m2_IP, 8080))
        def m2_2m10Clicked(self) :
            self.client_sock.sendto("2m0010".encode(), (self.m2_IP, 8080))

        def m2_6p1Clicked(self) :
            self.client_sock.sendto("6p0001".encode(), (self.m2_IP, 8080))
        def m2_6p10Clicked(self) :
            self.client_sock.sendto("6p0010".encode(), (self.m2_IP, 8080))
        def m2_6p100Clicked(self) :
            self.client_sock.sendto("6p0100".encode(), (self.m2_IP, 8080))
        def m2_6p1000Clicked(self) :
            self.client_sock.sendto("6p1000".encode(), (self.m2_IP, 8080))
        def m2_6m1Clicked(self) :
            self.client_sock.sendto("6m0001".encode(), (self.m2_IP, 8080))
        def m2_6m10Clicked(self) :
            self.client_sock.sendto("6m0010".encode(), (self.m2_IP, 8080))

        def m2_10p1Clicked(self) :
            self.client_sock.sendto("10p0001".encode(), (self.m2_IP, 8080))
        def m2_10p10Clicked(self) :
            self.client_sock.sendto("10p0010".encode(), (self.m2_IP, 8080))
        def m2_10p100Clicked(self) :
            self.client_sock.sendto("10p0100".encode(), (self.m2_IP, 8080))
        def m2_10p1000Clicked(self) :
            self.client_sock.sendto("10p1000".encode(), (self.m2_IP, 8080))
        def m2_10m1Clicked(self) :
            self.client_sock.sendto("10m0001".encode(), (self.m2_IP, 8080))
        def m2_10m10Clicked(self) :
            self.client_sock.sendto("10m0010".encode(), (self.m2_IP, 8080))

        # PID Button for m1
        def m1_2p_sendBClicked(self) :
            res = self.m1_2p_goal.get(1.0, END+"-1c")
            _msg = "2pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.m1_IP, 8080))
            print(_msg)
        def m1_6p_sendBClicked(self) :
            res = self.m1_6p_goal.get(1.0, END+"-1c")
            _msg = "6pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.m1_IP, 8080))
            print(_msg)
        def m1_10p_sendBClicked(self) :
            res = self.m1_10p_goal.get(1.0, END+"-1c")
            _msg = "1pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.m1_IP, 8080))
            print(_msg)
        def m1_2p_stopBClicked(self):
            _msg = "p2stop"
            self.client_sock.sendto(_msg.encode(), (self.m1_IP, 8080))
        def m1_6p_stopBClicked(self):
            _msg = "p6stop"
            self.client_sock.sendto(_msg.encode(), (self.m1_IP, 8080))
        def m1_10p_stopBClicked(self):
            _msg = "p10stop"
            self.client_sock.sendto(_msg.encode(), (self.m1_IP, 8080))

        # PID Button for m2
        def m2_2p_sendBClicked(self) :
            res = self.m2_2p_goal.get(1.0, END+"-1c")
            _msg = "2pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.m2_IP, 8080))
            print(_msg)
        def m2_6p_sendBClicked(self) :
            res = self.m2_6p_goal.get(1.0, END+"-1c")
            _msg = "6pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.m2_IP, 8080))
            print(_msg)
        def m2_10p_sendBClicked(self) :
            res = self.m2_10p_goal.get(1.0, END+"-1c")
            _msg = "1pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.m2_IP, 8080))
            print(_msg)
        def m2_2p_stopBClicked(self):
            _msg = "p2stop"
            self.client_sock.sendto(_msg.encode(), (self.m2_IP, 8080))
        def m2_6p_stopBClicked(self):
            _msg = "p6stop"
            self.client_sock.sendto(_msg.encode(), (self.m2_IP, 8080))
        def m2_10p_stopBClicked(self):
            _msg = "p10stop"
            self.client_sock.sendto(_msg.encode(), (self.m2_IP, 8080))

    root = Tk()
    for row_num in range(13) :
        root.rowconfigure(row_num, weight=1)
    for col_num in range(8) :
        root.columnconfigure(col_num, weight=1)
    gui = UnitTestGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()


if __name__ == "__main__":
    ControlPanel()