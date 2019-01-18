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
from Alames import chartlineseries

class Chart(QChart, chartmodifier.ChartModifier):
    """
    Purpose: setup and modify the QChart
    Manages the charting subsystem consisting of the ChartView, Properties and BottomWidget.
    Initializes the required objects as its own properties
    """
    ydata = []
    xdata = []

    def __init__(self):
        super(Chart, self).__init__()

######## Setup

    def constructChart(self, fileName):
        self.setAcceptHoverEvents(True)

        self.loadCSV(fileName)
        self.fillSeries()
        self.fillChart()
        self.updateAxes()

    def loadCSV(self, lFileName):
        self.ydata = []
        self.xdata = []

        if lFileName.endswith(".csv.xz"):
            try:
                lFileName = lzma.open(lFileName) # file name or object
            except lzma.LZMAError:
                scope.errorPopup("LZMA decompression failed - damaged xz file")

        f = pandas.read_csv(lFileName)
        csv = f.values
        self.columnNames = f.columns

        for i in range(len(csv[0])-1):
            self.ydata.append([])
        for row in csv:
            self.xdata.append(row[0])
            for i in range(len(row)-1):
                self.ydata[i].append(row[i+1])

    def fillSeries(self):
        self.qseries = []
        for i in range(len(self.ydata)):
            self.qseries.append(chartlineseries.ChartLineSeries(self.ydata[i]))

            # self.qseries[-1].setUseOpenGL(True)
            # IDEA: make a setting to turn off automatic header detection
            self.qseries[i].setName(str(i+1) + " - " + self.columnNames[i+1])
            # self.qseries[i].setName(str(i+1))

    def fillChart(self):
        for serie in self.qseries:
            self.addSeries(serie)

######## Getters

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

######## Setters

    def setRange(self, start, end):
        for serie in self.series():
            serie.setRange(start, end)
        self.updateAxes()

######## View modifiers

    def setZoom(self, start, end):
        firstPoint = self.mapToPosition(QtCore.QPoint(start, self.series()[0].getPoint(start).y()), self.series()[0])
        lastPoint = self.mapToPosition(QtCore.QPoint(end, self.series()[0].getPoint(end).y()), self.series()[0])
        area = self.plotArea()
        self.zoomIn(QtCore.QRectF(firstPoint.x(), area.y(), lastPoint.x() - firstPoint.x(), area.height()))

######## Toggle actions

    def toggleSerieVisiblity(self, key):
        if int(key) > len(self.qseries): return
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
