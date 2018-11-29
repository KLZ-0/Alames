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
from Alames import chartsetup

class Chart(QChart, chartmodifier.ChartModifier, chartsetup.ChartSetup):
    """
    Purpose: setup and modify the QChart
    Manages the charting subsystem consisting of the ChartView, Properties and BottomWidget.
    Initializes the required objects as its own properties
    """
    def __init__(self):
        super(Chart, self).__init__()

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

######## View modifiers

    def setRange(self, start, end):
        for serie in self.series():
            serie.setRange(start, end)
        self.updateAxes()

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
        scope.rightDock.widget().updateVisibleBoxes()

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

    def toggleBottomWidget(self):
        br = self.chartView.geometry()
        widgetHeight = self.bottomWidget.height()
        if self.bottomWidget.isVisible():
            self.bottomWidget.hide()
            self.chartView.setGeometry(br.x(), br.y(), br.width(), br.height()+widgetHeight)
        else:
            self.bottomWidget.show()
            self.chartView.setGeometry(br.x(), br.y(), br.width(), br.height()-widgetHeight)

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
