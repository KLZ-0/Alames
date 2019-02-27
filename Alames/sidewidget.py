import os
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

class SideWidget(QWidget):
    """
    Purpose: relative positioning of internal items in a DockWidget
    """

    _setupHappened = False

    def __init__(self, parent=None):
        super(SideWidget, self).__init__(parent)
        self.chart = None

######## Widget setup

    def setChart(self, chart):
        """
        Args: (Chart chart)
        chart - chart to get data from
        """
        self.chart = chart
        self.setup()
        self.update()

    def setup(self):
        """
        Args: ()
        Setup widget Ui elements
        """

        if not self._setupHappened:
            self.setupUi(self)

        self._setupHappened = True

######## Update Actions

    def update(self):
        """
        Args: ()
        Update all values of Ui elements
        """
        pass
