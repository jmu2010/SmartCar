import serial
import serial.tools.list_ports
import threading
import binascii
import time
# 这个是主函数，调用其他UI和功能
from Ui_terminal import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from time import sleep
from PyQt5.QtWidgets import QMessageBox

# 串口的各种操作
class my_serial(object):
    # 1、列举可用端口号
    def list_ports(self):
        Com_List=[]
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            Com_List.append(port[0])
        return Com_List
    # 2、打开串口，获取串口参数
    port_status = 0  
    ser = serial.Serial()
    def get_port_para(self):
        #port_list = self.list_ports()
        #print(port_list)
        self.ser.port =       ui.comboBox.currentText()
        self.ser.baudrate = int(ui.comboBox_2.currentText())
        self.ser.bytesize  = int(ui.comboBox_3.currentText())
        self.ser.stopbits  = int(ui.comboBox_5.currentText())
        ParityValue         = ui.comboBox_6.currentText()
        self.ser.parity      = ParityValue[0]
        
        #print(port)
        # 添加异常的处理
    def open_port(self):  
        try:
            self.threading_test()
            if self.port_status == 0:
                self.ser.open()
                if self.ser.isOpen():
                    #self.t1 = threading.Thread(target=self.receive_data,args=())    # 开始接收数据
                    #self.t1 = threading.Thread(target=self.threading_test,args=(self.test_v, )) 
                    #self.t1.setDaemon(True)
                    #self.t1.start()
                    self.port_status = 1
                    print('Open success')
                else:
                    print('Open failure!') 
            else:
                self.ser.close()
                if not self.ser.isOpen():
                    #ui_para.label_11.setText('串口关闭')
                    #ui_para.pushButton_5.setText( "打开串口")
                    self.port_status = 0
                    print('Close success')
                else:
                    print('Close Failure!')
            #print(self.port_status)
            return self.port_status
        except (OSError, serial.SerialException):
                    QMessageBox.warning(None, '端口警告',"端口无效或者不存在", QMessageBox.Ok)
                    ui.comboBox.clear()# 清空端口列表
                    
    def send_data(self):
        if self.ser.isOpen():
            self.ser.write("A".encode())
    def receive_data(self):
        #sleep(0.5)
        if self.ser.isOpen():
            #size = self.ser.inWaiting()
            #while count < self.cnt:        
                    # 读取缓冲区数据个数
                #sleep(0.6)                
                #size = self.ser.inWaiting()
            #sleep(0.5)
                #res_data = self.ser.read_all()
            res_data = self.ser.read(16).decode()
                    #self.ser.flushInput() 
            #count+=1
            ui.lineEdit_mv.setText(res_data[1:5])
            ui.lineEdit_ma.setText(res_data[6:10])
            ui.lineEdit_spd.setText(res_data[11:15])
            print(res_data)
            return res_data
            sleep(0.5)
        #print('receive_data...')
    click_cnt  = 0
    def threading_test(self):
        self.click_cnt = self.click_cnt + 1
        if self.click_cnt  == 1:
            my_task.setDaemon(True)    #设为守护进程，随主线程一同退出
            my_task.start()
        elif self.click_cnt  == 2:
            my_task.pause()
        elif self.click_cnt  == 3:
            my_task.resume()
            self.click_cnt = 1

# 多线程处理部分
class Task(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            #print(time.time())
            #time.sleep(1)
            serial_tool.receive_data()

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False 

app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)


# 串口操作
serial_tool = my_serial()
my_task = Task()
# 刷新串口
def refresh_port_status():
    # 1、搜索可用串口
    ui.comboBox.clear()# 清空端口列表
    online_ports = serial_tool.list_ports()
    #print(online_ports, len(online_ports))
    # 2、在组合框0中进行显示
    for port in online_ports:
        ui.comboBox.addItem(port)
    serial_tool.get_port_para()
    #print(port)
refresh_port_status()
# 获取端口参数
serial_tool.get_port_para()
# 改变端口状态
def change_port_status():
    if serial_tool.port_status == 1:
        ui.label_11.setText('串口打开')
        ui.pushButton_5.setText( "关闭串口")
    elif serial_tool.port_status == 0:
        ui.label_11.setText('串口关闭')
        ui.pushButton_5.setText( "打开串口")
    #ui.lineEdit.setText(serial_tool.res_data)

#serial_tool.open_port()
# 槽函数集合
# 串口打开和关闭的槽函数
ui.pushButton_5.clicked.connect(serial_tool.open_port)
ui.pushButton_5.clicked.connect(change_port_status)
ui.pushButton.clicked.connect(serial_tool.send_data)
ui.pushButton_Reflesh.clicked.connect(refresh_port_status)

#print(serial_tool.open_port())
Dialog.show()
sys.exit(app.exec_())
