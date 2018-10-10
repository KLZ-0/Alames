from PyQt5 import QtCore

import soul

def tooltip(self, position):
    try:
        self.pos_labels.show()
        for curve in self.checkedCurveBoxes:
            if self.focus_point[self.translateCurve[curve]].isVisible() == False:
                self.focus_point[self.translateCurve[curve]].show()
        self.focus_line.show()
        self.date_show.show()

        values = self.chart.mapToValue(QtCore.QPointF(position.x(), position.y()), self.chart.series()[0])
        yval = []
        focus_point_point = []
        for i in range(self.numberOfBaseValues):
            yval.append(self.curve_data[i][round(values.x())])
            focus_point_point.append(self.chart.mapToPosition(QtCore.QPointF(round(values.x()), yval[i]), self.curves[i]))

        self.pos_labels.setPos(position.x()+10, position.y()+10)
        text = ""
        for curve in self.checkedCurveBoxes:
            text += "<font color=\"" + self.colors[curve] + "\">" + str(round(yval[self.translateCurve[curve]], 4)) + "</font><br>"
        self.pos_labels.setHtml(text)
        # self.pos_labels.setText("\033[94m" + str(round(yval[0], 4)) + "\n" + str(round(yval[1], 4))) # edit yval
        self.date_show.setText(self.date + " " + self.xvalues[round(values.x())])
        for i in range(len(self.focus_point)):
            self.focus_point[i].setPos(focus_point_point[i].x()-3, focus_point_point[i].y()-3)
        # TODO: Optimize the next 4 lines
        if self.focus_point[0].isVisible():
            self.focus_line.setPos(focus_point_point[0].x(), 0)
        else:
            self.focus_line.setPos(focus_point_point[1].x(), 0)
    except KeyError: # if mapping goes out of the current series
        pass

def ChartViewLeave(self):
    if self.chart.series():
        self.pos_labels.hide()
        for point in self.focus_point:
            point.hide()
        self.focus_line.hide()
        self.date_show.hide()

def rmser(self, typ=0):
    try:
        for chartSeries in self.chart.series():
            self.chart.removeSeries(chartSeries)
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        self.pos_labels.hide()
        for point in self.focus_point:
            point.hide()
        self.focus_line.hide()
        self.timeInfoLabel.hide()
        self.rmsValueLabel.hide()
        self.rmsLabel.hide()
        self.phasorWidget.hide()

        if typ == 0:
            self.date_picker.hide()
            self.openReadingButton.show()

            for chartSeries in self.timeLineChart.series():
                self.timeLineChart.removeSeries(chartSeries)
            for axis in self.timeLineChart.axes():
                self.timeLineChart.removeAxis(axis)

        self.selectCurves.hide()
        for checkBox in self.selectCurvesOptions:
            if checkBox.isChecked():
                checkBox.toggle()
    except:
        pass

def radioChanged(self):
    for button in self.select:
        if button.isChecked():
            buttonObjectName = button.objectName()
            break
    if buttonObjectName == "Raw" or buttonObjectName == "Only current":
        self.durationSelect.show()
        self.durationSelectLabel.show()
    else:
        self.durationSelect.hide()
        self.durationSelectLabel.hide()
    resizeSaveButton(self)

def resizeSaveButton(self):
    if self.durationSelectLabel.isVisible():
        self.saveFileButton.setGeometry(self.width()/3, self.durationSelectLabel.frameGeometry().y() + self.durationSelectLabel.frameGeometry().height() + 10, self.saveFileButton.width(), self.saveFileButton.height())
    else:
        self.saveFileButton.setGeometry(self.width()/3, self.portEdit.frameGeometry().y() + self.portEdit.frameGeometry().height() + 10, self.saveFileButton.width(), self.saveFileButton.height())
