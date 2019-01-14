import os, sys
from six import string_types
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

class ChartLineSeries(QLineSeries):
    def __init__(self, ydata=[]):
        super(ChartLineSeries, self).__init__()

        self.baseRangeXData = range(len(ydata))

        for i in self.baseRangeXData:
            self.append(i, ydata[i])

        self.baseVect = self.pointsVector()
        self.currentVect = self.baseVect

        self.start = self.baseRangeXData[0]
        self.end = self.baseRangeXData[-1]

######## Update Actions

    def update(self):
        self.currentVect = self.baseVect[self.start:self.end+1]
        self.replace(self.currentVect)

######## Setters

    def setRange(self, start, end):
        """Expects a range between 0-max range of the chart"""
        self.start = start
        self.end = end
        self.update()

    def resetRange(self):
        self.start = self.baseRangeXData[0]
        self.end = self.baseRangeXData[-1]
        self.update()

    def setBaseData(self, baseData):
        self.baseVect = baseData
        self.update()

    def setColor(self, color):
        if isinstance(color, string_types): # if color is a text in hex format
            self.setColor(QtGui.QColor(color))
        else:
            super(ChartLineSeries, self).setColor(color)
            self.update()
            # TODO: update chart to get rid of openGL frags or update color of the openGL rendered parts

    def setUseOpenGL(self, state):
        self.hide()
        super(ChartLineSeries, self).setUseOpenGL(state)
        self.show()

######## Getters

    def baseData(self):
        return self.baseVect

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getBaseStart(self):
        return self.baseRangeXData[0]

    def getBaseEnd(self):
        return self.baseRangeXData[-1]

    def max(self):
        return max(point.y() for point in self.currentVect)

    def min(self):
        return min(point.y() for point in self.currentVect)

    def firstPoint(self):
        return self.currentVect[0]

    def lastPoint(self):
        return self.currentVect[-1]

    def getPoint(self, pos):
        return self.currentVect[pos]
