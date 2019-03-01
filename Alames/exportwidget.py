from Alames.importer import *

from Alames.basewidget import BaseWidget

from Alames import scope

class ExportWidget(BaseWidget):
    def __init__(self, parent=None):
        super(ExportWidget, self).__init__(parent)

    def toggle(self):
        self.setVisible(not self.isVisible())
