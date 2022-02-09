from tkinter import *
import socket, serial, threading, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np

AT_HOME = False

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
            self.X = list()
            self.Y = list()
            if AT_HOME :
                self._r_ = 171.5
                self._p_ = 171.5
                self._y_ = 171.5
            else :
                self._r_ = 0
                self._p_ = 0
                self._y_ = 0

            if AT_HOME :
                self.wemos_IP = "192.168.0.12"
            else :
                self.wemos_IP = "192.168.0.130"


            self.canvas = Canvas(master, width=100)
            self.threadedButton = Button(
                self.master, text="Comm. Start", command=self.onThreadedClicked,
                width=10, height=3, bg='black', fg='blue', font=("Arial", 15), highlightbackground='black')
            self.threadedButton.grid(column=0, row=0)

            self.cancelButton = Button(
                self.master, text="Stop", command=self.onStopClicked, width=10, height=3, bg='yellow', font=("Arial", 15))
            self.cancelButton.grid(column=1, row=0)

            '''
                Solenoid Valve Control Button
                2 6 10 / +0.001 +0.01 -0.001 -0.001 
            '''
            self.PAD_1 = Label(
                self.master, text="PID Control", width=10, height=2, bg='black', fg='white')
            self.PAD_1.grid(column=0, row=1)
            self.PAD_2 = Label(
                self.master, text="Target Pressure", width=10, height=2)
            self.PAD_2.grid(column=1, row=1)
            self.PAD_3 = Label(
                self.master, text="Send", width=10, height=2)
            self.PAD_3.grid(column=2, row=1)

            self.SV2_p1 = Button(
                self.master, text="SV2 +1", command=self.SV2_p001, width=8, height=2)
            self.SV2_p1.grid(column=3, row=0)
            self.SV2_p10 = Button(
                self.master, text="SV2 +10", command=self.SV2_p010, width=8, height=2)
            self.SV2_p10.grid(column=3, row=1)
            self.SV2_m1 = Button(
                self.master, text="SV2 -1", command=self.SV2_m001, width=8, height=2)
            self.SV2_m1.grid(column=3, row=2)
            self.SV2_m10 = Button(
                self.master, text="SV2 -10", command=self.SV2_m010, width=8, height=2)
            self.SV2_m10.grid(column=3, row=3)
            self.SV2_ALL_OFF = Button(
                self.master, text="SV2 A- OFF", command=self.SV2_OFF, width=8, height=2, fg='red')
            self.SV2_ALL_OFF.grid(column=3, row=7)
            self.SV2_P1V = Button(
                self.master, text="SV2 +1000", command=self.SV2_p1000, width=8, height=2)
            self.SV2_P1V.grid(column=3, row=4)
            self.SV2_M1V = Button(
                self.master, text="SV2 VAC ON", command=self.SV2_m1000, width=8, height=2, fg='blue')
            self.SV2_M1V.grid(column=3, row=6)
            self.SV2_p100 = Button(
                self.master, text="SV2 +100", command=self.SV2_p0100, width=8, height=2)
            self.SV2_p100.grid(column=3, row=5)

            self.SV6_p1 = Button(
                self.master, text="SV6 +1", command=self.SV6_p001, width=8, height=2)
            self.SV6_p1.grid(column=4, row=0)
            self.SV6_p10 = Button(
                self.master, text="SV6 +10", command=self.SV6_p010, width=8, height=2)
            self.SV6_p10.grid(column=4, row=1)
            self.SV6_m1 = Button(
                self.master, text="SV6 -1", command=self.SV6_m001, width=8, height=2)
            self.SV6_m1.grid(column=4, row=2)
            self.SV6_m10 = Button(
                self.master, text="SV6 -10", command=self.SV6_m010, width=8, height=2)
            self.SV6_m10.grid(column=4, row=3)
            self.SV6_ALL_OFF = Button(
                self.master, text="SV6 A- OFF", command=self.SV6_OFF, width=8, height=2, fg='red')
            self.SV6_ALL_OFF.grid(column=4, row=7)
            self.SV6_M1V = Button(
                self.master, text="SV6 VAC ON", command=self.SV6_m1000, width=8, height=2, fg='blue')
            self.SV6_M1V.grid(column=4, row=6)
            self.SV6_P1V = Button(
                self.master, text="SV6 +1000", command=self.SV6_p1000, width=8, height=2)
            self.SV6_P1V.grid(column=4, row=4)
            self.SV6_p100 = Button(
                self.master, text="SV6 +100", command=self.SV6_p0100, width=8, height=2)
            self.SV6_p100.grid(column=4, row=5)

            self.p2_PID_Label = Label(
                self.master, text='p2', width=10, height=3, font=('Arial', 15)
            ).grid(column=0, row=2)
            self.p6_PID_Label = Label(
                self.master, text='p6', width=10, height=3, font=('Arial', 15)
            ).grid(column=1, row=2)
            self.p10_PID_Label = Label(
                self.master, text='p10', width=10, height=3, font=('Arial', 15)
            ).grid(column=2, row=2)

            self.p2_PID_Value = Text(
                self.master, width=12, height=2, font=('Arial', 15)
            )
            self.p2_PID_Value.grid(column=0, row=3)
            self.p6_PID_Value = Text(
                self.master, width=12, height=2, font=('Arial', 15)
            )
            self.p6_PID_Value.grid(column=1, row=3)
            self.p10_PID_Value = Text(
                self.master, width=12, height=2, font=('Arial', 15)
            )
            self.p10_PID_Value.grid(column=2, row=3)

            self.p2_PID_Send = Button(
                self.master, text='p2 send', command=self.onClicked_getP2, width=8, height=2, fg='blue', font=('Arial', 15)
            )
            self.p2_PID_Send.grid(column=0, row=4)
            self.p6_PID_Send = Button(
                self.master, text='p6 send', command=self.onClicked_getP6, width=8, height=2, fg='blue', font=('Arial', 15)
            )
            self.p6_PID_Send.grid(column=1, row=4)
            self.p10_PID_Send = Button(
                self.master, text='p10 send', command=self.onClicked_getP10,  width=8, height=2, fg='blue', font=('Arial', 15)
            )
            self.p10_PID_Send.grid(column=2, row=4)
            self.p2_PID_Stop = Button(
                self.master, text='p2 stop', command=self.onClicked_P2_Stop, fg='red', width=8, height=2, font=('Arial', 15)
            )
            self.p2_PID_Stop.grid(column=0, row=5)
            self.p6_PID_Stop = Button(
                self.master, text='p6 stop', command=self.onClicked_P6_Stop, fg='red', width=8, height=2, font=('Arial', 15)
            )
            self.p6_PID_Stop.grid(column=1, row=5)
            self.p10_PID_Stop = Button(
                self.master, text='p10 stop', command=self.onClicked_P10_Stop, fg='red', width=8, height=2, font=('Arial', 15)
            )
            self.p10_PID_Stop.grid(column=2, row=5)

            self.SV10_p1 = Button(
                self.master, text="SV10 +1", command=self.SV10_p001, width=8, height=2)
            self.SV10_p1.grid(column=5, row=0)
            self.SV10_p10 = Button(
                self.master, text="SV10 +10", command=self.SV10_p010, width=8, height=2)
            self.SV10_p10.grid(column=5, row=1)
            self.SV10_m1 = Button(
                self.master, text="SV10 -1", command=self.SV10_m001, width=8, height=2)
            self.SV10_m1.grid(column=5, row=2)
            self.SV10_m10 = Button(
                self.master, text="SV10 -10", command=self.SV10_m010, width=8, height=2)
            self.SV10_m10.grid(column=5, row=3)
            self.SV10_ALL_OFF = Button(
                self.master, text="SV10 A- OFF", command=self.SV10_OFF, width=8, height=2, fg='red')
            self.SV10_ALL_OFF.grid(column=5, row=7)
            self.SV10_M1V = Button(
                self.master, text="SV10 VAC ON", command=self.SV10_m1000, width=8, height=2, fg='blue')
            self.SV10_M1V.grid(column=5, row=6)
            self.SV10_P1V = Button(
                self.master, text="SV10 +1000", command=self.SV10_p1000, width=8, height=2)
            self.SV10_P1V.grid(column=5, row=4)
            self.SV10_p100 = Button(
                self.master, text="SV10 +100", command=self.SV10_p0100, width=8, height=2)
            self.SV10_p100.grid(column=5, row=5)

            self.p2_Title = Label(self.master, text="p2", width=12, height=2, relief='solid')
            self.p2_Title.grid(column=0, row=8)
            self.p6_Title = Label(self.master, text="p6", width=12, height=2, relief='solid')
            self.p6_Title.grid(column=1, row=8)
            self.p10_Title = Label(self.master, text="p10", width=12, height=2, relief='solid')
            self.p10_Title.grid(column=2, row=8)

            self.p2_snsr = StringVar()
            self.p2_snsrVal = Label(self.master, textvariable=self.p2_snsr, width=12, height=2, fg='blue', font=("Arial", 18))
            self.p2_snsrVal.grid(column=0, row=9)
            self.p6_snsr = StringVar()
            self.p6_snsrVal = Label(self.master, textvariable=self.p6_snsr, width=12, height=2, fg='blue', font=("Arial", 18))
            self.p6_snsrVal.grid(column=1, row=9)
            self.p10_snsr = StringVar()
            self.p10_snsrVal = Label(self.master, textvariable=self.p10_snsr, width=12, height=2, fg='blue', font=("Arial", 18))
            self.p10_snsrVal.grid(column=2, row=9)

            self.r_Title = Label(self.master, text="r", width=12, height=2, relief='solid')
            self.r_Title.grid(column=0, row=10)
            self.p_Title = Label(self.master, text="p", width=12, height=2, relief='solid')
            self.p_Title.grid(column=1, row=10)
            self.y_Title = Label(self.master, text="y", width=12, height=2, relief='solid')
            self.y_Title.grid(column=2, row=10)
            self.r = StringVar()
            self.rVal = Label(self.master, textvariable=self.r, width=12, height=2, fg='red', font=("Arial", 18))
            self.rVal.grid(column=0, row=11)
            self.p = StringVar()
            self.pVal = Label(self.master, textvariable=self.p, width=12, height=2, fg='red', font=("Arial", 18))
            self.pVal.grid(column=1, row=11)
            self.y = StringVar()
            self.yVal = Label(self.master, textvariable=self.y, width=12, height=2, fg='red', font=("Arial", 18))
            self.yVal.grid(column=2, row=11)

            self.SV2_V_Title = Label(self.master, text="SV2_P_V", width=11, height=2, relief='solid')
            self.SV2_V_Title.grid(column=3, row=8)
            self.SV6_V_Title = Label(self.master, text="SV6_P_V", width=11, height=2, relief='solid')
            self.SV6_V_Title.grid(column=4, row=8)
            self.SV10_V_Title = Label(self.master, text="SV10_P_V", width=11, height=2, relief='solid')
            self.SV10_V_Title.grid(column=5, row=8)

            self.SV2_V = StringVar()
            self.SV6_V = StringVar()
            self.SV10_V = StringVar()

            self.SV2_V_Label = Label(self.master, textvariable=self.SV2_V, width=12, height=2, fg='blue', font=("Arial", 18))
            self.SV2_V_Label.grid(column=3, row=9)
            self.SV6_V_Label = Label(self.master, textvariable=self.SV6_V, width=12, height=2, fg='blue', font=("Arial", 18))
            self.SV6_V_Label.grid(column=4, row=9)
            self.SV10_V_Label = Label(self.master, textvariable=self.SV10_V, width=12, height=2, fg='blue', font=("Arial", 18))
            self.SV10_V_Label.grid(column=5, row=9)

            self.fig = plt.figure()
            # self.ax  = self.fig.add_subplot(111, projection='3d')
            # self.ax.set_title('Module Pose')
            self.ax  = self.fig.add_subplot(111)
            self.ax.set_title('Bending angle')
            self.ax.set_xlim([-1, 30])
            self.ax.set_ylim([-50, 50])


            # line6  = self.ax.plot([0, 0], [48.735, 48.735], [0, 171.5], c='black')[0]
            # line10 = self.ax.plot([-42.206, -42.206], [-24.368, -24.368], [0, 171.5], c='black')[0]
            # line2  = self.ax.plot([42.206, 42.206], [-24.368, -24.368], [0, 171.5], c='black')[0]
            # self.lines = [line6, line10, line2]

            # Draw IMU angle
            # self.lines = [self.ax.scatter([0, 1], [0, 1], c='black', linestyle='--')]
            self.lines = [self.ax.plot([], [], c='black', linestyle='--')[0]]

            # Creating fifty line objects.
            # NOTE: Can't pass empty arrays into 3d version of plot()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
            self.canvas.get_tk_widget().grid(column=6, row=0, rowspan=12)

            # self.line_ani = animation.FuncAnimation(self.fig, self.update_module_pose, 33, fargs=[self.lines],
            #                                         interval=50, blit=False)
            self.line_ani2 = animation.FuncAnimation(self.fig, self.update_module_pose2, 30, fargs=[self.lines],
                                                    interval=30, blit=False)


            self.quitB = Button(self.master, text='Quit', command=self.quitB, width=10, height=3, fg='red', font=("Arial", 15))
            self.quitB.grid(column=2, row=0)
            self.bgTask = BackgroundTask(self.myLongProcess)

            if not AT_HOME :
                server_IP = "192.168.0.99"  # this computer
            else :
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

        def update_module_pose2(self, _, lines):
            line = lines[0]
            self.X.append(_)
            self.Y.append(float(self._p_))
            line.set_data(self.X, self.Y)
            if len(self.X) > 30 :
                self.X = list()
                self.Y = list()

            # line10.set_data_3d(line10.get_data_3d()[0], line10.get_data_3d()[1], [0, self._p_])
            # line2.set_data_3d(line2.get_data_3d()[0], line2.get_data_3d()[1], [0, self._y_])
            return lines

        def close(self) :
            print("close")
            try:
                self.bgTask.stop()
            except:
                pass
            self.master.quit()

        def onThreadedClicked(self):
            print ("Sensor Read Start")
            try:
                self.bgTask.start()
            except:
                pass

        def onStopClicked(self) :
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
                sleep(0.001) # simulate doing work
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
            self._p_ = _p_
            self._y_ = float(_val[5])

            # _val  =_temp[1].decode('utf-8').rstrip().split(",")
            if len(_val) == 9 :
                self.p2_snsr.set(str(_val[0]))
                self.p6_snsr.set(str(_val[1]))
                self.p10_snsr.set(str(_val[2]))
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
        def SV2_p001(self) :
            self.client_sock.sendto("2p01".encode(), (self.wemos_IP, 8080))
        def SV2_p010(self) :
            self.client_sock.sendto("2p10".encode(), (self.wemos_IP, 8080))
        def SV2_m001(self) :
            self.client_sock.sendto("2m01".encode(), (self.wemos_IP, 8080))
        def SV2_m010(self) :
            self.client_sock.sendto("2m10".encode(), (self.wemos_IP, 8080))
        def SV6_p001(self) :
            self.client_sock.sendto("6p01".encode(), (self.wemos_IP, 8080))
        def SV6_p010(self) :
            self.client_sock.sendto("6p10".encode(), (self.wemos_IP, 8080))
        def SV6_m001(self) :
            self.client_sock.sendto("6m01".encode(), (self.wemos_IP, 8080))
        def SV6_m010(self) :
            self.client_sock.sendto("6m10".encode(), (self.wemos_IP, 8080))
        def SV10_p001(self) :
            self.client_sock.sendto("10p01".encode(), (self.wemos_IP, 8080))
        def SV10_p010(self) :
            self.client_sock.sendto("10p10".encode(), (self.wemos_IP, 8080))
        def SV10_m001(self) :
            self.client_sock.sendto("10m01".encode(), (self.wemos_IP, 8080))
        def SV10_m010(self) :
            self.client_sock.sendto("10m10".encode(), (self.wemos_IP, 8080))
        def SV2_OFF(self) :
            self.client_sock.sendto("2a0".encode(), (self.wemos_IP, 8080))
        def SV2_p1000(self) :
            self.client_sock.sendto("2p1000".encode(), (self.wemos_IP, 8080))
        def SV2_m1000(self) :
            self.client_sock.sendto("2m1000".encode(), (self.wemos_IP, 8080))
        def SV2_p0100(self) :
            self.client_sock.sendto("2p100".encode(), (self.wemos_IP, 8080))
        def SV6_OFF(self) :
            self.client_sock.sendto("6a0".encode(), (self.wemos_IP, 8080))
        def SV6_p1000(self) :
            self.client_sock.sendto("6p1000".encode(), (self.wemos_IP, 8080))
        def SV6_m1000(self) :
            self.client_sock.sendto("6m1000".encode(), (self.wemos_IP, 8080))
        def SV6_p0100(self) :
            self.client_sock.sendto("6p100".encode(), (self.wemos_IP, 8080))
        def SV10_OFF(self) :
            self.client_sock.sendto("10a0".encode(), (self.wemos_IP, 8080))
        def SV10_p1000(self) :
            self.client_sock.sendto("10p1000".encode(), (self.wemos_IP, 8080))
        def SV10_m1000(self) :
            self.client_sock.sendto("10m1000".encode(), (self.wemos_IP, 8080))
        def SV10_p0100(self) :
            self.client_sock.sendto("10p100".encode(), (self.wemos_IP, 8080))

        def onClicked_getP2(self) :
            res = self.p2_PID_Value.get(1.0, END+"-1c")
            _msg = "2pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.wemos_IP, 8080))
            print(_msg)
        def onClicked_getP6(self) :
            res = self.p6_PID_Value.get(1.0, END+"-1c")
            _msg = "6pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.wemos_IP, 8080))
            print(_msg)
        def onClicked_getP10(self) :
            res = self.p10_PID_Value.get(1.0, END+"-1c")
            _msg = "1pd" + str(res)
            self.client_sock.sendto(_msg.encode(), (self.wemos_IP, 8080))
            print(_msg)
        def onClicked_P2_Stop(self):
            _msg = "p2stop"
            self.client_sock.sendto(_msg.encode(), (self.wemos_IP, 8080))
        def onClicked_P6_Stop(self):
            _msg = "p6stop"
            self.client_sock.sendto(_msg.encode(), (self.wemos_IP, 8080))
        def onClicked_P10_Stop(self):
            _msg = "p10stop"
            self.client_sock.sendto(_msg.encode(), (self.wemos_IP, 8080))

        def quitB(self) :
            try :
                self.bgTask.stop()
                self.ser.close()
                self.master.destroy()
            except :
                pass
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