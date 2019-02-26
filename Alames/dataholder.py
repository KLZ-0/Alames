import math

from Alames import scope
from Alames.dataholderbase import DataHolderBase
from Alames.chartlineseries import ChartLineSeries

class DataHolder(DataHolderBase):
    """Data holder/container, inherits DataHolderBase and adds support for QSeries"""

    # NOTE: self.qSeries are not aligned with with self._YData
    #       Not every YData array contains numbers and thus cannot be added to the chart
    #       For example YData can contain 7 arrays but self.qSeries only 3

    _start = 0
    _end = -1

    _qSeries = []

    def __init__(self, xdata=[], ydata=[]):
        super(DataHolder, self).__init__(xdata, ydata)

######## Updates

    def updateColumnNames(self):
        for serie in self._qSeries:
            self._columnNames[serie.property("number")] = serie.name()

######## YData low level access - used in chartmodifier

    def setYData(self, ydatanum, ydata):
        super(DataHolder, self).setYData(ydatanum, ydata)
        self._updateQSeries()

######## Setters - only super

    def setDataFromCSV(self, csv):
        """High level access function"""
        super(DataHolder, self).setDataFromCSV(csv)
        self.resetRange()
        # TODO: Figure out what happens with the qseries inside the chart -> they should be deleted and new ones created

    def setData(self, xdata, ydata):
        """Low level access function"""
        super(DataHolder, self).setData(xdata, ydata)
        self.resetRange()

    def setXData(self, xdata):
        super(DataHolder, self).setXData(xdata)
        self.resetRange()

    def _truncate(self):
        super(DataHolder, self)._truncate()
        for serie in self._qSeries:
            if serie.chart():
                serie.chart().removeSeries(serie)
        self._qSeries = []

######## Setters - custom

    def setRange(self, start, end):
        """Expects a range between 0-max range of the chart"""
        # TODO: Fix the max zooming area to be zoomed out
        self._start = start
        self._end = end
        self._updateQSeries()

    def resetRange(self):
        self._start = 0
        self._end = len(self._XData)-1
        self._updateQSeries()

######## Getters

    def columnNamesOfSeries(self):
        """Column names which could be added to chart (their YData contains only numbers)"""
        return [serie.name() for serie in self._qSeries]

    def getDummyQSerie(self):
        """Return a dummy serie for e.g. mapping.."""
        return self._qSeries[0]

    def getQSeries(self, serienum=None):
        if serienum == None:
            return self._qSeries
        
        return self._qSeries[serienum]

######## Privates

    def _setDataToQSerie(self, YDataNum):
        """Set the data of a QSerie """
        for serie in self._qSeries:
            if serie.property("number") == YDataNum:
                serie.setData(
                    self._YData[YDataNum][self._start:self._end+1])

    def _makeQSeries(self):
        for i in range(len(self._YData)):
            # TODO: Make use of the property "number"
            if isinstance(self._YData[i][0], float) or isinstance(self._YData[i][0], int):
                # Only create a QSeries if data is number -> thus it can be shown on a chart
                self._qSeries.append(ChartLineSeries())
                self._qSeries[-1].setProperty("number", i)
                self._qSeries[-1].setName(self._columnNames[i])
                self._qSeries[-1].nameChanged.connect(self.updateColumnNames)
                self._qSeries[-1].needsData.connect(self._setDataToQSerie)

    def _updateQSeries(self):
        # if len doesn't match that means a new file could have been opened
        if len(self._YData) != len(self._qSeries) or len(self._qSeries) == 0: # NOTE: this will not work with dynamic series
            self._qSeries = []
            self._makeQSeries()

        # Add the ydata to series
        # for qserie in self._qSeries:
        #     qserie.setData(self._YData[qserie.property("number")][self._start:self._end+1])

        # At least one must be initialized for mapping
        self._setDataToQSerie(self._qSeries[0].property("number"))
