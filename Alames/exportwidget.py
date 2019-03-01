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
        # self.exportButton.clicked.connect(self.startExport)

    def startExport(self):
        radios = self.findChildren(QRadioButton)
        fileName = scope.window.getSaveFile("CSV (*.csv)")
        dataHolder = self.chart.selectionDataHolder # TODO: Make a method in chart to return the default dataholder

        print(DataFrame(zip(*dataHolder.YData())))
        # TODO: Add also XDATA as first column to CSV
        # print(radios)
        # TODO: Continue here
