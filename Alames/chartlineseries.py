import os, sys
from six import string_types
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

from Alames import scope

class ChartLineSeries(QLineSeries):
    """Derived class from QLineSeries"""

    # needsData is emitted at show() or setVisible(True)
    # needsData is connected to _setDataToQSerie(YDataNum)
    needsData = QtCore.pyqtSignal(int)
    scaleChanged = QtCore.pyqtSignal()

    _scale = 1

    def __init__(self):
        super(ChartLineSeries, self).__init__()

        self.setUseOpenGL(True)
        self.hide()
        # NOTE: The range will be the whole range of the dataholder (selectionDataHolder)
        #           Range reset will be available by setting the selectionDataHolder xdata and ydata from overallDataHolder

######## Overrides

    def setColor(self, color):
        if isinstance(color, string_types): # if color is a text in hex format
            self.setColor(QtGui.QColor(color))
        else:
            super(ChartLineSeries, self).setColor(color)
        self.setVisible(not self.isVisible())
        self.setVisible(not self.isVisible())

    def setUseOpenGL(self, state):
        self.setVisible(not self.isVisible())
        super(ChartLineSeries, self).setUseOpenGL(state)
        self.setVisible(not self.isVisible())

    def setVisible(self, state):
        if self.property("number") != None and state == True and not len(self.pointsVector()):
            self.needsData.emit(self.property("number"))
            scope.log("loaded in setVisible(True): %d" % self.property("number"))

        super(ChartLineSeries, self).setVisible(state)

    def show(self):
        if self.property("number") != None and not len(self.pointsVector()):
            self.needsData.emit(self.property("number"))
            scope.log("loaded in show(): %d" % self.property("number"))

        super(ChartLineSeries, self).show()

######## Setters

    def setData(self, ydata):
        """Replace current data with new data (better alternative to replaceData)"""

        newData = []
        for i in range(len(ydata)):
            # Set abstract X data
            newData.append(QtCore.QPointF(i, ydata[i]))

        self.replace(newData)
        self.rescale()

    def setLineScale(self, newScale):
        oldscale = self._scale
        self._scale = newScale
        self.rescale(oldscale)
        self.scaleChanged.emit()

    def rescale(self, oldscale=1):
        if self._scale == oldscale:
            # If scaling is not needed don't do it
            return 
        
        scope.log("scaled serie " + str(self.property("number")) + " by " + str(self._scale))

        scaledData = self.pointsVector()
        for point in scaledData:
            # The division is to set the scale to exactly the newscale instead of scalin an already scaled line
            point.setY(point.y()/oldscale * self._scale)
        self.replace(scaledData)

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
