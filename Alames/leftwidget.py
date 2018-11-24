import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

class LeftWidget(QDockWidget):
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """
    def __init__(self, parent):
        super(LeftWidget, self).__init__(parent)
        self.chart = None

        self.infoLabel = QLabel("Text", self)

        self.startBox = QSpinBox(self)
        self.endBox = QSpinBox(self)
        self.startBox.valueChanged.connect(self.updateRange)
        self.endBox.valueChanged.connect(self.updateRange)
        self.resetButton = QPushButton("Reset", self)
        self.resetButton.clicked.connect(self.resetRange)

        # self.setupBoxes()
        # self.updateAll()

######## Update Actions

    def setChart(self, chart):
        """
        Args: (Chart chart)
        chart - chart to get data from
        """
        self.chart = chart
        self.setupRanges()

    def setupRanges(self): # FIXME: Call to parent
        """
        Args: ()
        Setup box ranges
        """
        self.endBox.setMinimum(self.chart.getStart()+1)
        self.endBox.setMaximum(self.chart.getEnd())
        self.startBox.setMinimum(self.chart.getStart())
        self.startBox.setMaximum(self.chart.getEnd()-1)

    def updateRange(self):
        """
        Args: ()
        Update chart zoom
        """
        self.chart.setZoom(self.startBox.value(), self.endBox.value())

    def updateAll(self):
        """
        Args: ()
        Update all values of Ui elements
        """
        self.infoLabel.setText("Range:")
        self.startBox.setValue(self.chart.getStart())
        self.endBox.setValue(self.chart.getEnd())

    def resetRange(self):
        """
        Args: ()
        Reset range of chart and value of Ui elements
        """
        self.startBox.setValue(self.chart.getStart())
        self.endBox.setValue(self.chart.getEnd())

    def updateValuesFromChart(self):
        """
        Args: ()
        Update box values after e.g. rubberband zoom change
        """
        plotArea = self.chart.plotArea()
        startX = self.chart.mapToValue(QtCore.QPointF(plotArea.x(), plotArea.y()), self.chart.series()[0]).x()
        endX = self.chart.mapToValue(QtCore.QPointF(plotArea.x() + plotArea.width(), plotArea.y()), self.chart.series()[0]).x()
        self.startBox.setValue(round(startX))
        self.endBox.setValue(round(endX))

######## Event handlers

    def showEvent(self, event):
        super(LeftWidget, self).showEvent(event)
        # self.updateSections()

    # def keyPressEvent(self, event): # FIXME: Set MainWindow grab key events
    #     self.parent().chart.chart_view.keyPressEvent(event)
