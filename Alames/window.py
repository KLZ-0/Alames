#!/usr/bin/python

import os, sys, platform
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis
from pathlib import Path

from Alames import scope
from Alames.generated.ui_mainwindow import Ui_MainWindow

from Alames import chart

class Window(QMainWindow, Ui_MainWindow):
    """
    Purpose: setup and modify the QMainWindow
    Manages the whole window except for the charting subsystem which is managed by Chart.
    Initializes Chart as its own property
    """
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.centralWidget.hide()
        self.rightDock.hide()
        self.leftDock.hide()

        #### Assign scope
        scope.errorPopup = self.errorPopup
        scope.chartView = self.chartView
        scope.rightDock = self.rightDock
        scope.centralWidget = self.centralWidget
        scope.leftDock = self.leftDock

        self.setWindowTitle("Alames")
        self.setAcceptDrops(True)

        # self.initLabel = QLabel("Drag & Drop a CSV file, or press:\n\nO - to open and load data\n\nS - to draw the file contents into a chart\n\nQ - to quit", self)
        self.initLabel = QLabel("Drag & Drop a CSV file or press O to open one", self)
        self.initLabel.setAlignment(QtCore.Qt.AlignCenter)
        f = self.initLabel.font()
        f.setPointSize(24)
        self.initLabel.setFont(f)

######## Open file methods

    def openFile(self):
        f = self.fileSelect()
        if Path(f).is_file() and (f.endswith(".csv") or f.endswith(".csv.xz")):
            self.createChart(f)

    def createChart(self, csvFile):
        scope.chart = chart.Chart() # FIXME: Two functions
        scope.chart.constructChart(csvFile) # FIXME: Two functions
        scope.chartView.setChart(scope.chart)
        self.initLabel.hide()
        scope.centralWidget.show()
        scope.rightDock.show()
        scope.leftDock.show()

        # scope.chart.chartView = scope.chartView

    def fileSelect(self):
        if platform.uname().system == "Linux":
            return QFileDialog.getOpenFileName(self, "Select CSV file", str(Path(__file__).parents[1]), "CSV files (*.csv *.csv.xz)")[0]
        return QFileDialog.getOpenFileName(self, "Select CSV file", str(Path(__file__).parents[1]), "CSV files (*.csv *.csv.xz)")[0].encode("utf-8").decode("utf-8", "replace")

    def errorPopup(self, text):
        QErrorMessage(self).showMessage(text)

######## Event handlers

    def keyPressEvent(self, event):
        super(Window, self).keyPressEvent(event)
        key = event.text()
        if "o" in key:
            self.openFile()
        if "q" in key or event.key() == QtCore.Qt.Key_Escape:
            QApplication.exit()
        if event.key() == QtCore.Qt.Key_F12:
            QApplication.aboutQt()

    def dragEnterEvent(self, event):
        super(Window, self).dragEnterEvent(event)
        if event.mimeData().text()[-4:].lower() == ".csv":
            event.acceptProposedAction()

    def dropEvent(self, event):
        super(Window, self).dropEvent(event)
        self.createChart(event.mimeData().text())

    def resizeEvent(self, event):
        super(Window, self).resizeEvent(event)
        self.initLabel.setGeometry(self.contentsRect())