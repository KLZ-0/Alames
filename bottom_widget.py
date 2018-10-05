import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

# Created for relative positioning of internal labels
# same lvl as chartview

class BottomWidget(QWidget):
    def __init__(self, parent):
        super(BottomWidget, self).__init__(parent)

        self.scrollBar = QSlider(QtCore.Qt.Horizontal, self)
        self.scrollBar.setGeometry(0, 0, self.width(), self.scrollBar.height())
        self.slider = QScrollBar(QtCore.Qt.Horizontal, self)
        self.slider.setGeometry(0, self.scrollBar.height(), self.width(), self.slider.height())


    def applySettings(self):
        pass

    def resizeEvent(self, event):
        super(BottomWidget, self).resizeEvent(event)
        self.scrollBar.setGeometry(0, 0, self.width(), self.scrollBar.height())
        self.slider.setGeometry(0, self.scrollBar.height(), self.width(), self.slider.height())
