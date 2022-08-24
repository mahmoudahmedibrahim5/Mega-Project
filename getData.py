import sys
import time
import serial
import serial.tools.list_ports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,QTimer
from PyQt5.QtWidgets import QMessageBox,QWidget
import csv
import numpy as np
import warnings
import serial
import serial.tools.list_ports

class GetData(QThread):
    Readings = QtCore.pyqtSignal(float, float)

    def __init__(self, ser):
        QThread.__init__(self)
        self.ser = ser
        # arduino_ports = [  # automatically searches for an Arduino and selects the port it's on
        #     p.device
        #     for p in serial.tools.list_ports.comports()
        #     if 'Arduino' in p.description
        # ]
        #
        # if not arduino_ports:
        #     raise IOError("No Arduino found - is it plugged in? If so, restart computer.")
        # if len(arduino_ports) > 1:
        #     warnings.warn('Multiple Arduinos found - using the first')
        # self.ser = serial.Serial(arduino_ports[0], 9600, timeout=1)

        ## ADD THE COM PORT OF BLUETOOTH HERE
        # try:
        #     self.ser = serial.Serial("COM4", 9600, timeout=0.1)  # Change your port name COM... and your baudrate
        # except serial.SerialException:
        #     pass

    def __del__(self):  # part of the standard format of a QThread
        self.wait()

    def run(self):  # also a required QThread function, the working part
        self.ser.close()
        self.ser.open()
        self.ser.flush()
        self.ser.reset_input_buffer()
        start_time = time.time()

        while True:
            while self.ser.inWaiting() == 0:
                pass
            try:
                data = self.ser.readline()
                dataarray = data.decode().rstrip().split(',')
                self.ser.reset_input_buffer()
                voltage = float(dataarray[0])
                current = float(dataarray[1])
                self.Readings.emit(voltage, current)
                # print(voltage, current)
            except(KeyboardInterrupt, SystemExit, IndexError, ValueError):
                pass
