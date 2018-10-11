import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

class PropertyWidget(QWidget):
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """
    def __init__(self, parent):
        super(PropertyWidget, self).__init__(parent)

        self.setupCurveSettings()

######## Widget construction at init

    def setupCurveSettings(self):

        self.nOfLinesPerSerie = 3
        self.seriesNameLabels = []
        self.seriesNameLineEdits = []
        self.seriesColorLabels = []
        self.seriesColorValueLabels = []
        self.serieColorPickButtons = []
        self.hrLines = []

        for serie in self.parent().chart.series():
            self.seriesNameLabels.append(QLabel("Name: ", self))
            self.seriesNameLineEdits.append(QLineEdit(serie.name(), self))
            self.seriesNameLineEdits[-1].editingFinished.connect(self.applySettings)
            self.seriesColorLabels.append(QLabel("Color: ", self))
            self.seriesColorValueLabels.append(QLabel(serie.color().name(), self))
            self.serieColorPickButtons.append(QPushButton(self))
            pixRect = QtGui.QPixmap(64,64)
            pixRect.fill(serie.color())
            self.serieColorPickButtons[-1].setIcon(QtGui.QIcon(pixRect))
            # self.serieColorPickButtons[-1].setIcon(QtGui.QIcon("icons/adjust.png"))
            self.serieColorPickButtons[-1].pressed.connect(self.pickSerieColor)
            self.hrLines.append(QLabel("<hr>", self))

######## Actions

    def pickSerieColor(self):
        for i in range(len(self.serieColorPickButtons)):
            if self.serieColorPickButtons[i].isDown():
                color = QColorDialog.getColor(QtGui.QColor(self.seriesColorValueLabels[i].text()))
                self.seriesColorValueLabels[i].setText(color.name())
                self.applySettings()

    def applySettings(self):
        for i in range(len(self.parent().chart.series())):
            serie = self.parent().chart.series()[i]
            serie.setName(self.seriesNameLineEdits[i].text())
            try:
                serie.setColor(QtGui.QColor(self.seriesColorValueLabels[i].text()))
                pixRect = QtGui.QPixmap(64,64)
                pixRect.fill(serie.color())
                self.serieColorPickButtons[i].setIcon(QtGui.QIcon(pixRect))
            except ValueError:
                pass

######## Event handlers

    def showEvent(self, event):
        super(PropertyWidget, self).showEvent(event)
        for i in range(len(self.parent().chart.series())):
            self.seriesNameLineEdits[i].setText(self.parent().chart.series()[i].name())
            self.seriesColorValueLabels[i].setText(self.parent().chart.series()[i].color().name())
            pixRect = QtGui.QPixmap(64,64)
            pixRect.fill(self.parent().chart.series()[i].color())
            self.serieColorPickButtons[i].setIcon(QtGui.QIcon(pixRect))

    def resizeEvent(self, event):
        super(PropertyWidget, self).resizeEvent(event)
        for i in range(len(self.seriesNameLabels)):
            offset = i*self.nOfLinesPerSerie
            currentLine = 0
            self.seriesNameLabels[i].setGeometry(0, (offset+currentLine)*self.seriesNameLineEdits[i].height(), self.width()/3, self.seriesNameLineEdits[i].height())
            self.seriesNameLineEdits[i].setGeometry(self.width()/3, (offset+currentLine)*self.seriesNameLineEdits[i].height(), self.width()/1.5, self.seriesNameLineEdits[i].height())

            currentLine += 1
            self.seriesColorLabels[i].setGeometry(0, (offset+currentLine)*self.seriesNameLineEdits[i].height(), self.width()/3, self.seriesNameLineEdits[i].height())
            self.seriesColorValueLabels[i].setGeometry(self.width()/3, (offset+currentLine)*self.seriesNameLineEdits[i].height(), self.width()/1.5, self.seriesNameLineEdits[i].height())
            self.serieColorPickButtons[i].setGeometry(self.width()-self.seriesColorValueLabels[i].height(), (offset+currentLine)*self.seriesNameLineEdits[i].height(), self.seriesColorValueLabels[i].height(), self.seriesColorValueLabels[i].height())

            currentLine += 1
            self.hrLines[i].setGeometry(0, (offset+currentLine)*self.seriesNameLineEdits[i].height(), self.width(), self.seriesNameLineEdits[i].height())
