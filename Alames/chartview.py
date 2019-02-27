import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

from Alames.config.keymaps import chartviewkeymap

from Alames import scope

class View(QChartView):
    """
    Purpose: displaying and interacting with the rendered QChart
    Creates a widget inside MainWindow which is shared for max 3 widgets
    An object from this class is created in Chart
    """

    _shortcuts = []

    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.setMouseTracking(True)
        self.setInteractive(True)
        self.setRubberBand(self.HorizontalRubberBand)
        self._setupShortcuts()

######## Shortcut binding

    def _setupShortcuts(self):
        for key, method in chartviewkeymap.keydict.items():
            self._shortcuts.append(QShortcut(QtGui.QKeySequence(key), self, getattr(chartviewkeymap, method)))

######## overrides

    def setChart(self, chart):
        super(View, self).setChart(chart)
        scope.rightDock.widget().setChart(chart)
        scope.leftDock.widget().setChart(chart)
        self._createTrackingTools()

######## Init - tracking tools setup

    def _createTrackingTools(self):
        self.focusLine = QGraphicsLineItem(0, 0, 0, 10, self.chart())
        focusPen = QtGui.QPen()
        focusPen.setWidthF(1)
        focusPen.setStyle(QtCore.Qt.DashLine)
        focusPen.setColor(QtGui.QColor("#999999"))
        self.focusLine.setPen(focusPen)
        self.focusLine.setZValue(1500)

        self.focusValueTextItem = QGraphicsTextItem(self.chart())
        self.focusValueTextItem.setScale(1.5)
        self.focusValueTextItem.setZValue(100)
        self.focusValueTextItem.setDefaultTextColor(QtGui.QColor("#333333"))

######## Actions

    def saveToFile(self):
        pixmap = self.grab()
        filename = scope.window.getSaveFile("Images (*.png *.jpg)")
        if filename == None:
            return

        result = pixmap.save(filename)
        if result:
            scope.log("Render saved successfully to " + filename)
        else:
            scope.log("Render save failec to " + filename)


    def renderToFile(self, filename):
        pixmap = self.grab()
        return pixmap.save(filename)

######## Event handlers

    def mouseMoveEvent(self, event):
        super(View, self).mouseMoveEvent(event)
        if not self.focusLine.isVisible(): self.focusLine.show()
        if not self.focusValueTextItem.isVisible(): self.focusValueTextItem.show()

        self.focusValueTextItem.setPos(event.x(), event.y())

        xVal = self.chart().mapToValue(QtCore.QPointF(event.x(), 0), self.chart().getDummyQSerie()).x()
        if xVal < 0 or xVal >= self.chart().getEnd():
            # When the end of the chart is reached
            self.focusValueTextItem.hide()
            self.focusLine.hide()
            return

        html = str(self.chart().getXData()[round(xVal)]) + "<br>"
        for serie in self.chart().series():
            if serie.isVisible():
                html += "<font color=\"" + serie.color().name() + "\">" + "{0:.3f}<br>".format(self.chart().getYData(serie.property("number"))[round(xVal)])
        self.focusValueTextItem.setHtml(html)

        focusLineX = self.chart().mapToPosition(QtCore.QPointF(round(xVal), 0), self.chart().getDummyQSerie()).x()
        self.focusLine.setPos(focusLineX, 0)

    def leaveEvent(self, event):
        super(View, self).leaveEvent(event)
        # QApplication.restoreOverrideCursor()
        if self.chart().series():
            self.focusLine.hide()
            self.focusValueTextItem.hide()

    def enterEvent(self, event):
        super(View, self).enterEvent(event)
        # QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def keyPressEvent(self, event):
        super(View, self).keyPressEvent(event)
        key = event.text()
        if key in ["1","2","3","4","5","6","7","8","9"]:
            self.chart().toggleSerieVisiblity(key)

    def mousePressEvent(self, event):
        super(View, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.MiddleButton:
            self.chart().zoomReset()

    def mouseReleaseEvent(self, event):
        ######## set range values to left widget
        super(View, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton or event.button() == QtCore.Qt.RightButton:
            scope.leftDock.widget().updateValuesFromChart()

    def wheelEvent(self, event):
        super(View, self).wheelEvent(event)
        self.chart().scroll((event.angleDelta().y()/120)*self.chart().getScrollSpeed(), 0)
        scope.rightDock.widget().update()


    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        line = self.focusLine.line()
        line.setLength(self.height())
        self.focusLine.setLine(line)
