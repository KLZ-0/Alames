from Alames.importer import *

from Alames import scope

class DataHolderBase(QtCore.QObject):
    """Data holder/container, if the data is composed of Current and Voltage the power values will also be calculated - It has no range"""
    _xColumnName = ""
    _columnNames = []

    _YRMS = []
    _fi = 0
    _cosFi = 1
    _apparentP = 0
    _activeP = 0
    _reactiveP = 0

    changed = QtCore.pyqtSignal()

    def __init__(self, xdata=[], ydata=[]):
        super(DataHolderBase, self).__init__()
        self._XData = xdata  # xdata [val] val can be string
        self._YData = ydata  # ydata [i][val]

######## Actions

    def export(self, filename, exportSeries=None):
        exportHeaders = [self._xColumnName]
        exportData = [self._XData]
        if exportSeries == None:
            exportHeaders += self._columnNames
            exportData += self._YData
        
        else:
            for i in exportSeries:
                exportHeaders.append(self._columnNames[i])
                exportData.append(self._YData[i])

        pandasObject = DataFrame(list(zip(*exportData)))
        filename = open(filename, "w")
        filename.write("Reading exported from Alames;\n")
        pandasObject.to_csv(filename, sep=getattr(scope.settings, "ExportCSVDelimiter", ";"), header=exportHeaders, index=False, line_terminator=getattr(scope.settings, "ExportCSVLineTerminator", ";\n"))

######## Setters

    def setColumnNames(self, columnnames):
        # Strip the first column (it is the X axis) and strip the last column (unnamed something) > created if the delimiter is at the eol
        self._xColumnName = columnnames[0]
        self._columnNames = [name for name in columnnames[1:]]

    def setDataFromCSV(self, csv):
        """High level access function"""
        # append the required YData array length [][]
        rows = csv.values
        self.setColumnNames(csv.columns)

        self._setYDataLen(len(rows[0])-1)

        for row in rows:
            self._XData.append(row[0])

            for i in range(len(row)-1):
                self._YData[i].append(row[i+1])

        # Bad CSV correction
        # When the CSV comes from envis, it appends a delimiter at the end of every line > strip that off
        if "Unnamed" in self._columnNames[-1]:
            del self._columnNames[-1]
            del self._YData[-1]

        # Calc RMS and power
        if self._testUI():
            self._calcAll()

        self.changed.emit()

    def setData(self, xdata, ydata):
        """Low level access function"""
        self._XData = xdata
        self._YData = ydata

        # Calc RMS and power
        if self._testUI():
            self._calcAll()

        self.changed.emit()

    def setXData(self, xdata):
        self._XData = xdata

        # Calc RMS and power
        if self._testUI():
            self._calcAll()

        self.changed.emit()

    # Does not support overall YData change - it is not needed
    def setYData(self, ydatanum, ydata, calc=False):
        """YData low level access - used in chartmodifier"""
        self._YData[ydatanum] = ydata

        # Calc RMS and power 
        # In this case it can cause unexpected calculation problems if not all the ydata was changed
        self._calcAll() 

        self.changed.emit()

######## Getters

    def XData(self):
        """The returned data shouldn't be modified directly"""
        return self._XData

    def YData(self):
        """The returned data shouldn't be modified directly"""
        return self._YData

    def getYData(self, ydatanum):
        """YData low level access - used in chartmodifier (the returned data shouldn't be modified directly)"""
        return self._YData[ydatanum]

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
        return self.getLen()

    def getLen(self):
        return len(self._YData)

    def getRealXValue(self, abstractxval):
        """Retranslate the abstract XData to real value"""
        return self._XData[abstractxval]

    def getAbstractXValue(self, realxval):
        """Retranslate the real XData to abstract value"""
        return self._XData.index(realxval)

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
        self._XData = []
        self._YData = []

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
        """Finds two zero points and divides 90 degrees by their difference in x points"""
        keys = []
        dataSet = ydata[1] # FIXME: Possible IndexError
        u = 0
        for i in range(len(dataSet)):
            if (abs(dataSet[i]) > abs(dataSet[i+1]) < abs(dataSet[i+2]) and abs(dataSet[i+1]) < max(dataSet)/2):
                keys.append(i+1)
                if u:
                    break
                u += 1
        return 90/(keys[1] - keys[0])
