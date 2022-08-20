from PyQt5 import QtWidgets
from dialogthreeFrontend import Ui_Dialog_3
from PyQt5.QtWidgets import  QMainWindow
import serial

class Control(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_3()
        self.ui.setupUi(self)
        self.ser = serial.Serial("COM27", 9600, timeout=1)  # Change your port name COM... and your baudrate
        self.ui.pushButton.clicked.connect(self.moveForward)
        self.ui.pushButton_2.clicked.connect(self.moveRight)
        self.ui.pushButton_3.clicked.connect(self.moveLeft)
        self.ui.pushButton_4.clicked.connect(self.moveBackward)
    def moveForward(self):
        self.ser.write('F')
    def moveRight(self):
         self.ser.write('R')
    def moveLeft(self):
        self.ser.write('L')
    def moveBackward(self):
        self.ser.write('B')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    cont_ui = Control()
    cont_ui.show()
    sys.exit(app.exec_())
