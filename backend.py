from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog , QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage , QPixmap
from frontend import Ui_MainWindow
from dialogFrontend import Ui_Dialog
from dialogtwoFrontend import Ui_Dialog_2
import cv2

class megaProject(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.image= None
        self.ui.dialog1.clicked.connect(self.dialog_One)
        self.ui.dialog2.clicked.connect(self.dialog_Two)
        self.ui.pushButton_4.clicked.connect(self.start_Webcam)
    def dialog_One(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
    def dialog_Two(self):
        Dialog_2 = QtWidgets.QDialog()
        ui = Ui_Dialog_2()
        ui.setupUi(Dialog_2)
        Dialog_2.show()
        Dialog_2.exec_()
    def start_Webcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.timer= QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(5)
    def update_frames(self):
        ret , self.image= self.capture.read()
        self.image.cv2.flip(self.image, 1)
        self.displayImage(self.image , 1)
    def displayImage(self,img,window=1):
        qformat= QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB8888
        outImage= QImage(img,img.shape[1],img.shape[0],img.strides[0], qformat)
        outImage=outImage.rgbSwapped()
        if window==1:
            self.ui.label.setPixmap(QPixmap.fromImage(outImage))
            self.ui.label.setScaledContents(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mega_ui = megaProject()
    mega_ui.show()
    sys.exit(app.exec_())