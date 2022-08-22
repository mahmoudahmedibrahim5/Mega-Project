from main import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtGui import *
import serial
import cv2
import sys
from OpencvQT import Converter, Capture


class mainApp(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainApp, self).__init__()
        self.setupUi(self)
        self.bt_conn = 1

        try:
            self.ser = serial.Serial("COM8", 9600, timeout=0.1)  # Change your port name COM... and your baudrate
        except serial.SerialException:
            self.bt_conn = 0

        self.pushButton.clicked.connect(self.moveForward)
        self.pushButton_2.clicked.connect(self.moveRight)
        self.pushButton_3.clicked.connect(self.moveLeft)
        self.pushButton_4.clicked.connect(self.moveBackward)
        self.stitch_1.clicked.connect(self.Stitching_task)
        self.stereo_1.clicked.connect(self.StereoVision_task)
        self.speed_up.clicked.connect(self.higher_speed)
        self.speed_med.clicked.connect(self.med_speed)
        self.speed_down.clicked.connect(self.lower_speed)
        self.cam_screenshot.clicked.connect(self.cap_frame)
        self.view = qtw.QLabel()
        self.lay.addWidget(self.view, alignment=qtc.Qt.AlignCenter)
        self.view.setFixedSize(640, 400)
        self.init_camera()
       ## self.lcdcurrent.

        if self.bt_conn:
            self.robot_status.setText("Connected")
            self.robot_status.setStyleSheet("color: rgb(0, 0, 170);")
        else:
            self.robot_status.setText("Disconnected")
            self.robot_status.setStyleSheet("color: rgb(170, 0, 0);")

    def init_camera(self):
        self.capture = Capture()
        self.converter = Converter()
        captureThread = qtc.QThread(self)
        converterThread = qtc.QThread(self)
        self.converter.setProcessAll(False)
        captureThread.start()
        converterThread.start()
        self.capture.moveToThread(captureThread)
        self.converter.moveToThread(converterThread)
        self.capture.frameReady.connect(self.converter.processFrame)
        self.converter.imageReady.connect(self.setImage)
        self.capture.started.connect(lambda: print("started"))
        self.cam_start.clicked.connect(self.capture.start)
        ##self.cam_screenshot.clicked.connect(self.cap_frame)
        ##self..clicked.connect(self.capture.stop)

    @qtc.pyqtSlot(QImage)
    def setImage(self, image):
        self.view.setPixmap(QPixmap.fromImage(image))

    def cap_frame(self, frame):
        image = QImage(self.converter.image)
        ba = qtc.QByteArray()
        buff = qtc.QBuffer(ba)
        image.save("screenshot.jpg", "jpg")

    def moveForward(self):
        if self.bt_conn:
            self.dir_label.setText("Car Direction: Left")
            #self.ser.write(bytes("F\n", encoding = 'utf-8'))

    def moveRight(self):
        if self.bt_conn:
            self.dir_label.setText("Car Direction: Left")
            ##self.ser.write(bytes("R\n", encoding='utf-8'))

    def moveLeft(self):
        if self.bt_conn:
            self.dir_label.setText("Car Direction: Left")
            ##self.ser.write(bytes("L\n", encoding='utf-8'))

    def moveBackward(self):
        if self.bt_conn:
            self.dir_label.setText("Car Direction: Left")
            ##self.ser.write(bytes("B\n", encoding='utf-8'))

##next three function adjust motor speed and indicates the speed status on the screen
    def higher_speed(self):
        if self.bt_conn:
            self.label_2.setText("High")
            #self.ser.write(bytes("H\n", encoding = 'utf-8'))

    def med_speed(self):
        if self.bt_conn:
            self.label_2.setText("Medium")
            #self.ser.write(bytes("M\n", encoding = 'utf-8'))

    def lower_speed(self):
        if self.bt_conn:
            self.label_2.setText("Low")
            #self.ser.write(bytes("L\n", encoding = 'utf-8'))

    ## SOFTWARE TASKS CODE IMPLEMENTATION  HERE
    def Stitching_task(self):
        ## Put Stitching and object detection code here
        pass

    def StereoVision_task(self):
        # Put Stereovision code here
        pass

if __name__ == '__main__':
    app = qtw.QApplication([])
    final = mainApp()
    final.show()
    app.exec_()