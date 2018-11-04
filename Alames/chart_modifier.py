import traceback
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class Modifier:
    """
    Purpose: modifying chart series
    Chart overrides this class
    # NOTE: Use chart.series()[i].replace()
    # NOTE: ydata is not the same len as chart.series.. some series could be intentionally hidden and not present in ydata, therefore they are not displayed in the tracking tools
    """
    def __init__(self):
        self.filterAlamesOneApplied = False

    def multiplyAll(self, ratio):
        self.ydata = []
        for serie in self.series():
            self.ydata.append([])
            vect = serie.pointsVector()
            for point in vect:
                point.setY(point.y()*ratio)
                self.ydata[-1].append(point.y())
            serie.replace(vect)
        self.updateAxes()

    def filterAlamesOne(self):
        try:
            if self.filterAlamesOneApplied:
                self.parent.errorPopup("Filter already applied!")
                return
            self.series()[0].setName("Voltage")
            self.series()[1].setName("Current")
            self.series()[2].setName("State")

            voltageVect = self.series()[0].pointsVector()
            currentVect = self.series()[1].pointsVector()
            stateVect = self.series()[2].pointsVector()
            self.ydata = [[], []]
            for i in range(len(stateVect)):
                state = stateVect[i].y()
                if state == 0:
                    pass
                elif state == 1:
                    self.invertPointY(voltageVect[i])
                elif state == 2:
                    self.invertPointY(currentVect[i])
                elif state == 3:
                    self.invertPointY(voltageVect[i])
                    self.invertPointY(currentVect[i])
                self.multiplyPoint(voltageVect[i], 3.62) # calibration
                self.multiplyPoint(currentVect[i], 1/2.54) # current calc
                self.ydata[0].append(voltageVect[i].y())
                self.ydata[1].append(currentVect[i].y())

            self.series()[0].replace(voltageVect)
            self.series()[1].replace(currentVect)
            self.series()[2].hide()
            self.updateAxes()

            self.series()[0].setColor(QtGui.QColor("#0000ff"))
            self.series()[1].setColor(QtGui.QColor("#ff0000"))
            self.propertyWidget.updateSections()

            self.filterAlamesOneApplied = True
        except:
            self.parent.errorPopup(traceback.format_exc())

    def invertPointY(self, point):
        point.setY(-point.y())

    def multiplyPoint(self, point, ratio):
        point.setY(point.y()*ratio)

    def setRange(self, start, end):
        for serie in self.series():
            serie.setRange(start, end)
        self.updateAxes()
        firstX = self.mapToPosition(self.series()[0].firstPoint(), self.series()[0]).x()
        lastX = self.mapToPosition(self.series()[0].lastPoint(), self.series()[0]).x()

        self.zoomIn(QtCore.QRectF(firstX, self.plotArea().y(), lastX-firstX, self.plotArea().height()))
