from Alames.importer import *

from Alames.basewidget import BaseWidget
from Alames.generated import ui_leftwidget

from Alames import scope

class LeftWidget(BaseWidget, ui_leftwidget.Ui_LeftWidget):
    """
    Purpose: relative positioning of internal labels
    Creates a widget inside MainWindow which is shared for max 3 widgets
    Same lvl as chartview > an object from this class is created in Chart
    """

    exportTriggered = QtCore.pyqtSignal()

######## Widget setup

    def setup(self):
        """
        Args: ()
        Setup widget Ui elements
        """
        super(LeftWidget, self).setup()

        self.endBox.setMinimum(self.chart.getStart()+1)
        self.endBox.setMaximum(self.chart.getEnd())
        self.startBox.setMinimum(self.chart.getStart())
        self.startBox.setMaximum(self.chart.getEnd()-1)

        self._resetScrollSpeed()

    def _connectSlots(self):
        """
        Args: ()
        Connect signals to slots (happend only once)
        """
        super(LeftWidget, self)._connectSlots()

        self.startBox.valueChanged.connect(self.updateChartRange)
        self.endBox.valueChanged.connect(self.updateChartRange)
        self.resetButton.clicked.connect(self.resetRange)

        self.speedSlider.valueChanged.connect(self._updateScrollSpeed)
        self.speedSliderValueButton.clicked.connect(self._resetScrollSpeed)

        self.exportButton.clicked.connect(self.exportTriggered.emit)

        self.showXCheckBox.toggled.connect(scope.chart.toggleXAxis)

######## Update Actions

    def update(self):
        """
        Args: ()
        Update all values of Ui elements
        """
        super(LeftWidget, self).update()

        self.startBox.setValue(self.chart.getStart())
        self.endBox.setValue(self.chart.getEnd())

        self._updateScrollSpeed()

    def updateChartRange(self):
        """
        Args: ()
        Update chart zoom
        """
        self.chart.setZoom(self.startBox.value(), self.endBox.value())

    def resetRange(self):
        """
        Args: ()
        Reset range of chart and value of Ui elements
        """
        self.startBox.setValue(self.chart.getStart())
        self.endBox.setValue(self.chart.getEnd())
        self.chart.zoomReset()

    def updateValuesFromChart(self):
        """
        Args: ()
        Update box values after e.g. rubberband zoom change
        """
        plotArea = self.chart.plotArea()
        startX = self.chart.mapToValue(QtCore.QPointF(plotArea.x(), plotArea.y()), self.chart.series()[0]).x()
        endX = self.chart.mapToValue(QtCore.QPointF(plotArea.x() + plotArea.width(), plotArea.y()), self.chart.series()[0]).x()
        self.startBox.setValue(round(startX))
        self.endBox.setValue(round(endX))

    def _updateScrollSpeed(self):
        self.speedSliderValueButton.setText(str(self.speedSlider.value()) + "px")
        self.chart.setScrollSpeed(self.speedSlider.value())

    def _resetScrollSpeed(self):
        self.speedSlider.setValue(getattr(scope.settings, "DefaultScrollSpeed", 10))
