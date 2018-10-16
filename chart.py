import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np
import math
import lzma

import chart_view
import properties
import bottom_widget
import chart_modifier

class Chart(QChart, chart_modifier.Modifier):
    """
    Purpose: setup and modify the QChart
    Manages the charting subsystem consisting of the ChartView, Properties and BottomWidget.
    Initializes the required objects as its own properties
    """
    def __init__(self, parent):
        super(Chart, self).__init__()
        self.parent = parent
        self.propertiesBorder = 8

######## Chart construction

    def constructChart(self, fileName, app):
        self.setAcceptHoverEvents(True)
        # IDEA: Set as settings animatable
        # self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart_view = chart_view.View(self, self.parent, app)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.chart_view.setRubberBand(self.chart_view.HorizontalRubberBand)

        self.loadCSV(fileName)
        self.fillSeries()
        self.fillChart()
        self.updateAxes()
        self.createPropertyWidget()
        self.createBottomWidget()

        self.chart_view.show()
        self.chart_view.setGeometry(self.parent.contentsRect())

    def loadCSV(self, lFileName):
        self.ydata = []
        self.xdata = []

        if lFileName.endswith(".csv.xz"):
            lFileName = lzma.open(lFileName) # file name or object

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
            self.qseries.append(QLineSeries())
            # self.qseries[-1].setUseOpenGL(True)

            for u in range(len(self.xdata)):
                self.qseries[i].append(u, self.ydata[i][u])
            # IDEA: make a setting to turn off automatic header detection
            self.qseries[i].setName(str(i+1) + " - " + self.columnNames[i+1])
            # self.qseries[i].setName(str(i+1))

    def fillChart(self):
        for serie in self.qseries:
            self.addSeries(serie)

    def createPropertyWidget(self):
        self.propertyWidget = properties.PropertyWidget(self.parent)
        self.propertyWidget.setGeometry(self.parent.width()/6*5, self.propertiesBorder, self.parent.width()/6-self.propertiesBorder, self.parent.height()-2*self.propertiesBorder)

    def createBottomWidget(self):
        self.bottomWidget = bottom_widget.BottomWidget(self.parent)
        self.bottomWidget.setGeometry(  self.propertiesBorder,
                                        self.parent.height() - self.propertiesBorder*2 - self.bottomWidget.scrollBar.height(),
                                        self.parent.width() - 2*self.propertiesBorder,
                                        self.bottomWidget.scrollBar.height()+2*self.propertiesBorder)

######## Update actions

    def updateAxisExtremes(self):
        # NOTE: not adaptive > each curve has the same axis with the max value from the entire file
        self.minY = min(min(x) for x in self.ydata)
        self.maxY = max(max(x) for x in self.ydata)

    def updateAxes(self):
        self.updateAxisExtremes()
        # IDEA: make a setting to turn on/edit 10% Y reserve
        yMinReserve = self.minY/10
        yMaxReserve = self.maxY/10
        base = 10 # round to this number

        axisY = QValueAxis()
        if self.series()[0].attachedAxes():
            axisY =  self.series()[0].attachedAxes()[0]
        if self.minY <= 0:
            axisY.setMin(int(base * math.floor(float(self.minY + yMinReserve)/base)))
        else:
            axisY.setMin(0)
        if self.maxY >= 0:
            axisY.setMax(int(base * math.ceil(float(self.maxY + yMaxReserve)/base)))
        else:
            axisY.setMax(0)

        for serie in self.series():
            if len(serie.attachedAxes()) == 0:
                self.setAxisY(axisY, serie)

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

    def toggleAnimatable(self, key):
        if self.animationOptions() == QChart.NoAnimation:
            self.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self.setAnimationOptions(QChart.NoAnimation)

    def toggleProperties(self):
        if self.propertyWidget.isVisible():
            self.propertyWidget.hide()
            self.chart_view.setGeometry(0, 0, self.parent.width(), self.chart_view.height())
        else:
            self.propertyWidget.show()
            self.chart_view.setGeometry(0, 0, self.parent.width()/6*5, self.chart_view.height())

    def toggleBottomWidget(self):
        if self.bottomWidget.isVisible():
            self.bottomWidget.hide()
            self.chart_view.setGeometry(0, 0, self.chart_view.width(), self.parent.height())
        else:
            self.bottomWidget.show()
            self.chart_view.setGeometry(0, 0, self.chart_view.width(), self.parent.height() - self.bottomWidget.height())
