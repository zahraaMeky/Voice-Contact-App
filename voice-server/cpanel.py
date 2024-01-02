import sys
from audio import AudioReceiver, ServerConnection
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QTimer,QDateTime, QCoreApplication
from bluetooth import *
import sys
import subprocess
import speaker
import subprocess
import os
from time import sleep

class CustomDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface = "wlan0"

        # self.setWindowTitle("Room Info")

        self.setFixedWidth(500)
        self.setFixedHeight(350)

        QBtn = QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        # self.frame_2 = QtWidgets.QFrame()
        # self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_2.setObjectName("frame_2")
        # self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        # self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        # self.label.mousePressEvent = self.closeWindow

        # self.verticalLayout_2.addWidget(self.label)
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel()
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.line_4 = QtWidgets.QFrame()
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_5.addWidget(self.line_4)
        self.label_ip = QtWidgets.QLabel()
        self.label_ip.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip.setObjectName("label_ip")
        self.horizontalLayout_5.addWidget(self.label_ip)
        
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel()
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_9.setText("Status")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.line_9 = QtWidgets.QFrame()
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout_9.addWidget(self.line_9)
        self.label_ip_connection = QtWidgets.QLabel()
        self.label_ip_connection.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip_connection.setObjectName("label_ip_connection")
        self.horizontalLayout_9.addWidget(self.label_ip_connection)

        self.line_mid = QtWidgets.QFrame()
        self.line_mid.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_mid.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_mid.setObjectName("line_end")

        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.label_16 = QtWidgets.QLabel()
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setText("static ip")
        self.horizontalLayout_15.addWidget(self.label_16)
        self.line_14 = QtWidgets.QFrame()
        self.line_14.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout_15.addWidget(self.line_14)
        # self.label_ip2 = QtWidgets.QLabel()
        # self.label_ip2.setAlignment(QtCore.Qt.AlignCenter)
        self.edit_ip = QtWidgets.QLineEdit()
        self.horizontalLayout_15.addWidget(self.edit_ip)
        
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.staticip_button = QtWidgets.QPushButton()
        self.staticip_button.clicked.connect(self.actionIP)
        self.staticip_button.setText("set new static ip")
        self.horizontalLayout_19.addWidget(self.staticip_button)
        # self.line_19 = QtWidgets.QFrame()
        # self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        # self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.horizontalLayout_19.addWidget(self.line_19)

        self.line_end = QtWidgets.QFrame()
        self.line_end.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_end.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_end.setObjectName("line_end")

        self.label.setText("Room Info")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line)
        self.layout.addLayout(self.horizontalLayout_5)
        self.layout.addLayout(self.horizontalLayout_9)
        # self.layout.addWidget(self.line_mid)
        # self.layout.addLayout(self.horizontalLayout_15)
        # self.layout.addLayout(self.horizontalLayout_19)
        self.layout.addWidget(self.line_end)
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.running = self.getRunning()
        self.ip = self.getIP(self.interface)
        self.label_6.setText("IP Address")
        self.label_ip.setText(self.ip)

        if (self.running):
            self.label_ip_connection.setText("Connected")
        else:
            self.label_ip_connection.setText("Disconnected")

    def getRunning(self):
        running = False
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.connect(("8.8.8.8", 80))
            # ip = my_socket.getsockname()[0]
            # print('Your IP Address is',ip)
            running = True
        except:
            running = False
        return running
    
    def getIP(self, interface):
        ip = None
        proc = subprocess.Popen('ifconfig ' + interface, shell=True, stdout=subprocess.PIPE)
        stdout = proc.communicate()[0].decode()
        proc.wait()
        ip = stdout.split("\n")[1].strip().split(" ")[1].strip()
        if (len(ip.split("."))!=4):
            ip = None

        return ip
        
    def setIP(self, old, new):
        fname= "/etc/dhcpcd.conf"
        file = open(fname, 'r')
        content = file.read()
        i = 0
        n = 0
        for line in content.split('\n'):
            if (self.interface in line):
                if (line[0]!="#"):
                    n = i
            i += 1
        if (n>0):
            m = n + 1
            old_ip = content.split('\n')[m].split("=")[1].split("/")[0]
            content = content.replace(old, new)
        else:
            new_config = "\n\ninterface "+ self.interface + "\n" +  "static ip_address="+ new +"/24\n" + "static routers=192.168.31.1\n" + "static domain_name_servers=192.168.31.1\n"
            content += new_config
        file = open(fname, 'w')
        file.write(content)
        os.system("sudo ifconfig " + self.interface + " down")
        os.system("sudo ifconfig " + self.interface + " up")
        sleep(4)
        print("restart networking service")
        os.system("sudo service networking restart")
        sleep(8)
        # print("DONE")


    def setStaticIP(self, static_ip):
        ip = self.getIP(self.interface)
        print("Old System IP : " , ip)
        self.setIP(ip, static_ip)
        ip = self.getIP(self.interface)
        print("New System IP : " , ip)

        return True
        #if (ip==static_ip): return True
        #else: return False

    def actionIP(self):
        newIP = self.edit_ip.text()
        if (len(newIP.split("."))==4):
            print(newIP)
            self.alert(newIP)

    def alert(self, ip):
        reply = QMessageBox.question(self, 'Set Static IP', 'Are you sure you want to set static ip to : ' + ip + ' ?\nSystem reboot after setting static ip',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.waiting()
            done = self.setStaticIP(ip)
            if (done):
                print("DONE")
                print("Rebooting")
                os.system("echo voicetoall | sudo reboot")

    def waiting(self):
        reply = QMessageBox.question(self, 'Processing', 'Please wait...',
        QMessageBox.No, QMessageBox.No)


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        self.speaker = speaker.Speaker()
   
        self.ip, self.running = self.getIP()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame()
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.mousePressEvent = self.closeWindow

        self.verticalLayout_2.addWidget(self.label)
        self.once = False

        self.line = QtWidgets.QFrame(self.frame_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.line_4 = QtWidgets.QFrame(self.frame_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_5.addWidget(self.line_4)
        self.label_ip = QtWidgets.QLabel(self.frame_2)
        self.label_ip.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip.setObjectName("label_ip")
        self.horizontalLayout_5.addWidget(self.label_ip)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.line_5 = QtWidgets.QFrame(self.frame_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_6.addWidget(self.line_5)
        self.label_ip_connection = QtWidgets.QLabel(self.frame_2)
        self.label_ip_connection.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip_connection.setObjectName("label_ip_connection")
        self.horizontalLayout_6.addWidget(self.label_ip_connection)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 2)
        self.verticalLayout_2.setStretch(3, 2)

        self.frame_1 = QtWidgets.QFrame(self.centralwidget)
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.frame_1)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label1 = QtWidgets.QLabel(self.frame_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label1.setFont(font)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label1")
        self.label1.mousePressEvent = self.closeWindow
        self.verticalLayout_21.addWidget(self.label1)
        self.line1 = QtWidgets.QFrame(self.frame_1)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.verticalLayout_21.addWidget(self.line1)

        self.horizontalLayout_select = QtWidgets.QHBoxLayout()
        self.label_select = QtWidgets.QLabel()
        self.label_select.setText("Select Speaker")

        self.cb = QtWidgets.QComboBox()
        # self.cb.currentIndexChanged.connect(self.selectPairedSpeaker)

        self.connect_paired_button = QtWidgets.QPushButton()
        self.connect_paired_button.setText("connect")
        self.connect_paired_button.clicked.connect(self.selectPairedSpeaker)

        self.horizontalLayout_select.addWidget(self.label_select)
        self.horizontalLayout_select.addWidget(self.cb)
        self.horizontalLayout_select.addWidget(self.connect_paired_button)
        self.verticalLayout_21.addLayout(self.horizontalLayout_select)

        self.line__ = QtWidgets.QFrame()
        self.line__.setFrameShape(QtWidgets.QFrame.HLine)
        self.line__.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout_21.addWidget(self.line__)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_1)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        
        self.horizontalLayout_4.addWidget(self.label_2)
        self.line_2 = QtWidgets.QFrame(self.frame_1)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_4.addWidget(self.line_2)
        self.label_speaker_name = QtWidgets.QLabel(self.frame_1)
        self.label_speaker_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_speaker_name.setObjectName("label_speaker_name")
        self.horizontalLayout_4.addWidget(self.label_speaker_name)
        self.verticalLayout_21.addLayout(self.horizontalLayout_4)
        
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.frame_1)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.line_3 = QtWidgets.QFrame(self.frame_1)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_3.addWidget(self.line_3)
        self.label_speaker_connection = QtWidgets.QLabel(self.frame_1)
        self.label_speaker_connection.setAlignment(QtCore.Qt.AlignCenter)
        self.label_speaker_connection.setObjectName("label_speaker_connection")
        self.horizontalLayout_3.addWidget(self.label_speaker_connection)

        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.label_14 = QtWidgets.QLabel(self.frame_1)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setText("Action")
        self.horizontalLayout_13.addWidget(self.label_14)
        self.line_13 = QtWidgets.QFrame(self.frame_1)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout_13.addWidget(self.line_13)

        self.label_speaker_action = QtWidgets.QWidget(self.frame_1)
        self.label_speaker_action.setObjectName("label_speaker_action")
        self.horizontalLayout_13.addWidget(self.label_speaker_action)

        self.verticalLayout_21.addLayout(self.horizontalLayout_3)
        self.verticalLayout_21.addLayout(self.horizontalLayout_13)
        self.verticalLayout_21.setStretch(0, 1)
        self.verticalLayout_21.setStretch(1, 1)
        self.verticalLayout_21.setStretch(2, 1)
        self.verticalLayout_21.setStretch(3, 2)
        self.verticalLayout_21.setStretch(4, 2)
        self.verticalLayout_21.setStretch(5, 2)
        self.verticalLayout_21.setStretch(6, 2)

        # self.horizontalLayout.addWidget(self.frame_1)
        self.verticalLayout.addLayout(self.horizontalLayout)


        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_info = QtWidgets.QPushButton()
        self.btn_info.setText("IP INFO")
        self.btn_info.clicked.connect(self.button_clicked)
        self.label_10 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.btn_info)
        self.verticalLayout_3.addWidget(self.label_10)
        self.line_6 = QtWidgets.QFrame(self.frame)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_3.addWidget(self.line_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.label_streaming_status = QtWidgets.QLabel(self.frame)
        self.label_streaming_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_streaming_status.setObjectName("label_streaming_status")
        self.horizontalLayout_7.addWidget(self.label_streaming_status)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        
        # add slider
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        # self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider.setTickInterval(5)
        self.slider.setSingleStep(1)
        self.slider.setValue(float(self.get_volume()))
        self.slider.valueChanged.connect(self.valuechange)
        self.slider.setMinimumSize(0, 40)
       
        self.label_volume_title = QtWidgets.QLabel()
        self.label_volume_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_volume_title.setText("Volume")

        self.label_volume_value = QtWidgets.QLabel()
        self.label_volume_value.setAlignment(QtCore.Qt.AlignCenter)
        self.label_volume_value.setText(" " + str(self.get_volume()) + "%")

        self.button_decrease = QtWidgets.QPushButton()
        self.button_decrease.setText("-")
        self.button_decrease.clicked.connect(lambda: self.add_volume(-10))
        self.button_decrease.setFixedWidth(40)

        self.button_increase = QtWidgets.QPushButton()
        self.button_increase.setText("+")
        self.button_increase.clicked.connect(lambda: self.add_volume(10))
        self.button_increase.setFixedWidth(40)


        # self.horizontalLayout_8.addWidget(self.label_volume_title)
        self.horizontalLayout_8.addWidget(self.button_decrease)
        self.horizontalLayout_8.addWidget(self.slider)
        self.horizontalLayout_8.addWidget(self.button_increase)
        # self.horizontalLayout_8.addWidget(self.label_volume_value)

        # self.horizontalLayout_8.setStretch(0, 0)
        # self.horizontalLayout_8.setStretch(1, 1)
        # self.horizontalLayout_8.setStretch(2, 0)

        self.label_volume_value.setFixedHeight(30)
        
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.verticalLayout_3.addWidget(self.label_volume_value)
        self.horizontalLayout.addWidget(self.frame)

        self.verticalLayout_3.setStretch(5,0)
        # self.horizontalLayout.addWidget(self.frame_1)
      
        self.frame_4 = QtWidgets.QFrame()
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_4)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 351, 187))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.devicesLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.devicesLayout.setObjectName("devicesLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        
        self.button_layout = QtWidgets.QHBoxLayout()

        self.h_layout = QtWidgets.QHBoxLayout(self.frame_4)

        self.button_scan = QtWidgets.QPushButton(self.frame_4)
        self.button_scan.setObjectName("button_scan")
        self.button_scan.clicked.connect(self.scan)

        self.button_scan_reset = QtWidgets.QPushButton(self.frame_4)
        self.button_scan_reset.setObjectName("button_scan_reset")
        self.button_scan_reset.setText("Reset")
        self.button_scan_reset.clicked.connect(self.resetScan)

        self.h_layout.addWidget(self.button_scan_reset)
        self.h_layout.addWidget(self.button_scan)
        self.h_layout.setStretch(1, 1)

        self.h_widget = QtWidgets.QWidget(self.frame_4)
        self.h_widget.setLayout(self.h_layout)

        self.verticalLayout_4.addWidget(self.h_widget)

        self.horizontalLayout.addWidget(self.frame_4)
        self.horizontalLayout.addWidget(self.frame_1)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.info = CustomDialog(self)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        device, paired = self.speaker.check_devices()
        print("connected device : ", device)
        if (device):
            self.label_speaker_name.setText(device["name"])
            self.label_speaker_connection.setText("connected")

        self.setup_server()
        self.start_server()

        self.timer_check = QTimer(self)
        self.timer_check.timeout.connect(self.checkInfo)
        self.timer_check.start(5000)

        self.timer_clientcheck = QTimer(self)
        self.timer_clientcheck.timeout.connect(self.check_if_client_connected)
        self.timer_clientcheck.start(1000)

    def selectPairedSpeaker(self):
        i = self.cb.currentIndex()
        print("index: " , i)
        self.connect_dev(None, self.paired[i])
        
        
    def add_volume(self, vol):
        v = int(self.get_volume())
        v += vol
        if (v>100): v = 100
        elif (v<0): v = 0
        self.set_volume(v)
        self.slider.setValue(v)

    def button_clicked(self, s):
        print("click", s)

        # self.info = CustomDialog(self)
        if self.info.exec():
            print("Success!")
        else:
            print("Cancel!")

    def valuechange(self, value):
        print("volume : " , value)
        self.set_volume(value)
        self.label_volume_value.setText(" " + str(self.get_volume()) + "%")

    def addActionButton(self):
        # self.button_layout = QtWidgets.QHBoxLayout()
        self.clearActionButton()
        self.button_speaker_action = QtWidgets.QPushButton()
        self.button_speaker_action.setObjectName("button_speaker_action")
        self.button_speaker_action.setText("Disconnect")
        self.button_speaker_action.clicked.connect(self.disconnect_speaker)
        self.button_layout.addWidget(self.button_speaker_action)
        self.label_speaker_action.setLayout(self.button_layout)

    def clearActionButton(self):
        self.clearLayout(self.button_layout)

    def resetScan(self):
        self.clearLayout(self.devicesLayout)

    def scan(self):
        self.resetScan()
        self.loading()
        self.scan_timer = QTimer(self)
        self.scan_timer.timeout.connect(self.Scanning)
        self.scan_timer.start(10)

    def disconnect_speaker(self):
        print("disconnect")
        self.speaker.disconnect()

    def Scanning(self):
        self.speaker.scan_devices_cmd()
        devs = self.speaker.scan_devices()
        print(devs)
        self.resetScan()
        for dev in devs:
            self.device_node(dev)
        self.scan_timer.stop()
        # self.spinner.stop()
        
    def device_node(self, dev):
        devLayout = QtWidgets.QHBoxLayout()
        devlabel_1 = QtWidgets.QLabel(self.scrollArea)
        devlabel_1.setAlignment(QtCore.Qt.AlignCenter)
        devlabel_1.setText(dev["name"])
        devLayout.addWidget(devlabel_1)
        devline_1 = QtWidgets.QFrame(self.frame_4)
        devline_1.setFrameShape(QtWidgets.QFrame.VLine)
        devline_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        # devline_1.setObjectName("devline_1")
        devLayout.addWidget(devline_1)
        dev_status = QtWidgets.QLabel(self.scrollArea)
        dev_status.setAlignment(QtCore.Qt.AlignCenter)
        # dev_status.setObjectName("dev_status")
        dev_status.setText(dev["mac"])
        devLayout.addWidget(dev_status)
        # frame = QtWidgets.QFrame()
        frame = QtWidgets.QGroupBox("")
        frame.setFixedHeight(100)
        frame.setLayout(devLayout)
        frame.mousePressEvent = lambda a: self.connect_dev(a, dev)

        # frame.setStyleSheet("QGroupBox#dframe{background-color:grey}")
        self.devicesLayout.addWidget(frame)
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def connect_dev(self, event, dev):
        print("clicked : " , dev)
        reply = QMessageBox.question(self, 'Connect', 'Are you sure you want to connect to ' + dev["name"] + '?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # event.accept()
            connected = self.speaker.connectTo(dev["mac"])
            if (connected):
                print("connected")
                self.label_speaker_name.setText(dev["name"])
                self.label_speaker_connection.setText("connected")
                self.resetScan()
                self.once = False

    def checkPairedSpeakers(self):
        device, self.paired = self.speaker.check_devices()
        if (device==None):
            # self.once = False
            self.cb.clear()
            for pair in self.paired:
                self.cb.addItem(pair["name"])

            self.once = True


    def checkInfo(self):
        device, self.paired = self.speaker.check_devices()
        print("connected device : ", device)
        if (device):
            if (self.connection): self.connection.set_speaker(1)
            self.label_speaker_name.setText(device["name"])
            self.label_speaker_connection.setText("connected")
            self.addActionButton()
            self.cb.setEnabled(False)
            self.connect_paired_button.setEnabled(False)
        else:
            if (self.connection): self.connection.set_speaker(0)
            self.label_speaker_name.setText("-")
            self.label_speaker_connection.setText("-")
            self.clearActionButton()
            self.cb.setEnabled(True)
            self.connect_paired_button.setEnabled(True)
            if(not self.once): self.checkPairedSpeakers()
            # self.once = True
            # self.cb.clear()
            # for pair in self.paired:
            #     self.cb.addItem(pair["name"])

            # self.once = False

        ip, self.running = self.getIP()
        # print(self.running)
        if (self.running):
            self.info.label_ip_connection.setText("Connected")
        else:
            self.info.label_ip_connection.setText("Disconnected")
        
    def check_if_client_connected(self):

        check = self.receiver.check_client()
        print("check client : " , check)
        if(check):
            self.label_streaming_status.setText("Running")
        else:
            self.label_streaming_status.setText("Closed")

    def showTime(self):
        time=QDateTime.currentDateTime()
        timeDisplay=time.toString('yyyy-MM-dd hh:mm:ss dddd')
        print(timeDisplay)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Room Info"))
        self.label_6.setText(_translate("MainWindow", "IP Address"))
        self.label_ip.setText(_translate("MainWindow", self.ip))
        self.label_8.setText(_translate("MainWindow", "Status"))
        self.label_ip_connection.setText(_translate("MainWindow", "-"))
        self.label1.setText(_translate("MainWindow", "Speaker Info"))
        self.label_2.setText(_translate("MainWindow", "Speaker Name"))
        self.label_speaker_name.setText(_translate("MainWindow", "-"))
        self.label_4.setText(_translate("MainWindow", "Status"))
        self.label_speaker_connection.setText(_translate("MainWindow", "-"))
        self.label_10.setText(_translate("MainWindow", "Speaking Part"))
        self.label_11.setText(_translate("MainWindow", "Status"))
        self.label_streaming_status.setText(_translate("MainWindow", "-"))
        self.button_scan.setText(_translate("MainWindow", "Scan Bluetooth Speakers"))

    def loading(self):
        print("loading")
        label = QtWidgets.QLabel()
        label.setText("Scanning...")
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.devicesLayout.addWidget(label)
     
  
    def get_volume(self):
        proc = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE)
        amixer_stdout = proc.communicate()[0].decode().split('\n')[5]
        proc.wait()
        find_start = amixer_stdout.find('[') + 1
        find_end = amixer_stdout.find('%]', find_start)
        return amixer_stdout[find_start:find_end]

    def set_volume(self, volume):
        val = volume
        val = float(int(val))
        proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
        proc.wait()
        

    def getIP(self):
        running = False
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.connect(("8.8.8.8", 80))
            ip = my_socket.getsockname()[0]
            # print('Your IP Address is',ip)
            running = True
        except:
            ip = ""
            running = False
        return ip, running
    
    def setup_server(self):
        # self.HOST = '0.0.0.0'
        self.HOST = ''
        self.PORT = 9999
        self.receiver = AudioReceiver(self.HOST, self.PORT, 100)
        self.connection = ServerConnection(self.HOST, 7777)
        self.connection.start_server()

    def start_server(self):
        if (self.receiver): 
            self.receiver.start_server()
            print(self.receiver.isRunning())
        else:
            self.setup_server()
            self.receiver.start_server()
            print(self.receiver.isRunning())

    def closeWindow(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print(self.quit)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
    # def closeWindow(self):
    #     reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
    #     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         print(self.quit)

    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            print(self.quit)
        else:
            event.ignore()
        # print(self.quit)


app = QApplication([])

window = Window()
window.show()
# window.showFullScreen()
sys.exit(app.exec())