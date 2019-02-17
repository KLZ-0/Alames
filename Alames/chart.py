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

        self.updateAxes()

    def loadCSV(self, lFileName):
        if lFileName.endswith(".csv.xz"):
            try:
                lFileName = lzma.open(lFileName) # file name or object
            except lzma.LZMAError:
                scope.errorPopup("LZMA decompression failed - damaged xz file")

        f = pandas.read_csv(lFileName)
        csv = f.values
        
        self.selectionDataHolder.setColumnNames(f.columns)
        self.selectionDataHolder.setDataFromRows(csv)
        self.overallDataHolder.setColumnNames(f.columns)
        self.overallDataHolder.setDataFromRows(csv)

######## Signal handlers

    def onSelectionChange(self, range):
        # call in ....connect(self.onSelectionChange)
        # self.selectionDataHolder.update(range)
        pass

######## Getters

    def getXData(self):
        return self.selectionDataHolder.XData()

    def getYData(self):
        return self.selectionDataHolder.YData()

    def getRange(self):
        try:
            return self.series()[0].getStart(), self.series[0].getEnd()
        except IndexError:
            return 0

    def getStart(self):
        try:
            return self.series()[0].getStart()
        except IndexError:
            return 0

    def getEnd(self):
        try:
            return self.series()[0].getEnd()
        except IndexError:
            return 0

######## Series modifier

    def setRange(self, start, end):
        self.selectionDataHolder.setRange(start, end)
        self.resetZoom()
        scope.window.updateChildren()

######## View modifiers

    def setZoom(self, start, end):
        firstPoint = self.mapToPosition(QtCore.QPoint(start, 0), self.series()[0])
        lastPoint = self.mapToPosition(QtCore.QPoint(end, 0), self.series()[0])
        area = self.plotArea()
        self.zoomIn(QtCore.QRectF(firstPoint.x(), area.y(), lastPoint.x() - firstPoint.x(), area.height()))

    def resetZoom(self):
        self.setZoom(self.getStart(), self.getEnd())

    def zoomReset(self):
        """Override the inherited method"""
        self.resetZoom()

######## Toggle actions

    def toggleSerieVisiblity(self, key):
        if int(key) > self.selectionDataHolder.getLen():
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

    def toggleAnimatable(self, key):
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
        self.minY = min(serie.min() for serie in self.series())
        self.maxY = max(serie.max() for serie in self.series())

    def updateAxes(self):
        self.updateAxisExtremes()
        # IDEA: make a setting to turn on/edit 10% Y reserve
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
