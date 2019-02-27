from Alames.importer import *

from Alames.phasorscene import PhasorScene

class PhasorView(QGraphicsView):
    """Phasor Diagram View"""

    def __init__(self, parent):
        super(PhasorView, self).__init__(parent)
        self.setScene(PhasorScene())
        self.scene().redrawn.connect(self.centerScene)

    def reDraw(self):
        """Just a wrapper method for the scene reDraw"""
        self.scene().reDraw()

    def centerScene(self):
        self.centerOn(self.scene().sceneRect().center())

    def resizeEvent(self, event):
        super(PhasorView, self).resizeEvent(event)
