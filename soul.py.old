import os, pandas, platform
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QDateTimeAxis

import sinlib

# NOTE: Library for core functions in the future
# NOTE: Currently the time precision is around 0.5ms at worst >> 3ms now (with raw)

# TODO: add functions for sequential and long-term capturing

def openfl(self):
    if platform.uname().system == "Linux":
        op_dir = QFileDialog.getOpenFileName(self, 'Load KLZ archive', '/home', "KLZ archives (*.klz)")[0]
    else:
        op_dir = QFileDialog.getOpenFileName(self, 'Load KLZ archive', 'C:', "KLZ archives (*.klz)")[0].encode('utf-8').decode('utf-8', 'replace')
    if Path(op_dir).is_file():
        xdata, xvalues, voltages, currents, date, times = getdata(op_dir)
        self.xvalues = xvalues
        self.date = date
        self.times = times
        self.numberOfBaseValues = 1

        self.timeInfoLabel.setText(times[0] + " - " + times[-1])

        for checkBox in self.selectCurvesOptions:
            checkBox.hide()
        self.selectCurvesOptions = [QCheckBox("I", self.selectCurves)]
        if voltages:
            self.numberOfBaseValues += 1
            self.selectCurvesOptions.append(QCheckBox("U", self.selectCurves))

        setDynamicGeometry(self)

        self.timeInfoLabel.show()
        self.date_picker.clear()
        self.date_picker.addItem("Select one")
        self.date_picker.addItems(times)
        self.openReadingButton.hide()
        self.date_picker.show()
        # r = lambda: random.randint(0, 255)
        # self.add_graphs(xdata, ydata, color=QtGui.QColor('#%02X%02X%02X' % (r(), r(), r())))
        voltages, currents = sinlib.recalculateValues(voltages, currents, self.settings["calibration"])
        self.xdata = xdata
        self.voltages = voltages
        self.currents = currents
        createTimeChart(self)

def getdata(dir):
    with open(dir, "r") as of:
        date = of.readline().rstrip(",1\n")
    voltages = []
    currents = []
    times = []
    xvalue = []
    pwd = os.getcwd()
    os.chdir(os.path.dirname(dir))
    f = pandas.read_csv(os.path.basename(dir))
    os.chdir(pwd)
    csv = f.values
    xdata = range(len(csv))
    for line in csv:
        try:
            time_ = line[0].split(".")[0]
            if time_ not in times:
                times.append(time_)
                u=time_
            xvalue.append(line[0])
            if len(f.columns) == 4:
                if line[3] == 0:
                    voltages.append(line[1])
                    currents.append(line[2])
                elif line[3] == 1:
                    voltages.append(-line[1])
                    currents.append(line[2])
                elif line[3] == 2:
                    voltages.append(line[1])
                    currents.append(-line[2])
                elif line[3] == 3:
                    voltages.append(-line[1])
                    currents.append(-line[2])
            elif len(f.columns) == 3:
                if line[2] == 0 or line[2] == 1:
                    currents.append(line[1])
                elif line[2] == 2 or line[2] == 3:
                    currents.append(-line[1])
            else:
                print("Currupt .klz file")
        except:
            pass
    return xdata, xvalue, voltages, currents, date, times

def calcAllRms(times, values, voltages, currents):
    rmsVoltageValues = []
    rmsCurrentValues = []
    for time in times:
        first = 0
        last = 0
        for i, j in enumerate(values):
            if time in j:
                if first == False:
                    first = i
                else:
                    last = i
        if len(voltages) != 0:
            rmsVoltageValues.append(sinlib.calcRms(voltages[first:last]))
        rmsCurrentValues.append(sinlib.calcRms(currents[first:last]))
        rmsValues = [rmsCurrentValues, rmsVoltageValues]
    return rmsValues

def createTimeChart(self):
    self.rmsValues = calcAllRms(self.times, self.xvalues, self.voltages, self.currents)
    self.timeChartSeries = []
    for i in range(self.numberOfBaseValues):
        self.timeChartSeries.append(QLineSeries())
        self.timeChartSeries[i].append(sinlib.series_to_polyline(range(len(self.times)), self.rmsValues[i]))
        sinlib.colorCurve(self.timeChartSeries[i], self.colors[self.translateIndex[i]], QtCore.Qt.RoundCap)
        self.timeLineChart.addSeries(self.timeChartSeries[i])

    axisX = QDateTimeAxis()
    axisX.setFormat("hh:mm:ss")
    axisX.setMin(QtCore.QDateTime.fromString(self.times[0], "hh:mm:ss"))
    axisX.setMax(QtCore.QDateTime.fromString(self.times[-1], "hh:mm:ss"))
    self.timeLineChart.setAxisX(axisX)
    axisY = QValueAxis()
    axisY.setRange(0, 260)
    for curve in self.timeChartSeries:
        self.timeLineChart.setAxisY(axisY, curve)

def setDynamicGeometry(self):
    for checkBox in self.selectCurvesOptions:
        checkBox.stateChanged.connect(self.displayCurve)
    self.selectCurves.setGeometry(self.width()-self.width()/3, self.date_picker.frameGeometry().y() + self.date_picker.frameGeometry().height(), self.width()/3, self.selectCurvesOptions[0].height()*(1+len(self.selectCurvesOptions)*0.6))
    for i in range(len(self.selectCurvesOptions)):
        self.selectCurvesOptions[i].setGeometry(10, self.selectCurvesOptions[i].height()*0.6*(i+1), self.width()/3, self.selectCurvesOptions[i].height())
    self.rmsLabel.setGeometry(self.width()-self.width()/3, self.selectCurves.frameGeometry().y() + self.selectCurves.frameGeometry().height() + 10, self.width()/6 + 1, (self.rmsValueLabel.font().weight()/3)*(len(self.baseRmsText) + 1))
    self.rmsValueLabel.setGeometry(self.width()-self.width()/6, self.selectCurves.frameGeometry().y() + self.selectCurves.frameGeometry().height() + 10, self.width()/6, (self.rmsValueLabel.font().weight()/3)*(len(self.baseRmsText) + 1))
    setPhasorPos(self)
    try: setFocusLine(self)
    except AttributeError: pass

def setPhasorPos(self):
    xstart = self.width()-self.width()/3
    ystart = self.rmsLabel.frameGeometry().y() + self.rmsLabel.frameGeometry().height()
    side = self.width()/5
    xoffset = (self.width()/3 - side)/2
    yoffset = ((self.height() - (self.rmsLabel.frameGeometry().y() + self.rmsLabel.frameGeometry().height())) - side)/2
    self.phasorWidget.setGeometry(xstart + xoffset, ystart + yoffset, side, side)

def setFocusLine(self):
    line = self.focus_line.line()
    line.setLength(self.chart_view.height())
    self.focus_line.setLine(line)
