import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis
import pandas
import numpy as np
import math
import lzma

from Alames import chartview
from Alames import rightwidget
from Alames import leftwidget
from Alames import bottomwidget
from Alames import chartmodifier
from Alames import chartlineseries

class ChartSetup:
    """Convenience class inherited by Chart for managing initial setup of the chart"""
    def constructChart(self, fileName, app):
        self.setAcceptHoverEvents(True)
        # IDEA: Set as settings animatable
        # self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chartView = chartview.View(self, self.parent, app)
        # self.chartView = self.parent.chartView
        # self.chartView.setChart(self.parent.chart)
        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.chartView.setRubberBand(self.chartView.HorizontalRubberBand)

        self.loadCSV(fileName)
        self.fillSeries()
        self.fillChart()
        self.updateAxes()
        self.createBottomWidget()
        self.createSideWidgets()

        self.chartView.show()
        self.chartView.setGeometry(self.parent.contentsRect())

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
            self.qseries.append(chartlineseries.ChartLineSeries(self.ydata[i]))
            # self.qseries[-1].setUseOpenGL(True)

            # IDEA: make a setting to turn off automatic header detection
            self.qseries[i].setName(str(i+1) + " - " + self.columnNames[i+1])
            # self.qseries[i].setName(str(i+1))

    def fillChart(self):
        for serie in self.qseries:
            self.addSeries(serie)

    def createSideWidgets(self):
        self.propertyWidget = rightwidget.RightWidget(self.parent)
        self.propertyWidget.setGeometry(self.parent.width()/6*5,
                                        self.propertiesBorder,
                                        self.parent.width()/6-self.propertiesBorder,
                                        self.parent.height()-2*self.propertiesBorder - self.bottomWidget.height())
        self.leftWidget = leftwidget.LeftWidget(self.parent)
        self.leftWidget.setGeometry(    self.propertiesBorder,
                                        self.propertiesBorder,
                                        self.parent.width()/6-self.propertiesBorder,
                                        self.parent.height()-2*self.propertiesBorder - self.bottomWidget.height())

    def createBottomWidget(self):
        self.bottomWidget = bottomwidget.BottomWidget(self.parent)
        childrenHeight = sum([child.height() for child in self.bottomWidget.children()])
        self.bottomWidget.setGeometry(  self.propertiesBorder,
                                        self.parent.height() - self.propertiesBorder*2 - childrenHeight,
                                        self.parent.width() - 2*self.propertiesBorder,
                                        childrenHeight+2*self.propertiesBorder)
