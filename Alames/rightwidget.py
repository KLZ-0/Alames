import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

from Alames.generated import ui_rightwidget

from Alames import rightwidgetsection

class RightWidget(QWidget, ui_rightwidget.Ui_RightWidget):
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """

    _sections = []

    def __init__(self, parent=None):
        super(RightWidget, self).__init__(parent)
        self.chart = None
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
        self.setupUi(self)
        for serie in self.chart.series():
            self._sections.append(rightwidgetsection.RightWidgetSection(self, serie))
            self.scrollArea.widget().layout().addWidget(self._sections[-1])
            # print(self.parent().rightWidget.objectName(), self.widget())

######## Update Actions

    def update(self):
        self.updateSections()

    def updateSections(self):
        for section in self._sections:
            section.update()

######## Event handlers

    def showEvent(self, event):
        super(RightWidget, self).showEvent(event)
        # self.updateSections() # FIXME: try: except:
