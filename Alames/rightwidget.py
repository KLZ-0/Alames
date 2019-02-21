import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

from Alames.generated.ui_rightwidget import Ui_RightWidget

from Alames import rightwidgetsection

class RightWidget(QWidget, Ui_RightWidget):
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """

    DEFAULT_VISIBLE_SECTION_NUM = 0

    _sections = []

    loaded = QtCore.pyqtSignal()
    sectionUpdated = QtCore.pyqtSignal()

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
        i = 0
        for serie in self.chart.series():
            self._sections.append(rightwidgetsection.RightWidgetSection(self, serie))
            self._sections[-1].updated.connect(self.sectionUpdated.emit)
            # Show first n sections
            if i < self.DEFAULT_VISIBLE_SECTION_NUM: 
                self._sections[-1].setProperty("visible_by_default", True)
                self._sections[-1].show()
            else:
                self._sections[-1].setProperty("visible_by_default", False)
                self._sections[-1].hide()
                
            self.scrollArea.widget().layout().addWidget(self._sections[-1])
            # print(self.parent().rightWidget.objectName(), self.widget())
            i += 1

        self.loaded.emit()

######## External section management

    def getSectionLen(self):
        return len(self._sections)

    def getSectionName(self, num):
        return self._sections[num].getName()

    def isVisibleSection(self, num):
        return self._sections[num].isVisible()
        
    def isVisibleSectionByDefault(self, num):
        return self._sections[num].property("visible_by_default")

    def isVisibleSectionSerie(self, num):
        return self._sections[num].serie.isVisible()

    def setVisibleSection(self, num, state):
        self._sections[num].setVisible(state)

######## Update Actions

    def update(self):
        self.updateSections()
        self.sectionUpdated.emit()

    def updateSections(self):
        for section in self._sections:
            section.update()

######## Event handlers

    def showEvent(self, event):
        super(RightWidget, self).showEvent(event)
        # self.updateSections() # FIXME: try: except:
