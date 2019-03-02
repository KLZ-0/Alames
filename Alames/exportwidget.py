from Alames.importer import *

from Alames.basewidget import BaseWidget
from Alames.generated.ui_exportwidget import Ui_ExportWidget

from Alames import scope

class ExportWidget(BaseWidget, Ui_ExportWidget):
    """
    Purpose: A widget for CSV exporting
    """

    def __init__(self, parent=None):
        super(ExportWidget, self).__init__(parent)

    def _connectSlots(self):
        super(ExportWidget, self)._connectSlots()
        """
        Args: ()
        Connect signals to slots (happend only once)
        """
        
        self.exportButton.clicked.connect(self.startExport)

    def startExport(self):
        if self.onlyVisibleRadio.isChecked() and len(scope.chart.getVisibleSeries()) == 0:
            scope.errorPopup("No series are visible!",
                             "Select at least one or choose 'Everything' in the export widget", level=2)
            return

        # File selection dialog
        fileName = scope.window.getSaveFile("CSV (*.csv)")
        if fileName == None:
            return
        
        # TODO: Make a method in chart to return the default dataholder
        if self.withModificationCheckBox.isChecked():
            dataHolder = self.chart.selectionDataHolder
        else:
            dataHolder = self.chart.overallDataHolder

        if self.everythingRadio.isChecked():
            dataHolder.export(fileName)
        elif self.onlyVisibleRadio.isChecked():  
            visibleNumbers = [serie.property("number") for serie in scope.chart.getVisibleSeries()]

            if self.sampleDurCheckBox.isChecked() and 0 not in visibleNumbers:
                visibleNumbers.insert(0, 0)
            dataHolder.export(fileName, visibleNumbers)

        self.filenameLabel.setText("Export saved to <a href=" + fileName +">" + fileName + "</a>")
