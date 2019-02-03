from Alames import scope
from Alames.chartlineseries import ChartLineSeries

class SeriesHelper:
    """Helper for managing Chart QSeries"""

    def fillSeries(ydata, columnnames):
        scope.chart.qseries = []
        for i in range(len(ydata)):
            scope.chart.qseries.append(ChartLineSeries(ydata[i]))

            scope.chart.qseries[i].setName(str(i+1) + " - " + columnnames[i+1])

    def fillChart():
        for serie in scope.chart.qseries:
            scope.chart.addSeries(serie)

    def setRange(start, end):
        for serie in scope.chart.series():
            serie.setRange(start, end)
        scope.chart.updateAxes()
