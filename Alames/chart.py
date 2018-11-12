import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis
import pandas
import numpy as np
import math
import lzma

from Alames import chart_view
from Alames import properties
from Alames import left_widget
from Alames import bottom_widget
from Alames import chart_modifier
from Alames import chart_lineseries

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
        self.createBottomWidget()
        self.createSideWidgets()

        self.chart_view.show()
        self.chart_view.setGeometry(self.parent.contentsRect())

    def loadCSV(self, lFileName):
        self.ydata = []
        self.xdata = []

        if lFileName.endswith(".csv.xz"):
            try:
                lFileName = lzma.open(lFileName) # file name or object
            except lzma.LZMAError:
                self.parent.errorPopup("LZMA decompression failed - damaged xz file")

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
            self.qseries.append(chart_lineseries.LineSeries(self.ydata[i]))
            # self.qseries[-1].setUseOpenGL(True)

            # IDEA: make a setting to turn off automatic header detection
            self.qseries[i].setName(str(i+1) + " - " + self.columnNames[i+1])
            # self.qseries[i].setName(str(i+1))

    def fillChart(self):
        for serie in self.qseries:
            self.addSeries(serie)

    def createSideWidgets(self):
        self.propertyWidget = properties.PropertyWidget(self.parent)
        self.propertyWidget.setGeometry(self.parent.width()/6*5,
                                        self.propertiesBorder,
                                        self.parent.width()/6-self.propertiesBorder,
                                        self.parent.height()-2*self.propertiesBorder - self.bottomWidget.height())
        self.leftWidget = left_widget.LeftWidget(self.parent)
        self.leftWidget.setGeometry(    self.propertiesBorder,
                                        self.propertiesBorder,
                                        self.parent.width()/6-self.propertiesBorder,
                                        self.parent.height()-2*self.propertiesBorder - self.bottomWidget.height())

    def createBottomWidget(self):
        self.bottomWidget = bottom_widget.BottomWidget(self.parent)
        childrenHeight = sum([child.height() for child in self.bottomWidget.children()])
        self.bottomWidget.setGeometry(  self.propertiesBorder,
                                        self.parent.height() - self.propertiesBorder*2 - childrenHeight,
                                        self.parent.width() - 2*self.propertiesBorder,
                                        childrenHeight+2*self.propertiesBorder)

######## Update actions

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

######## Getters

    def getRange(self):
        return self.series()[0].getStart(), self.series[0].getEnd()

    def getStart(self):
        return self.series()[0].getStart()

    def getEnd(self):
        return self.series()[0].getEnd()

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
        self.propertyWidget.updateVisibleBoxes()

    def toggleAnimatable(self, key):
        if self.animationOptions() == QChart.NoAnimation:
            self.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self.setAnimationOptions(QChart.NoAnimation)

    def toggleProperties(self):
        br = self.chart_view.geometry()
        widgetWidth = self.parent.width()/6
        if self.propertyWidget.isVisible():
            self.propertyWidget.hide()
            self.chart_view.setGeometry(br.x(), br.y(), br.width()+widgetWidth, br.height())
        else:
            self.propertyWidget.show()
            self.chart_view.setGeometry(br.x(), br.y(), br.width()-widgetWidth, br.height())

    def toggleLeftWidget(self):
        br = self.chart_view.geometry()
        widgetWidth = self.parent.width()/6
        if self.leftWidget.isVisible():
            self.leftWidget.hide()
            self.chart_view.setGeometry(br.x()-widgetWidth, br.y(), br.width()+widgetWidth, br.height())
        else:
            self.leftWidget.show()
            self.chart_view.setGeometry(br.x()+widgetWidth, br.y(), br.width()-widgetWidth, br.height())

    def toggleBottomWidget(self):
        br = self.chart_view.geometry()
        widgetHeight = self.bottomWidget.height()
        if self.bottomWidget.isVisible():
            self.bottomWidget.hide()
            self.chart_view.setGeometry(br.x(), br.y(), br.width(), br.height()+widgetHeight)
        else:
            self.bottomWidget.show()
            self.chart_view.setGeometry(br.x(), br.y(), br.width(), br.height()-widgetHeight)
