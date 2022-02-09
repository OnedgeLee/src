from tkinter import *
import socket, serial, threading, queue

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

def tkThreadingTest():
    from tkinter import Tk, Label, Button, StringVar
    from time import sleep

    class UnitTestGUI:

        def __init__(self, master):
            self.master = master
            master.title("Control Panel")

            self.wemos_IP = "192.168.0.125"

            self.label1 = Label(self.master, width=10, height=5, bg='black')
            self.label1.pack()
            self.SV1_Label = Label(self.master, width=10, height=3)
            self.SV1_Label.pack()
            self.SV2_Label = Label(self.master, width=10, height=3)
            self.SV2_Label.pack()
            self.SV3_Label = Label(self.master, width=10, height=3)
            self.SV3_Label.pack()
            self.SV4_Label = Label(self.master, width=10, height=3)
            self.SV4_Label.pack()
            self.SV5_Label = Label(self.master, width=10, height=3) # Solenoid Valve Off
            self.SV5_Label.pack()
            self.SV6_Label = Label(self.master, width=10, height=3) # Solenoid Valve + + 1V
            self.SV6_Label.pack()
            self.SV7_Label = Label(self.master, width=10, height=3) # Solenoid Valve - + 1V
            self.SV7_Label.pack()

            self.psnsr_Title = Label(self.master, width=12, height=2)
            self.psnsr_Title.pack()

            self.psnsr_Label = Label(self.master, width=12, height=2)
            self.psnsr_Label.pack()

            self.imu_Title = Label(self.master, width=12, height=2)
            self.imu_Title.pack()
            self.imu_Label = Label(self.master, width=12, height=2)
            self.imu_Label.pack()

            self.SV_V_Title = Label(self.master, width=12, height=2)
            self.SV_V_Title.pack()
            self.SV_V_Label = Label(self.master, width=12, height=2)
            self.SV_V_Label.pack()

            self.threadedButton = Button(
                self.label1, text="Comm. Start", command=self.onThreadedClicked, width=10, height=3, fg='blue', font=("Arial", 15))
            self.threadedButton.pack(side=LEFT)

            self.cancelButton = Button(
                self.label1, text="Stop", command=self.onStopClicked, width=10, height=3, font=("Arial", 15))
            self.cancelButton.pack(side=LEFT)

            '''
                Solenoid Valve Control Button
                2 6 10 / +0.001 +0.01 -0.001 -0.001 
            '''
            self.PAD_1 = Label(
                self.SV1_Label, text="PID Control", width=10, height=3)
            # self.PAD_1.grid(column=0, row=0)
            self.PAD_1.pack(side=LEFT)
            self.PAD_2 = Label(
                self.SV1_Label, text="Target Pressure", width=10, height=3)
            self.PAD_2.pack(side=LEFT)
            self.PAD_3 = Label(
                self.SV1_Label, text="Send", width=10, height=3)
            self.PAD_3.pack(side=LEFT)

            self.SV2_p1 = Button(
                self.SV1_Label, text="SV2 +1", command=self.SV2_p001, width=10, height=3)
            self.SV2_p1.pack(side=LEFT)

            self.SV2_p10 = Button(
                self.SV2_Label, text="SV2 +10", command=self.SV2_p010, width=10, height=3)
            self.SV2_p10.pack(side=LEFT)
            self.SV2_m1 = Button(
                self.SV3_Label, text="SV2 -1", command=self.SV2_m001, width=10, height=3)
            self.SV2_m1.pack(side=LEFT)
            self.SV2_m10 = Button(
                self.SV4_Label, text="SV2 -10", command=self.SV2_m010, width=10, height=3)
            self.SV2_m10.pack(side=LEFT)
            self.SV2_ALL_OFF = Button(
                self.SV5_Label, text="SV2 A- OFF", command=self.SV2_OFF, width=10, height=3, fg='red')
            self.SV2_ALL_OFF.pack(side=LEFT)
            self.SV2_P1V = Button(
                self.SV6_Label, text="SV2 +1000", command=self.SV2_p1000, width=10, height=3)
            self.SV2_P1V.pack(side=LEFT)
            self.SV2_M1V = Button(
                self.SV5_Label, text="SV2 VAC ON", command=self.SV2_m1000, width=10, height=3, fg='blue')
            self.SV2_M1V.pack(side=LEFT)
            self.SV2_p100 = Button(
                self.SV7_Label, text="SV2 +100", command=self.SV2_p0100, width=10, height=3)
            self.SV2_p100.pack(side=LEFT)

            self.SV6_p1 = Button(
                self.SV1_Label, text="SV6 +1", command=self.SV6_p001, width=10, height=3)
            self.SV6_p1.pack(side=LEFT)
            self.SV6_p10 = Button(
                self.SV2_Label, text="SV6 +10", command=self.SV6_p010, width=10, height=3)
            self.SV6_p10.pack(side=LEFT)
            self.SV6_m1 = Button(
                self.SV3_Label, text="SV6 -1", command=self.SV6_m001, width=10, height=3)
            self.SV6_m1.pack(side=LEFT)
            self.SV6_m10 = Button(
                self.SV4_Label, text="SV6 -10", command=self.SV6_m010, width=10, height=3)
            self.SV6_m10.pack(side=LEFT)
            self.SV6_ALL_OFF = Button(
                self.SV5_Label, text="SV6 A- OFF", command=self.SV6_OFF, width=10, height=3, fg='red')
            self.SV6_ALL_OFF.pack(side=LEFT)
            self.SV6_P1V = Button(
                self.SV6_Label, text="SV6 +1000", command=self.SV6_p1000, width=10, height=3)
            self.SV6_P1V.pack(side=LEFT)
            self.SV6_M1V = Button(
                self.SV5_Label, text="SV6 VAC ON", command=self.SV6_m1000, width=10, height=3, fg='blue')
            self.SV6_M1V.pack(side=LEFT)
            self.SV6_p100 = Button(
                self.SV7_Label, text="SV6 +100", command=self.SV6_p0100, width=10, height=3)
            self.SV6_p100.pack(side=LEFT)

            self.SV10_p1 = Button(
                self.SV1_Label, text="SV10 +1", command=self.SV10_p001, width=10, height=3)
            self.SV10_p1.pack(side=LEFT)
            self.SV10_p10 = Button(
                self.SV2_Label, text="SV10 +10", command=self.SV10_p010, width=10, height=3)
            self.SV10_p10.pack(side=LEFT)
            self.SV10_m1 = Button(
                self.SV3_Label, text="SV10 -1", command=self.SV10_m001, width=10, height=3)
            self.SV10_m1.pack(side=LEFT)
            self.SV10_m10 = Button(
                self.SV4_Label, text="SV10 -10", command=self.SV10_m010, width=10, height=3)
            self.SV10_m10.pack(side=LEFT)
            self.SV10_ALL_OFF = Button(
                self.SV5_Label, text="SV10 A- OFF", command=self.SV10_OFF, width=10, height=3, fg='red')
            self.SV10_ALL_OFF.pack(side=LEFT)
            self.SV10_P1V = Button(
                self.SV6_Label, text="SV10 +1000", command=self.SV10_p1000, width=10, height=3)
            self.SV10_P1V.pack(side=LEFT)
            self.SV10_M1V = Button(
                self.SV5_Label, text="SV10 VAC ON", command=self.SV10_m1000, width=10, height=3, fg='blue')
            self.SV10_M1V.pack(side=LEFT)
            self.SV10_p100 = Button(
                self.SV7_Label, text="SV10 +100", command=self.SV10_p0100, width=10, height=3)
            self.SV10_p100.pack(side=LEFT)

            self.p2_Title = Label(self.psnsr_Title, text="p2", width=12, height=2, relief='solid')
            self.p2_Title.pack(side=LEFT)
            self.p6_Title = Label(self.psnsr_Title, text="p6", width=12, height=2, relief='solid')
            self.p6_Title.pack(side=LEFT)
            self.p10_Title = Label(self.psnsr_Title, text="p10", width=12, height=2, relief='solid')
            self.p10_Title.pack(side=LEFT)

            self.p1_snsr = StringVar()
            self.p1_snsrVal = Label(self.psnsr_Label, textvariable=self.p1_snsr, width=12, height=2, fg='blue', font=("Arial", 18))
            self.p1_snsrVal.pack(side=LEFT)
            self.p2_snsr = StringVar()
            self.p2_snsrVal = Label(self.psnsr_Label, textvariable=self.p2_snsr, width=12, height=2, fg='blue', font=("Arial", 18))
            self.p2_snsrVal.pack(side=LEFT)
            self.p3_snsr = StringVar()
            self.p3_snsrVal = Label(self.psnsr_Label, textvariable=self.p3_snsr, width=12, height=2, fg='blue', font=("Arial", 18))
            self.p3_snsrVal.pack(side=LEFT)

            self.r_Title = Label(self.imu_Title, text="r", width=12, height=2, relief='solid')
            self.r_Title.pack(side=LEFT)
            self.p_Title = Label(self.imu_Title, text="p", width=12, height=2, relief='solid')
            self.p_Title.pack(side=LEFT)
            self.y_Title = Label(self.imu_Title, text="y", width=12, height=2, relief='solid')
            self.y_Title.pack(side=LEFT)
            self.r = StringVar()
            self.rVal = Label(self.imu_Label, textvariable=self.r, width=12, height=2, fg='red', font=("Arial", 18))
            self.rVal.pack(side=LEFT)
            self.p = StringVar()
            self.pVal = Label(self.imu_Label, textvariable=self.p, width=12, height=2, fg='red', font=("Arial", 18))
            self.pVal.pack(side=LEFT)
            self.y = StringVar()
            self.yVal = Label(self.imu_Label, textvariable=self.y, width=12, height=2, fg='red', font=("Arial", 18))
            self.yVal.pack(side=LEFT)

            self.SV2_V_Title = Label(self.SV_V_Title, text="SV2_P_V", width=12, height=2, relief='solid')
            self.SV2_V_Title.pack(side=LEFT)
            self.SV6_V_Title = Label(self.SV_V_Title, text="SV6_P_V", width=12, height=2, relief='solid')
            self.SV6_V_Title.pack(side=LEFT)
            self.SV10_V_Title = Label(self.SV_V_Title, text="SV10_P_V", width=12, height=2, relief='solid')
            self.SV10_V_Title.pack(side=LEFT)

            self.SV2_V = StringVar()
            self.SV6_V = StringVar()
            self.SV10_V = StringVar()

            self.SV2_V_Label = Label(self.SV_V_Label, textvariable=self.SV2_V, width=12, height=2, fg='blue', font=("Arial", 18))
            self.SV2_V_Label.pack(side=LEFT)
            self.SV6_V_Label = Label(self.SV_V_Label, textvariable=self.SV6_V, width=12, height=2, fg='blue', font=("Arial", 18))
            self.SV6_V_Label.pack(side=LEFT)
            self.SV10_V_Label = Label(self.SV_V_Label, textvariable=self.SV10_V, width=12, height=2, fg='blue', font=("Arial", 18))
            self.SV10_V_Label.pack(side=LEFT)


            self.quitB = Button(self.label1, text='Quit', command=self.quitB, width=10, height=3, fg='red', font=("Arial", 15))
            self.quitB.pack(side=LEFT)
            self.bgTask = BackgroundTask(self.myLongProcess)

            server_IP = "192.168.0.99"  # this computer
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
                if len(data):
                    self.onMyLongProcessUpdate(data)
                else :
                    self.onMyLongProcessUpdate("N/A")
                # update rate : every 50 ms
                sleep(0.03) # simulate doing work
            # self.onMyLongProcessUpdate("Done!")

        def onMyLongProcessUpdate(self, snsrVal) :
            # print("Process Update: %s" %(snsrVal,))
            # print(snsrVal.rstrip())
            _val = snsrVal.split(",")
            # _val  =_temp[1].decode('utf-8').rstrip().split(",")
            if len(_val) == 9 :
                self.p1_snsr.set(str(_val[0]))
                self.p2_snsr.set(str(_val[1]))
                self.p3_snsr.set(str(_val[2]))
                self.r.set(str(_val[3]))
                self.p.set(str(_val[4]))
                self.y.set(str(_val[5]))
                self.SV2_V.set(str(_val[6]))
                self.SV6_V.set(str(_val[7]))
                self.SV10_V.set(str(_val[8]))
            else :
                pass
                '''
                self.p1_snsr.set(str(snsrVal))
                self.p2_snsr.set(str(snsrVal))
                self.p3_snsr.set(str(snsrVal))
                self.r.set(str(snsrVal))
                self.p.set(str(snsrVal))
                self.y.set(str(snsrVal))
                '''

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

        def quitB(self) :
            try :
                self.bgTask.stop()
                self.master.destroy()
            except :
                pass

    root = Tk()
    gui = UnitTestGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()

if __name__ == "__main__":
    tkThreadingTest()