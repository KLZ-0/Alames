import os, sys, platform
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis
from pathlib import Path

import chart
import chart_view

class Window(QMainWindow):
    """
    Purpose: setup and modify the QMainWindow
    Manages the whole window except for the charting subsystem which is managed by Chart.
    Initializes Chart as its own property
    """
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Alames")
        self.setAcceptDrops(True)

        self.chart = chart.Chart(self)

        # self.initLabel = QLabel("Drag & Drop a CSV file, or press:\n\nO - to open and load data\n\nS - to draw the file contents into a chart\n\nQ - to quit", self)
        self.initLabel = QLabel("Drag & Drop a CSV file or press O to open one", self)
        self.initLabel.setAlignment(QtCore.Qt.AlignCenter)
        f = self.initLabel.font()
        f.setPointSize(24)
        self.initLabel.setFont(f)

        # self.constructChart(op_dir, app)

        self.show()
        self.windowHandle().setScreen(app.screens()[-1])
        self.setGeometry(app.screens()[-1].availableGeometry())
        self.setWindowState(QtCore.Qt.WindowMaximized)

######## Open file methods

    def openFile(self):
        f = self.fileSelect()
        if Path(f).is_file() and (f.endswith(".csv") or f.endswith(".csv.xz")):
            self.createChart(f)

    def createChart(self, csvFile):
        self.chart.constructChart(csvFile, app)
        self.initLabel.hide()

    def fileSelect(self):
        if platform.uname().system == "Linux":
            return QFileDialog.getOpenFileName(self, 'Select CSV file', '/', "CSV files (*.csv *.csv.xz)")[0]
        return QFileDialog.getOpenFileName(self, 'Select CSV file', 'C:', "CSV files (*.csv *.csv.xz)")[0].encode('utf-8').decode('utf-8', 'replace')

    def errorPopup(self, text):
        QErrorMessage(self).showMessage(text)

######## Event handlers

    def keyPressEvent(self, event):
        super(Window, self).keyPressEvent(event)
        key = event.text()
        if "o" in key:
            self.openFile()
        if "q" in key or event.key() == QtCore.Qt.Key_Escape:
            app.exit()
        if event.key() == QtCore.Qt.Key_F12:
            app.aboutQt()

    def dragEnterEvent(self, event):
        super(Window, self).dragEnterEvent(event)
        if event.mimeData().text()[-4:].lower() == ".csv":
            event.acceptProposedAction()

    def dropEvent(self, event):
        super(Window, self).dropEvent(event)
        self.createChart(event.mimeData().text())

    def resizeEvent(self, event):
        self.initLabel.setGeometry(self.contentsRect())

######## Actual start

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Alames")
    # app.setWindowIcon(QtGui.QIcon("icons/main.png"))
    QtGui.QFontDatabase.addApplicationFont("fonts/Gidole-Regular.ttf")
    app.setFont(QtGui.QFont("Gidole"))
    ex = Window()
    sys.exit(app.exec_())
