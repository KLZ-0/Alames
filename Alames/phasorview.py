import math
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from Alames.phasorscene import PhasorScene

class PhasorView(QGraphicsView):
    """Phasor Diagram View"""

    def __init__(self, parent):
        super(PhasorView, self).__init__(parent)
        self.setScene(PhasorScene())

    def resizeEvent(self, event):
        super(PhasorView, self).resizeEvent(event)
