import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np
import math

import chart_view
import properties

class Chart:
    def __init__(self):
        pass

    def constructChart(self, fileName, app):
        self.chart = QChart()
        self.chart.setAcceptHoverEvents(True)
        # IDEA: Set as settings animatable
        # self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart_view = chart_view.View(self.chart, self, app)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.chart_view.setRubberBand(self.chart_view.HorizontalRubberBand)

        self.loadCSV(fileName)
        self.fillSeries()
        self.fillChart()
        self.createAxes()
        self.createPropertyWidget()

    def loadCSV(self, lFileName):
        self.ydata = []
        self.xdata = []

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
        self.series = []
        for i in range(len(self.ydata)):
            self.series.append(QLineSeries())
            # self.series[-1].setUseOpenGL(True)

            for u in range(len(self.xdata)):
                self.series[i].append(u, self.ydata[i][u])
            # IDEA: make a setting to turn off automatic header detection
            self.series[i].setName(str(i+1) + " - " + self.columnNames[i+1])
            # self.series[i].setName(str(i+1))

    def fillChart(self):
        for serie in self.series:
            self.chart.addSeries(serie)

    def createAxes(self):
        # NOTE: not adaptive > each curve has the same axis with the max value from the entire file
        minValue = min(min(x) for x in self.ydata)
        maxValue = max(max(x) for x in self.ydata)

        # IDEA: make a setting to turn on/edit 10% Y reserve
        yMinReserve = minValue/10
        yMaxReserve = maxValue/10
        base = 10 # round to this number

        axisY = QValueAxis()
        if minValue <= 0:
            axisY.setMin(int(base * math.floor(float(minValue + yMinReserve)/base)))
        else:
            axisY.setMin(0)
        if maxValue >= 0:
            axisY.setMax(int(base * math.ceil(float(maxValue + yMaxReserve)/base)))
        else:
            axisY.setMax(0)

        for i in range(len(self.ydata)):
            self.chart.setAxisY(axisY, self.series[i])

    def createPropertyWidget(self):
        self.propertyWidget = properties.PropertyWidget(self)
        self.propertyWidget.setGeometry(self.width()/6*5, self.propertiesBorder, self.width()/6-self.propertiesBorder, self.height()-2*self.propertiesBorder)

    def toggleSerieVisiblity(self, key):
        if int(key) > len(self.series): return
        if self.chart.series()[int(key) - 1].isVisible():
            self.chart.series()[int(key) - 1].hide()
        else:
            self.chart.series()[int(key) - 1].show()

        # Trigger move event after toggle to ensure current text of focusValueTextItem will change
        c = self.cursor()
        c.setPos(c.pos().x()+1, c.pos().y())
        c.setPos(c.pos().x()-1, c.pos().y())

    def toggleAnimatable(self, key):
        if self.chart.animationOptions() == QChart.NoAnimation:
            self.chart.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self.chart.setAnimationOptions(QChart.NoAnimation)

    def toggleProperties(self):
        if self.propertyWidget.isVisible():
            self.propertyWidget.hide()
            self.chart_view.setGeometry(0, 0, self.width(), self.height())
        else:
            self.propertyWidget.show()
            self.chart_view.setGeometry(0, 0, self.width()/6*5, self.height())
