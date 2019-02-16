import math

from Alames import scope
from Alames.dataholderbase import DataHolderBase
from Alames.chartlineseries import ChartLineSeries

class DataHolder(DataHolderBase):
    """Data holder/container, inherits DataHolderBase and adds support for QSeries"""

    _start = 0
    _end = -1

    _qSeries = []

    def __init__(self, xdata=[], ydata=[]):
        super(DataHolder, self).__init__(xdata, ydata)

######## YData low level access - used in chartmodifier

    def setYData(self, ydatanum, ydata):
        super(DataHolder, self).setYData(ydatanum, ydata)
        self._updateQSeries()

######## Setters - only super

    def setDataFromRows(self, rows):
        """High level access function"""
        super(DataHolder, self).setDataFromRows(rows)
        self.resetRange()

    def setData(self, xdata, ydata):
        """Low level access function"""
        super(DataHolder, self).setData(xdata, ydata)
        self.resetRange()

    def setXData(self, xdata):
        super(DataHolder, self).setXData(xdata)
        self.resetRange()

######## Setters - custom

    def setRange(self, start, end):
        """Expects a range between 0-max range of the chart"""
        self._start = start
        self._end = end
        self._updateQSeries()

    def resetRange(self):
        self._start = 0
        self._end = len(self._XData)-1
        self._updateQSeries()

######## Getters

    def getQSeries(self, serienum=None):
        if serienum == None:
            return self._qSeries
        
        return self._qSeries[serienum]

######## Privates

    def _makeQSeries(self):
        for i in range(len(self._YData)):
            # TODO: Implement the constructor and remove most of chartlineseries, preserving some methods
            # TODO: Make use of the property "number"
            self._qSeries.append(ChartLineSeries())
            self._qSeries[-1].setProperty("number", i)

    def _updateQSeries(self):
        # if len doesn't match that means a new file could have been opened
        if len(self._YData) != len(self._qSeries) or len(self._qSeries) == 0:
            self._qSeries = []
            self._makeQSeries()

        # Add the ydata to series
        for qserie in self._qSeries:
            # TODO: Implement this method in chartlineseries
            qserie.setData(self._YData[qserie.property("number")][self._start:self._end+1])
