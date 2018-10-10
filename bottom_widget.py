import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

class BottomWidget(QWidget):
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """
    def __init__(self, parent):
        super(BottomWidget, self).__init__(parent)

        self.scrollBar = QSlider(QtCore.Qt.Horizontal, self)
        self.scrollBar.setGeometry(0, 0, self.width(), self.scrollBar.height())
        self.slider = QScrollBar(QtCore.Qt.Horizontal, self)
        self.slider.setGeometry(0, self.scrollBar.height(), self.width(), self.slider.height())


    def applySettings(self):
        pass

######## Event handlers

    def resizeEvent(self, event):
        super(BottomWidget, self).resizeEvent(event)
        self.scrollBar.setGeometry(0, 0, self.width(), self.scrollBar.height())
        self.slider.setGeometry(0, self.scrollBar.height(), self.width(), self.slider.height())
