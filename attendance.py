from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3
import attendance

from PyQt5.uic import loadUiType

ui,_ = loadUiType('attendance.ui')

con = sqlite3.connect("attendance.db")
cur = con.cursor()

class StartClass(QWidget, ui):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Attendance System")
        self.show()