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
        self.stitch_1.clicked.connect(self.S_Task1)
        self.stereo_1.clicked.connect(self.S_Task2)
        self.cam_screenshot.clicked.connect(self.cap_frame)
        self.view = qtw.QLabel()
        self.lay.addWidget(self.view, alignment=qtc.Qt.AlignCenter)
        self.view.setFixedSize(640, 400)
        self.init_camera()
        self._translate = qtc.QCoreApplication.translate

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
        #self.ser.write(bytes("F\n", encoding = 'utf-8'))
        print("message: ")
        self.dir_label.setText("Car Direction: Forward")
        #msg = self.ser.readline().decode()
        #print(msg)

    def moveRight(self):
        self.dir_label.setText("Car Direction: Right")
        ##self.ser.write(bytes("R\n", encoding='utf-8'))

    def moveLeft(self):
        pass
        ##self.ser.write(bytes("L\n", encoding='utf-8'))

    def moveBackward(self):
        self.ser.write(bytes("B\n", encoding='utf-8'))
        print("THE MESSAGE IS: ")
        msg = self.ser.read_until().decode()
        print(msg)

    def carSpeed(self):
        slow, med, fast = "slow", "medium", "fast"
        # use label.settext function to change text label depending on speed
        pass

    ## SOFTWARE TASKS CODE IMPLEMENTATION  HERE
    def S_Task1(self):
        ## Here we open a QDialog for the software image stitching task after implementing its code
        pass
    def S_Task2(self):
        # Here we open a QDialog for the software stereo vision task after implementing its code
        pass


if __name__ == '__main__':
    app = qtw.QApplication([])
    final = mainApp()
    final.show()
    app.exec_()