import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets


class Capture(QtCore.QObject):
    started = QtCore.pyqtSignal()
    frameReady = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super(Capture, self).__init__(parent)
        self._frame = None
        self.m_timer = QtCore.QBasicTimer()
        self.m_videoCapture = cv2.VideoCapture()

    @QtCore.pyqtSlot()
    def start(self, cam=0):
        if self.m_videoCapture is not None:
            self.m_videoCapture.release()
            self.m_videoCapture = cv2.VideoCapture(cam)
        if self.m_videoCapture.isOpened():
            self.m_timer.start(0, self)
            self.started.emit()

    @QtCore.pyqtSlot()
    def stop(self):
        self.m_timer.stop()

    def __del__(self):
        self.m_videoCapture.release()

    def frame(self):
        return self.m_frame

    def timerEvent(self, event):
        if event.timerId() != self.m_timer.timerId():
            return

        ret, val = self.m_videoCapture.read()
        if not ret:
            self.m_timer.stop()
            return
        self.m_frame = val
        self.frameReady.emit(self.m_frame)

    frame = QtCore.pyqtProperty(np.ndarray, fget=frame, notify=frameReady, user=True)

class Converter(QtCore.QObject):
    imageReady = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(Converter, self).__init__(parent)
        self.m_frame = np.array([])
        self.m_timer = QtCore.QBasicTimer()
        self.m_processAll = True
        self.m_image = QtGui.QImage()

    def queue(self, frame):
        self.m_frame = frame
        if not self.m_timer.isActive():
            self.m_timer.start(0, self)

    def process(self, frame):
        w, h, _ = frame.shape
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.m_image = QtGui.QImage(rgbImage.data, h, w, QtGui.QImage.Format_RGB888)
        self.imageReady.emit(QtGui.QImage(self.m_image))

    def timerEvent(self, event):
        if event.timerId() != self.m_timer.timerId():
            return
        self.process(self.m_frame)
        self.m_timer.stop()

    def processAll(self):
        return self.m_processAll

    def setProcessAll(self, _all):
        self.m_processAll = _all

    def processFrame(self, frame):
        if self.m_processAll:
            self.process(frame)
        else:
            self.queue(frame)

    def image(self):
        return self.m_image

    image = QtCore.pyqtProperty(QtGui.QImage, fget=image, notify=imageReady, user=True)
    processAll = QtCore.pyqtProperty(bool, fget=processAll, fset=setProcessAll)