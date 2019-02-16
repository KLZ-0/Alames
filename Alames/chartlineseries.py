import os, sys
from six import string_types
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

class ChartLineSeries(QLineSeries):
    def __init__(self, ydata=[]):
        super(ChartLineSeries, self).__init__()
        # TODO: Remove setup from constructor
        # TODO: Make a setYData method
        # TODO: Remove range modifying methods > the range will be the whole range of the dataholder (selectionDataHolder)
        #           Range reset will be available by setting the selectionDataHolder xdata and ydata from overallDataHolder
        # TODO: Preserve the basic access and modifying methods to keep backwards compatibility

######## Setters

    def setColor(self, color):
        if isinstance(color, string_types): # if color is a text in hex format
            self.setColor(QtGui.QColor(color))
        else:
            super(ChartLineSeries, self).setColor(color)
            self.hide()
            self.show()

    def setUseOpenGL(self, state):
        self.hide()
        super(ChartLineSeries, self).setUseOpenGL(state)
        self.show()

    def setData(self, ydata):
        """Replace current data with new data (better alternative to replaceData)"""

        newData = []
        for i in range(len(ydata)):
            # Set abstract X data
            newData.append(QtCore.QPointF(i, ydata[i]))

        self.replace(newData)

######## Getters

    def getStart(self):
        return self.firstPoint().x()

    def getEnd(self):
        return self.lastPoint().x()

    def max(self):
        return max(point.y() for point in self.pointsVector())

    def min(self):
        return min(point.y() for point in self.pointsVector())

    def firstPoint(self):
        return self.pointsVector()[0]

    def lastPoint(self):
        return self.pointsVector()[-1]

    def getPoint(self, pos):
        return self.pointsVector()[pos-1]
