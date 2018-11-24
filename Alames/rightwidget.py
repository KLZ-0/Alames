import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

from Alames import rightwidgetsection

class RightWidget(QWidget): # TODO: Reformat to QDockWidget
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """
    def __init__(self, parent):
        super(RightWidget, self).__init__(parent)
        self.setLayout(QFormLayout(self))
        self.setupCurveSettings()

######## Widget construction at init

    def setupCurveSettings(self):
        self.sections = []

        for serie in self.parent().chart.series():
            self.sections.append(rightwidgetsection.RightWidgetSection(self, serie))
            self.layout().addWidget(self.sections[-1])

######## Update Actions

    def updateVisibleBoxes(self):
        for section in self.sections:
            section.updateVisibleBox()

    def updateSections(self):
        for section in self.sections:
            section.updateAll()

######## Event handlers

    def showEvent(self, event):
        super(RightWidget, self).showEvent(event)
        self.updateSections()

    def resizeEvent(self, event):
        super(RightWidget, self).resizeEvent(event)

    def keyPressEvent(self, event):
        self.parent().chart.chart_view.keyPressEvent(event)
