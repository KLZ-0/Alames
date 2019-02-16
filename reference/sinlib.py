from PyQt5.QtGui import QPolygonF, QColor
import numpy as np
import math
import os

# NOTE: Library for mathematical operations

def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline

    This code is derived from PythonQwt's function named
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size-1)*2+1:2] = xdata
    memory[1:(size-1)*2+2:2] = ydata
    return polyline

def calcRms(instantValues):
    sums = sum([k**2 for k in instantValues])
    rms = math.sqrt(sums/len(instantValues))
    return round(rms, 2)

def getEffectivePoints(time_values, ydata, times):       # for future -- x placeholder is not parameter
    ydata_cur = []
    for text in times:
        first = 0
        last = 0
        for i, j in enumerate(time_values):
            if text in j:
                if first == False:
                    first = i
                else:
                    last = i
        cur = ydata[first:last]
        for u in range(len(cur)):
            cur[u] = (cur[u] / 204.6) * 10
        ydata_cur.append(calcRms(cur))
    return times, ydata_cur

def recalculateValues(voltages, currents, const):
    if voltages:
        voltages = [i*const for i in voltages]
    currents = [i/2.54 for i in currents]
    return voltages, currents

def colorCurve(curve, color, penCap):
    pen = curve.pen()
    pen.setColor(QColor(color))
    pen.setCapStyle(penCap)
    pen.setWidthF(1.5)
    curve.setPen(pen)

def calcFi(ydata):
    keys = []
    density = getDegreeDensity(ydata)
    for values in ydata:
        preVar = abs(values[0])
        for i in range(len(values)):
            if (abs(values[i]) > abs(values[i+1]) < abs(values[i+2]) and abs(values[i+1]) < max(values)/2) or values[i+1] == 0:
                keys.append(i+1)
                break
    return (keys[0]-keys[1])*density

def getDegreeDensity(ydata):
    keys = []
    dataSet = ydata[1]
    u = 0
    waitingtime = 30
    for i in range(len(dataSet)):
        if (abs(dataSet[i]) > abs(dataSet[i+1]) < abs(dataSet[i+2]) and abs(dataSet[i+1]) < max(dataSet)/2):
            keys.append(i+1)
            if u: break
            u += 1
    return 90/(keys[1] - keys[0])

def setPowerRelatedValues(self, ydata):
    if len(ydata) > 1:
        self.fi = calcFi(ydata)
        if self.fi % 90 == 0 and self.fi != 0:
            self.fi -= 0.01
        self.cosFi = round(math.cos(math.radians(self.fi)), 2)
        self.apparentP = abs(round(calcRms(ydata[0])*calcRms(ydata[1]), 2))
        self.activeP = abs(self.apparentP * self.cosFi)
        self.reactiveP = abs(self.apparentP * round(math.sin(math.radians(self.fi)), 2))
        self.powerDataSet = [self.activeP, self.reactiveP, self.apparentP, self.cosFi]
        self.actualValues = [calcRms(ydata[0]), calcRms(ydata[1])]
    else:
        setEmptyPRV(self)

def setEmptyPRV(self):
    self.powerDataSet = []
    self.fi = 0
    self.actualValues = []
