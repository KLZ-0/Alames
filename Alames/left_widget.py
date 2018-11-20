import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

class LeftWidget(QWidget):
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """
    def __init__(self, parent):
        super(LeftWidget, self).__init__(parent)
        self.padding = 5

        self.infoLabel = QLabel("Text", self)

        self.startBox = QSpinBox(self)
        self.endBox = QSpinBox(self)
        self.startBox.setMinimum(self.parent().chart.getStart())
        self.startBox.setMaximum(self.parent().chart.getEnd()-1)
        self.startBox.valueChanged.connect(self.updateRange)
        self.endBox.setMinimum(self.parent().chart.getStart()+1)
        self.endBox.setMaximum(self.parent().chart.getEnd())
        self.endBox.valueChanged.connect(self.updateRange)

        self.resetButton = QPushButton("Reset", self)
        self.resetButton.clicked.connect(self.resetRange)

        self.updateAll()

######## Update Actions

    def updateRange(self):
        self.parent().chart.setZoom(self.startBox.value(), self.endBox.value())

    def recalculatePadding(self):
        padding = self.padding
        for child in self.children():
            child.setGeometry(child.x() + padding, child.y() + padding, child.width() - 2*padding, child.height() - 2*padding)

    def updateAll(self):
        self.infoLabel.setText("Range:")
        self.startBox.setValue(self.parent().chart.getStart())
        self.endBox.setValue(self.parent().chart.getEnd())

    def resetRange(self):
        self.startBox.setValue(self.parent().chart.series()[0].getStart())
        self.endBox.setValue(self.parent().chart.series()[0].getEnd())

    def updateValuesFromChart(self):
        plotArea = self.parent().chart.plotArea()
        startX = self.parent().chart.mapToValue(QtCore.QPointF(plotArea.x(), plotArea.y()), self.parent().chart.series()[0]).x()
        endX = self.parent().chart.mapToValue(QtCore.QPointF(plotArea.x() + plotArea.width(), plotArea.y()), self.parent().chart.series()[0]).x()
        self.startBox.setValue(round(startX))
        self.endBox.setValue(round(endX))

######## Event handlers

    def showEvent(self, event):
        super(LeftWidget, self).showEvent(event)
        # self.updateSections()

    def resizeEvent(self, event):
        super(LeftWidget, self).resizeEvent(event)
        self.infoLabel.setGeometry(0, 0, self.width(), self.infoLabel.height()*2)
        self.startBox.setGeometry(0, self.infoLabel.height(), self.width()/2, self.startBox.height()+2*self.padding)
        self.endBox.setGeometry(self.width()/2, self.infoLabel.height(), self.width()/2, self.endBox.height()+2*self.padding)
        self.resetButton.setGeometry(0, self.endBox.y() + self.endBox.height(), self.width(), self.resetButton.height())
        self.recalculatePadding()

    def keyPressEvent(self, event):
        self.parent().chart.chart_view.keyPressEvent(event)
