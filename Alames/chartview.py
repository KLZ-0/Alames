import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import pandas
import numpy as np

class View(QChartView):
    """
    Purpose: displaying and interacting with the rendered QChart
    Creates a widget inside MainWindow which is shared for max 3 widgets
    An object from this class is created in Chart
    """
    def __init__(self, chart, parent, app):
        super(View, self).__init__(chart, parent)
        self.app = app
        self.setMouseTracking(True)
        self.setInteractive(True)
        self.createTrackingTools()

######## Init - tracking tools setup

    def createTrackingTools(self):
        self.focusLine = QGraphicsLineItem(0, 0, 0, 10, self.chart())
        focusPen = QtGui.QPen()
        focusPen.setWidthF(1)
        focusPen.setStyle(QtCore.Qt.DashLine)
        focusPen.setColor(QtGui.QColor("#999999"))
        self.focusLine.setPen(focusPen)

        self.focusValueTextItem = QGraphicsTextItem(self.chart())
        self.focusValueTextItem.setScale(1.5)
        self.focusValueTextItem.setZValue(10)
        self.focusValueTextItem.setDefaultTextColor(QtGui.QColor("#333333"))

######## Event handlers

    def mouseMoveEvent(self, event):
        super(View, self).mouseMoveEvent(event)
        if not self.focusLine.isVisible(): self.focusLine.show()
        if not self.focusValueTextItem.isVisible(): self.focusValueTextItem.show()

        try:
            self.focusValueTextItem.setPos(event.x(), event.y())

            xVal = self.chart().mapToValue(QtCore.QPointF(event.x(), 0), self.chart().series()[0]).x()
            html = str(self.parent().chart.xdata[round(xVal)]) + "<br>"
            for i in range(len(self.chart().ydata)):
                if self.chart().series()[i].isVisible():
                    html += "<font color=\"" + self.chart().series()[i].color().name() + "\">" + "{0:.3f}<br>".format(self.parent().chart.ydata[i][round(xVal)])
            self.focusValueTextItem.setHtml(html)

            focusLineX = self.chart().mapToPosition(QtCore.QPointF(round(xVal), 0), self.chart().series()[0]).x()
            self.focusLine.setPos(focusLineX, 0)
        except IndexError:
            self.focusValueTextItem.hide()
            self.focusLine.hide()

    def leaveEvent(self, event):
        super(View, self).leaveEvent(event)
        # self.app.changeOverrideCursor(QtCore.Qt.ArrowCursor)
        self.app.restoreOverrideCursor()
        if self.chart().series():
            self.focusLine.hide()
            self.focusValueTextItem.hide()

    def enterEvent(self, event):
        super(View, self).enterEvent(event)
        self.app.setOverrideCursor(QtCore.Qt.CrossCursor)

    def keyPressEvent(self, event):
        super(View, self).keyPressEvent(event)
        key = event.text()
        if key in ["1","2","3","4","5","6","7","8","9"]:
            self.parent().chart.toggleSerieVisiblity(key)
        if "a" in key:
            self.parent().chart.toggleAnimatable(key)
        if "p" in key:
            self.parent().chart.toggleProperties()
        if "f" in key:
            self.parent().chart.toggleLeftWidget()
        if "t" in key:
            self.parent().chart.toggleBottomWidget()
        if "m" in key:
            self.parent().chart.multiplyAll(2)
        if "d" in key: # DEBUG
            self.parent().chart.filterAlamesOne()
        if "r" in key: # DEBUG
            self.parent().chart.zoomReset()
        if "u" in key: # DEBUG
            self.parent().chart.leftWidget.updateAll()

        if event.key() == QtCore.Qt.Key_Right:
            self.chart().scroll(10, 0)
        if event.key() == QtCore.Qt.Key_Left:
            self.chart().scroll(-10, 0)

    def mousePressEvent(self, event):
        super(View, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.MiddleButton:
            self.chart().zoomReset()


    def mouseReleaseEvent(self, event):
        ######## set range values to left widget
        super(View, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.chart().leftWidget.updateValuesFromChart()


    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        line = self.focusLine.line()
        line.setLength(self.height())
        self.focusLine.setLine(line)
