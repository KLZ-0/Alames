import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis
import pandas
import numpy as np
import math
import lzma

from Alames import scope

from Alames import chartview
from Alames import leftwidget
from Alames import chartmodifier
from Alames.dataholderbase import DataHolderBase
from Alames.dataholder import DataHolder

class Chart(QChart, chartmodifier.ChartModifier):
    """
    Purpose: setup and modify the QChart
    Manages the charting subsystem consisting of the ChartView, Properties and BottomWidget.
    Initializes the required objects as its own properties
    """

    # Updated from LeftWidget
    _scrollSpeed = 10

    def __init__(self):
        super(Chart, self).__init__()
        self.selectionDataHolder = DataHolder()
        self.overallDataHolder = DataHolderBase()

######## Setup

    def constructChart(self, fileName):
        self.setAcceptHoverEvents(True)

        self.loadCSV(fileName)
        for serie in self.selectionDataHolder.getQSeries():
            self.addSeries(serie)
            serie.visibleChanged.connect(self.updateAxes)
            serie.scaleChanged.connect(self.updateAxes)

    def loadCSV(self, lFileName):
        if lFileName.endswith(".csv.xz"):
            try:
                lFileName = lzma.open(lFileName) # file name or object
            except lzma.LZMAError:
                scope.errorPopup("LZMA decompression failed - damaged xz file")

        # Detect a header -> set data header to be the second line
        f = pandas.read_csv(lFileName, header=1, delimiter=";", low_memory=False)
        
        self.selectionDataHolder.setDataFromCSV(f)
        self.overallDataHolder.setDataFromCSV(f)

######## Signal handlers

    def onSelectionChange(self, range):
        # call in ....connect(self.onSelectionChange)
        # self.selectionDataHolder.update(range)
        pass

######## Getters

    def getXData(self):
        return self.selectionDataHolder.XData()

    def getYData(self, num=None):
        if num != None:
            return self.selectionDataHolder.getYData(num)
        return self.selectionDataHolder.YData()

    def getDummyQSerie(self):
        return self.selectionDataHolder.getDummyQSerie()

    def getRange(self):
        try:
            return self.selectionDataHolder.getDummyQSerie().getStart(), self.selectionDataHolder.getDummyQSerie().getEnd()
        except IndexError:
            return 0

    def getStart(self):
        try:
            return self.selectionDataHolder.getDummyQSerie().getStart()
        except IndexError:
            return 0

    def getEnd(self):
        try:
            return self.selectionDataHolder.getDummyQSerie().getEnd()
        except IndexError:
            return 0

    def getScrollSpeed(self):
        return self._scrollSpeed

######## Setters

    def setScrollSpeed(self, scrollspeed):
        self._scrollSpeed = scrollspeed

######## Series modifier

    def setRange(self, start, end):
        self.selectionDataHolder.setRange(start, end)
        self.resetZoom()
        scope.window.updateChildren()

######## View modifiers

    def setZoom(self, start, end):
        firstPoint = self.mapToPosition(QtCore.QPoint(start, 0), self.selectionDataHolder.getDummyQSerie())
        lastPoint = self.mapToPosition(QtCore.QPoint(end, 0), self.selectionDataHolder.getDummyQSerie())
        area = self.plotArea()
        self.zoomIn(QtCore.QRectF(firstPoint.x(), area.y(), lastPoint.x() - firstPoint.x(), area.height()))

    def resetZoom(self):
        self.setZoom(self.getStart(), self.getEnd())

    def zoomReset(self):
        """Override the inherited method"""
        self.resetZoom()

######## Toggle actions

    def toggleSerieVisiblity(self, key):
        if int(key) > len(self.series()):
            return
        if self.series()[int(key) - 1].isVisible():
            self.series()[int(key) - 1].hide()
        else:
            self.series()[int(key) - 1].show()

        # Trigger move event after toggle to ensure current text of focusValueTextItem will change
        c = self.cursor()
        c.setPos(c.pos().x()+1, c.pos().y())
        c.setPos(c.pos().x()-1, c.pos().y())
        scope.rightDock.widget().update()

    def toggleAnimatable(self):
        if self.animationOptions() == QChart.NoAnimation:
            self.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self.setAnimationOptions(QChart.NoAnimation)

    def toggleProperties(self):
        if scope.rightDock.isVisible():
            scope.rightDock.hide()
        else:
            scope.rightDock.show()

    def toggleLeftWidget(self):
        if scope.leftDock.isVisible():
            scope.leftDock.hide()
        else:
            scope.leftDock.show()

######## Update actions

    def updateChildren(self):
        self.updateAxes()

    def scaleChangedFun(self):
        print("scaleChanged")

    def geometryChangedFun(self):
        print("geometryChanged")

    def updateAxisExtremes(self):
        # self.minY = min(min(x) for x in self.ydata)
        # self.maxY = max(max(x) for x in self.ydata)
        if len([serie for serie in self.series() if serie.isVisible()]) > 0:
            minY = min([serie.min() for serie in self.series() if serie.isVisible()])
            maxY = max([serie.max() for serie in self.series() if serie.isVisible()])
            if minY == self.minY and maxY == self.maxY:
                # The axes does not need to be updated
                return False

            self.minY = minY
            self.maxY = maxY

        else:
            self.minY = -10
            self.maxY = 10
        
        return True

    def updateAxes(self):
        if len(self.series()) == 0:
            # Return if series not exist in the chart
            return

        # IDEA: make a setting to turn on/edit 10% Y reserve
        if not self.updateAxisExtremes():
            # If the update was not necessary, do not recreate the axes
            return

        yMinReserve = self.minY/10
        yMaxReserve = self.maxY/10
        base = 10 # round to this number

        axisX = QValueAxis()
        axisY = QValueAxis()
        if self.series()[0].attachedAxes():
            axisX = self.series()[0].attachedAxes()[0]
            axisY = self.series()[0].attachedAxes()[1]

        if self.minY <= 0:
            axisY.setMin(int(base * math.floor(float(self.minY + yMinReserve)/base)))
        else:
            axisY.setMin(0)
        if self.maxY >= 0:
            axisY.setMax(int(base * math.ceil(float(self.maxY + yMaxReserve)/base)))
        else:
            axisY.setMax(0)

        axisX.setRange(self.series()[0].getStart(), self.series()[0].getEnd())
        axisX.hide()

        for serie in self.series():
            if len(serie.attachedAxes()) == 0:
                self.setAxisX(axisX, serie)
                self.setAxisY(axisY, serie)
