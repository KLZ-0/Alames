import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

from Alames.generated import ui_rightwidget

from Alames import rightwidgetsection

class RightWidget(QWidget, ui_rightwidget.Ui_RightWidget): # TODO: Reformat to QDockWidget
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """
    def __init__(self, parent=None):
        super(RightWidget, self).__init__(parent)
        self.chart = None
        self.sections = []
        # self.setup()

######## Widget setup

    def setChart(self, chart):
        """
        Args: (Chart chart)
        chart - chart to get data from
        """
        self.chart = chart
        self.setup()

    def setup(self):
        self.setLayout(QFormLayout(self))
        for serie in self.chart.series():
            self.sections.append(rightwidgetsection.RightWidgetSection(self, serie))
            self.layout().addWidget(self.sections[-1]) # FIXME: Add to layout
            # print(self.parent().rightWidget.objectName(), self.widget())

######## Update Actions

    def update(self):
        self.updateSections()

    def updateSections(self):
        for section in self.sections:
            section.update()

######## Event handlers

    def showEvent(self, event):
        super(RightWidget, self).showEvent(event)
        # self.updateSections() # FIXME: try: except:
