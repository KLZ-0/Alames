from Alames.importer import *

from Alames import scope

from Alames import chartview
from Alames import leftwidget
from Alames import chartmodifier
from Alames.dataholderbase import DataHolderBase
from Alames.dataholder import DataHolder

class Chart(QChart, chartmodifier.ChartModifier):
    """
    Purpose: setup and modify the QChart
    Manages the charting subsystem consisting of the ChartView, Properties and BottomWidget.
    Initializes the required objects as its own properties
    """

    # Updated from LeftWidget
    _scrollSpeed = 10

    def __init__(self):
        super(Chart, self).__init__()
        self.setAcceptHoverEvents(True)
        self.selectionDataHolder = DataHolder()
        self.overallDataHolder = DataHolderBase()

######## Setup

    def constructChart(self, fileName):

        if not self.loadCSV(fileName):
            return False
        for serie in self.selectionDataHolder.getQSeries():
            self.addSeries(serie)
            serie.visibleChanged.connect(self.updateAxes)
            serie.scaleChanged.connect(self.updateAxes)
            
        return True

    def loadCSV(self, lFileName):
        if lFileName.endswith(".csv.xz"):
            lFileName = lzma.open(lFileName)  # file name or object
        elif lFileName.endswith(".csv"):
            lFileName = open(lFileName, "r")
        else:
            scope.errorPopup("Not supported file type", "The requested file does not match any known filetypes", level=2)
            return False

        try:
            # Detect a header -> set data header to be the second line
            autoDelimiter = self._detectDelimiter(lFileName)
            f = read_csv(lFileName, header=1, delimiter=getattr(scope.settings, "OpenCSVDelimiter", autoDelimiter), low_memory=False)
            if len(f.columns) == 1:
                raise ValueError("Not enough columns")
            self.selectionDataHolder.setDataFromCSV(f)
            self.overallDataHolder.setDataFromCSV(f)
            return True
        except lzma.LZMAError:
            scope.window.hideUi()
            scope.errorPopup("LZMA decompression failed", "damaged xz file", traceback.format_exc(), level=2)
            return False
        except ValueError:
            scope.window.hideUi()
            scope.errorPopup("Invalid delimiter", "The CSV parsing returned only one column", traceback.format_exc(), level=2)
            return False

    def _detectDelimiter(self, readableFile):
        charset = getattr(scope.settings, "OpenCSVDelimiterCheck", [",", ";"])
        charsetSplits = []
        for i, line in enumerate(readableFile):
            if i == 3: # some random line number in the data range
                for char in charset:
                    charsetSplits.append(len(str(line).split(char)))
                break
        
        readableFile.seek(0)
        for i in range(len(charsetSplits)):
            if charsetSplits[i] == max(charsetSplits):
                return charset[i]

        return ";"

######## Signal handlers

    def onSelectionChange(self, range):
        # call in ....connect(self.onSelectionChange)
        # self.selectionDataHolder.update(range)
        pass

######## Getters

    def getXData(self):
        return self.selectionDataHolder.XData()

    def getYData(self, num=None):
        if num != None:
            return self.selectionDataHolder.getYData(num)
        return self.selectionDataHolder.YData()

    def getDummyQSerie(self):
        return self.selectionDataHolder.getDummyQSerie()

    def getVisibleSeries(self):
        return [serie for serie in self.series() if serie.isVisible()]

    def getRange(self):
        try:
            return self.selectionDataHolder.getDummyQSerie().getStart(), self.selectionDataHolder.getDummyQSerie().getEnd()
        except IndexError:
            return 0

    def getStart(self):
        try:
            return self.selectionDataHolder.getDummyQSerie().getStart()
        except IndexError:
            return 0

    def getEnd(self):
        try:
            return self.selectionDataHolder.getDummyQSerie().getEnd()
        except IndexError:
            return 0

    def getScrollSpeed(self):
        return self._scrollSpeed

######## Setters

    def setScrollSpeed(self, scrollspeed):
        self._scrollSpeed = scrollspeed

######## Series modifier

    def setRange(self, start, end):
        self.selectionDataHolder.setRange(start, end)
        self.resetZoom()
        scope.window.updateChildren()

######## View modifiers

    def getZoomRange(self):
        return scope.leftDock.widget().startBox.value(), scope.leftDock.widget().endBox.value()

    def setZoom(self, start, end):
        firstPoint = self.mapToPosition(QtCore.QPoint(start, 0), self.selectionDataHolder.getDummyQSerie())
        lastPoint = self.mapToPosition(QtCore.QPoint(end, 0), self.selectionDataHolder.getDummyQSerie())
        area = self.plotArea()
        self.zoomIn(QtCore.QRectF(firstPoint.x(), area.y(), lastPoint.x() - firstPoint.x(), area.height()))

    def resetZoom(self):
        self.setZoom(self.getStart(), self.getEnd())

    def zoomReset(self):
        """Override the inherited method"""
        self.resetZoom()

######## Toggle actions

    def toggleSerieVisiblity(self, key):
        visibleSeries = scope.rightDock.widget().getVisibleSectionSeries()
        if int(key) > len(visibleSeries):
            return
        visibleSeries[int(key) - 1].toggleVisible()

        # Trigger move event after toggle to ensure current text of focusValueTextItem will change
        c = self.cursor()
        c.setPos(c.pos().x()+1, c.pos().y())
        c.setPos(c.pos().x()-1, c.pos().y())
        scope.rightDock.widget().update()

    def toggleAnimatable(self):
        if self.animationOptions() == QChart.NoAnimation:
            self.setAnimationOptions(QChart.SeriesAnimations)
        else:
            self.setAnimationOptions(QChart.NoAnimation)

    def toggleProperties(self):
        if scope.rightDock.isVisible():
            scope.rightDock.hide()
        else:
            scope.rightDock.show()

    def toggleLeftWidget(self):
        if scope.leftDock.isVisible():
            scope.leftDock.hide()
        else:
            scope.leftDock.show()

    def toggleXAxis(self, state):
        self.axisX(self.series()[0]).setVisible(state)

######## Update actions

    def updateChildren(self):
        self.updateAxes()

    def scaleChangedFun(self):
        print("scaleChanged")

    def geometryChangedFun(self):
        print("geometryChanged")

    def updateAxisExtremes(self):
        # self.minY = min(min(x) for x in self.ydata)
        # self.maxY = max(max(x) for x in self.ydata)
        if len([serie for serie in self.series() if serie.isVisible()]) > 0:
            realMinY = min([serie.min() for serie in self.series() if serie.isVisible()])
            realMaxY = max([serie.max() for serie in self.series() if serie.isVisible()])

            minY, maxY = self._calculateAxisSize(realMinY, realMaxY)

            if minY == self.minY and maxY == self.maxY:
                # The axes does not need to be updated
                return False

            self.minY, self.maxY = minY, maxY

        else:
            self.minY = -10
            self.maxY = 10
        
        return True

    def _calculateAxisSize(self, minimum, maximum):
        yMinReserve = minimum*getattr(scope.settings, "YAxisReserve", 10)/100
        yMaxReserve = maximum*getattr(scope.settings, "YAxisReserve", 10)/100
        base = getattr(scope.settings, "YAxisRound", 10)  # round to this number

        if minimum <= 0:
            calcMin = int(base * math.floor(float(minimum + yMinReserve)/base))
        else:
            calcMin = 0

        if maximum >= 0:
            calcMax = int(base * math.ceil(float(maximum + yMaxReserve)/base))
        else:
            calcMax = 0

        return calcMin, calcMax

    def updateAxes(self):
        if len(self.series()) == 0:
            # Return if series not exist in the chart
            return

        # IDEA: make a setting to turn on/edit 10% Y reserve
        if not self.updateAxisExtremes():
            # If the update was not necessary, do not recreate the axes
            return

        axisX = QValueAxis()
        axisY = QValueAxis()
        if self.series()[0].attachedAxes():
            axisX = self.series()[0].attachedAxes()[0]
            axisY = self.series()[0].attachedAxes()[1]

        axisY.setMin(self.minY)
        axisY.setMax(self.maxY)

        axisX.setRange(self.series()[0].getStart(), self.series()[0].getEnd())
        axisX.hide()

        for serie in self.series():
            if len(serie.attachedAxes()) == 0:
                self.setAxisX(axisX, serie)
                self.setAxisY(axisY, serie)
