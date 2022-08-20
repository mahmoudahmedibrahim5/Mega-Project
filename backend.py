from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog , QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage , QPixmap
from frontend import Ui_MainWindow
from dialogFrontend import Ui_Dialog
from dialogtwoFrontend import Ui_Dialog_2
from dialogthreeFrontend import Ui_Dialog_3
from dialogthreeBackend import Control

import cv2

class megaProject(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.dialog1.clicked.connect(self.dialog_One)
        self.ui.dialog2.clicked.connect(self.dialog_Two)
        self.ui.control.clicked.connect(self.dialog_Three)
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
    def dialog_Three(self):
        Dialog_3 = QtWidgets.QDialog()
        ui = Ui_Dialog_3()
        ui.setupUi(Dialog_3)
        Dialog_3.show()
        Dialog_3.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mega_ui = megaProject()
    mega_ui.show()
    sys.exit(app.exec_())