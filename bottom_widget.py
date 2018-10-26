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

        self.scrollBar = QScrollBar(QtCore.Qt.Horizontal, self)
        self.scrollBar.setRange(1, 1000)
        self.scrollBar.valueChanged.connect(self.applySettings)


    def applySettings(self):
        # print(self.scrollBar.value())
        self.parent().chart.scroll(self.scrollBar.value()/100, 0)

######## Event handlers

    def resizeEvent(self, event):
        super(BottomWidget, self).resizeEvent(event)
        self.scrollBar.setGeometry(0, 0, self.width()-self.width()/6, self.scrollBar.height())

    def keyPressEvent(self, event):
        self.parent().chart.chart_view.keyPressEvent(event)
