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
from Alames import rightwidget
from Alames import leftwidget
from Alames import chartmodifier
from Alames import chartlineseries

class ChartSetup:
    """Convenience class inherited by Chart for managing initial setup of the chart"""
    def constructChart(self, fileName):
        self.setAcceptHoverEvents(True)
        # IDEA: Set as settings animatable
        # self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # self.chartView = chartview.View(self, self.parent, app)

        self.loadCSV(fileName)
        self.fillSeries()
        self.fillChart()
        self.updateAxes()
        self.createBottomWidget()
        self.createSideWidgets()

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

    def createSideWidgets(self):
        # self.rightWidget = rightwidget.RightWidget(self.parent)
        # self.leftWidget = leftwidget.LeftWidget(self.parent)
        pass

    def createBottomWidget(self):
        # self.bottomWidget = bottomwidget.BottomWidget(self.parent)
        # childrenHeight = sum([child.height() for child in self.bottomWidget.children()])
        pass
