#!/usr/bin/python

import os, sys, platform
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis
from pathlib import Path

from Alames import scope
from Alames.generated.ui_mainwindow import Ui_MainWindow
from Alames.generated import ui_aboutwidget

from Alames.config.keymaps import windowkeymap

from Alames import chart

class Window(QMainWindow, Ui_MainWindow):
    """
    Purpose: setup and modify the QMainWindow
    Manages the whole window except for the charting subsystem which is managed by Chart.
    Initializes Chart as its own property
    """

    _shortcuts = []

    def __init__(self):
        super(Window, self).__init__()
        scope.window = self

        self.setupUi(self)
        self.centralWidget.hide()
        self.rightDock.hide()
        self.leftDock.hide()
        self.rightDock.widget().loaded.connect(self.loaderDock.widget().setup)

        #### Assign scope
        scope.errorPopup = self.errorPopup
        scope.chartView = self.chartView
        scope.rightDock = self.rightDock
        scope.centralWidget = self.centralWidget
        scope.leftDock = self.leftDock
        scope.loaderDock = self.loaderDock

        self.setWindowTitle("Alames")
        self.setAcceptDrops(True)

        self.aboutWidget = QWidget()
        self.aboutWidget.ui = ui_aboutwidget.Ui_AboutWidget()
        self.aboutWidget.ui.setupUi(self.aboutWidget)

        # self.initLabel = QLabel("Drag & Drop a CSV file, or press:\n\nO - to open and load data\n\nS - to draw the file contents into a chart\n\nQ - to quit", self)
        self.initLabel = QLabel("Drag & Drop a CSV file or press O to open one", self)
        self.initLabel.setAlignment(QtCore.Qt.AlignCenter)
        f = self.initLabel.font()
        f.setPointSize(24)
        self.initLabel.setFont(f)

        self._setupShortcuts()

######## Update methods

    def updateChildren(self):
        self.rightDock.widget().update()
        self.leftDock.widget().update()
        self.chartView.chart().updateChildren()

######## Open file methods

    def openFile(self):
        f = self.getOpenFile("CSV files (*.csv *.csv.xz)")
        if f == None:
            return

        self.createChart(f)

    def createChart(self, csvFile):
        if scope.chartView.chart():
            scope.chartView.chart().deleteLater()

        scope.chart = chart.Chart() # FIXME: Two functions
        scope.chart.constructChart(csvFile) # FIXME: Two functions
        scope.chartView.setChart(scope.chart)
        self.initLabel.hide()
        scope.centralWidget.show()
        scope.rightDock.show()
        scope.leftDock.show()

        # send signal to window->phasorWidget to update
        self.phasorView.scene().setData(scope.chart.selectionDataHolder, {"show-current-circle": False, "current-color": "#ff0000", "voltage-color": "#0000ff"})

        # scope.chart.chartView = scope.chartView

        # needed when opening a new file
        self.updateChildren()

    def getOpenFile(self, typeFilter="CSV files (*.csv *.csv.xz)"):
        f = QFileDialog.getOpenFileName(self, "Open..", str(
            Path(__file__).parents[1]), typeFilter)

        # If windows sometimes problems with the encoding happen
        fileName = f[0]
        if platform.uname().system != "Linux":
            fileName = fileName.encode("utf-8").decode("utf-8", "replace")

        # Extract suffixes from filter
        fileSuffixes = f[1][f[1].find("(")+1:f[1].find(")")].split()
        fileSuffixes = [suffix.lstrip("*") for suffix in fileSuffixes]

        # Test if exists
        if not Path(fileName).is_file() or not fileName.endswith(tuple(fileSuffixes)):
            return None

        return fileName

    def getSaveFile(self, typeFilter="Images (*.png *.jpg)"):
        f = QFileDialog.getSaveFileName(self, "Save as..", str(
            Path(__file__).parents[1]), typeFilter)

        # If windows sometimes problems with the encoding happen
        fileName = f[0]
        if platform.uname().system != "Linux":
            fileName = fileName.encode("utf-8").decode("utf-8", "replace")

        # Test whether the returned filename is not empty
        if fileName == "":
            return None

        # Extract suffixes from filter
        fileSuffixes = f[1][f[1].find("(")+1:f[1].find(")")].split()
        fileSuffixes = [suffix.lstrip("*") for suffix in fileSuffixes]

        # If returned filename does not have a suffix, append the first one (the default)
        if not fileName.endswith(tuple(fileSuffixes)):
            fileName += fileSuffixes[0]

        return fileName

    def errorPopup(self, text):
        QErrorMessage(self).showMessage(text)

######## Shortcut binding

    def _setupShortcuts(self):
        for key, method in windowkeymap.keydict.items():
            self._shortcuts.append(QShortcut(QtGui.QKeySequence(key), self, getattr(windowkeymap, method)))

######## Event handlers

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
