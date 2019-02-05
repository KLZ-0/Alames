import math

from Alames import scope
from Alames.serieshelper import SeriesHelper

class DataHolder:
    """Data holder/container, if the data is composed of Current and Voltage the power values will also be calculated"""
    _columnNames = []

    _YRMS = []
    _fi = 0
    _cosFi = 1
    _apparentP = 0
    _activeP = 0
    _reactiveP = 0

    def __init__(self, xdata=[], ydata=[]):
        self._XData = xdata # xdata [val]
        self._YData = ydata # ydata [i][val]

######## Setters

    def setDataFromRows(self, rows):
        """High level access function"""
        # append the required YData array length [][]
        self._setYDataLen(len(rows[0])-1)

        for row in rows:
            self._XData.append(row[0])
            for i in range(len(row)-1):
                self._YData[i].append(row[i+1])

        if self._testUI(): self._calcAll()

    def setData(self, xdata, ydata):
        """Low level access function"""
        self._XData = xdata
        self._YData = ydata

    def setColumnNames(self, columnnames):
        self._columnNames = columnnames

######## Getters

    def XData(self):
        return self._XData

    def YData(self):
        return self._YData

    def columnNames(self):
        return self._columnNames

    def fi(self):
        return self._fi

    def powerDataSet(self):
        return [self._activeP,
                self._reactiveP, self._apparentP, self._cosFi]

    def RMSValues(self):
        return self._YRMS

    def isLoaded(self):
        return len(self._YData)

######## Privates

    def _testUI(self):
        """Test for Alames One values - whether the data is composed of voltage and current"""
        return len(self._XData) and len(self._YData) == 3

    def _calcAll(self):
        self._calcPowerRelatedValues(self._YData)

    def _setYDataLen(self, num):
        self._truncate()

        for i in range(num):
            self._YData.append([])

    def _truncate(self):
        self.setData([], [])

######## Privates - calculations

    def _calcPowerRelatedValues(self, ydata):
        self._calcRms()

        if len(ydata) > 1:
            self._fi = self._calcFi(ydata)
            if self._fi % 90 == 0 and self._fi != 0:
                self._fi -= 0.01
            self._cosFi = round(math.cos(math.radians(self._fi)), 2)
            self._apparentP = abs(round(self._YRMS[0]*self._YRMS[1], 2))
            self._activeP = abs(self._apparentP * self._cosFi)
            self._reactiveP = abs(
                self._apparentP * round(math.sin(math.radians(self._fi)), 2))
        else:
            self._YRMS = []
            self._fi = 0
            self._cosFi = 1
            self._apparentP = 0
            self._activeP = 0
            self._reactiveP = 0

    def _calcRms(self):
        self._YRMS = []

        for instantValues in self._YData:
            sums = sum([k**2 for k in instantValues])
            rms = math.sqrt(sums/len(instantValues))
            self._YRMS.append(round(rms, 2))

    def _calcFi(self, ydata):
        keys = []
        density = self._getDegreeDensity(ydata)
        for values in ydata:
            preVar = abs(values[0])
            for i in range(len(values)):
                if (abs(values[i]) > abs(values[i+1]) < abs(values[i+2]) and abs(values[i+1]) < max(values)/2) or values[i+1] == 0:
                    keys.append(i+1)
                    break
        return (keys[0]-keys[1])*density

    def _getDegreeDensity(self, ydata):
        keys = []
        dataSet = ydata[1]
        u = 0
        waitingtime = 30
        for i in range(len(dataSet)):
            if (abs(dataSet[i]) > abs(dataSet[i+1]) < abs(dataSet[i+2]) and abs(dataSet[i+1]) < max(dataSet)/2):
                keys.append(i+1)
                if u:
                    break
                u += 1
        return 90/(keys[1] - keys[0])
