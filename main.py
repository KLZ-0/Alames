# IDEA: Add select time with rubberband and calcRms only from it
# IDEA: Add selecting more seconds + calcRms from them
# TODO: Add select timeRange from timeLineChart

# IDEA: Modify menubar to something like in Pymage

# TODO: Add sequential reading IDEA: Add live reading

# TODO: Add settings reloading
# TODO: update setings/repaint chart maybe

# TODO: HW: Construct DIN voltage Transformer, calibrate    NOTE: Partially done
# TODO: Add scaling of phasor arrows

# TODO: Create scale and valueLabels in phasorWidget

import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis

import mainlib
import sinlib
import actions

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.synonyms = {"i" : "current", "u" : "voltage"}
        self.translateCurve = {"current" : 0, "voltage" : 1}
        self.translateIndex = ["current", "voltage"]
        self.alltypes = ["current", "voltage", "activeP", "reactiveP", "apparentP", "cosFi"]
        self.units = {"current" : "A", "voltage" : "V", "activeP" : "W", "reactiveP" : "VAr", "apparentP" : "VA", "cosFi" : ""}
        mainlib.setupAll(self, app)

    def displaynew(self, text):
        if self.chart.series():
            actions.rmser(self, 1)
        # TODO: Translate to Slovak
        if text != "Select one":
            self.rmsValueLabel.show()
            self.rmsLabel.show()
            self.phasorWidget.show()
            mainlib.resizeDynamicContent(self)
            self.selectCurves.show()
            first = 0
            last = 0
            for i, j in enumerate(self.xvalues):
                if text in j:
                    if first == False:
                        first = i
                    else:
                        last = i
            if len(self.voltages) != 0:
                voltages = self.voltages[first:last]
            else:
                voltages = False
            currents = self.currents[first:last]
            xdata = self.xdata[first:last]

            if voltages:
                ydata = [currents, voltages]
            else:
                ydata = [currents]

            self.init_chart_data(xdata, ydata)
        elif text == "Select one":
            self.rmsValueLabel.hide()
            self.rmsLabel.hide()
            self.phasorWidget.hide()
            self.selectCurves.hide()
            for checkBox in self.selectCurvesOptions:
                if checkBox.isChecked():
                    checkBox.toggle()

    def init_chart_data(self, xdata, ydata):
        self.curves = []
        self.curve_data = []
        self.focus_point = []
        self.axis = []
        for i in ydata:
            self.curves.append(QLineSeries())
            self.curve_data.append({})
            self.focus_point.append(QGraphicsEllipseItem(self.chart))
            self.axis.append(QValueAxis())

        self.pos_labels = QGraphicsTextItem(self.chart)
        self.pos_labels.setScale(1.5)
        self.pos_labels.setZValue(10)

        self.focus_line = QGraphicsLineItem(0, 0, 0, self.chart_view.height(), self.chart)
        self.focus_line.hide()
        focus_pen = QtGui.QPen()
        focus_pen.setWidthF(1)
        focus_pen.setStyle(QtCore.Qt.DashLine)
        focus_pen.setColor(QtGui.QColor("#999999"))
        self.focus_line.setPen(focus_pen)

        self.setup_chart(xdata, ydata)
        try:
            sinlib.setPowerRelatedValues(self, ydata)
            mainlib.setRmsLabel(ydata, self.settings["language"], self.fi, self.powerDataSet, self.rmsValueLabel, self.rmsLabel, self.baseRmsText, self.units, self.alltypes)
        except IndexError:
            if self.settings["language"] == "English":
                self.rmsLabel.setText("Failed to load power..")
                self.rmsValueLabel.setText("Empty measurement?")
            elif self.settings["language"] == "Slovak":
                self.rmsLabel.setText("Nemožný výpočet výkonu..")
                self.rmsValueLabel.setText("Prázdne meranie?")
            sinlib.setEmptyPRV(self)
        self.phasorWidget.update()

    def setup_chart(self, xdata, ydata):
        for i in range(len(ydata)):
            self.curve_data[i] = dict(zip(xdata, ydata[i])) # constant for one chart >> use curve[0], but two points and labels >> warning! if only current reading

            sinlib.colorCurve(self.curves[i], self.colors[self.translateIndex[i]], QtCore.Qt.RoundCap)

            self.curves[i].append(sinlib.series_to_polyline(xdata, ydata[i]))

            if self.translateCurve["current"] == i and self.settings["dynamic-axis-scaling"] == False:
                self.axis[i].setMax(50)
                self.axis[i].setMin(-50)
            elif self.translateCurve["voltage"] == i and self.settings["dynamic-axis-scaling"] == False:
                self.axis[i].setMax(400)
                self.axis[i].setMin(-400)
            else:
                mx = max(max(ydata[i]), abs(min(ydata[i])))
                self.axis[i].setMax(mx+0.1)
                self.axis[i].setMin(-(mx+0.1))

            self.focus_point[i].setRect(0, 0, 6, 6)
            self.focus_point[i].hide()

            focus_brush = QtGui.QBrush()
            focus_brush.setStyle(QtCore.Qt.SolidPattern)
            focus_brush.setColor(QtGui.QColor(self.colors[self.translateIndex[i]]))
            self.focus_point[i].setBrush(focus_brush)

    def displayCurve(self, state):
        self.checkedCurveBoxes = []
        for i in range(self.numberOfBaseValues):
            if self.selectCurvesOptions[i].isChecked(): self.checkedCurveBoxes.append(self.synonyms[self.selectCurvesOptions[i].text().lower()])
            u = self.translateCurve[self.synonyms[self.selectCurvesOptions[i].text().lower()]]
            if self.selectCurvesOptions[i].isChecked() and mainlib.seriesInChart(self.curves[i], self.chart) == False:
                self.addCurve(u)
            elif self.selectCurvesOptions[i].isChecked() == False and mainlib.seriesInChart(self.curves[i], self.chart):
                self.removeCurve(u)

    def addCurve(self, i):
            self.chart.zoomReset()
            self.chart.addSeries(self.curves[i])
            self.chart.setAxisY(self.axis[i], self.curves[i])

    def removeCurve(self, i):
        for chartSeries in self.chart.series():
            if self.curves[i] == chartSeries:
                self.chart.removeSeries(chartSeries)
        self.chart.removeAxis(self.axis[i])
        self.focus_point[i].hide()
        if len(self.chart.series()) == 0:
            self.focus_line.hide()

    def exit(self):
        app.quit()

    def resizeEvent(self, event):
        self.menubar.setGeometry(0, 0, self.width(), self.menubar.height())
        self.tabmenu.setGeometry(0, self.menubar.frameGeometry().height(), (self.width()/3)*2, (self.height()/3)*2 - self.menubar.height())
        self.chart_view.setGeometry(0, 0, self.tab[0].width(), self.tab[0].height())
        self.timeLineChartView.setGeometry(0, self.tabmenu.height() + self.menubar.height(), self.width()/1.5, (self.height()-self.menubar.height())/3)
        self.openReadingButton.setGeometry(self.width()-self.width()/3, self.menubar.frameGeometry().height(), self.width()/3, 40)
        self.date_picker.setGeometry(self.width()-self.width()/3, self.menubar.frameGeometry().height(), self.width()/9, 40)
        self.timeInfoLabel.setGeometry(self.date_picker.x() + self.date_picker.width() + 10, self.menubar.frameGeometry().height(), self.width()/9*2, 40) # RMS etc..
        self.date_show.setGeometry(self.tabmenu.width()/2.45, 0, 200, 50)
        if self.selectCurvesOptions:
            mainlib.resizeDynamicContent(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
