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

    def setup(self):
        super(ExportWidget, self).setup()
        """
        Args: ()
        Setup widget Ui elements
        """

        # FIXME: Enable if fixed
        self.exportButton.clicked.connect(self.startExport)

    def startExport(self):
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
            dataHolder.export(fileName, [serie.property("number") for serie in scope.chart.getVisibleSeries()])

        self.filenameLabel.setText("Export saved to <a href=" + fileName +">" + fileName + "</a>")
