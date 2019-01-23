import sys, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont, QPalette, QColor

from Alames.window import Window

class Alames(QApplication):
    VERSION = "1.1-r4"

    def __init__(self, argv):
        super(Alames, self).__init__(argv)

        self.launch()

    def version(self):
        return self.VERSION

    def launch(self, fusion=True):
        if fusion: # needs to be applied before QApp init
            self.setFusion()
            self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

        self.setApplicationDisplayName("Alames")
        # self.setWindowIcon(QtGui.QIcon("icons/main.png"))
        QFontDatabase.addApplicationFont(os.path.join(os.path.join(os.path.dirname(__file__), "fonts"), "Gidole-Regular.ttf"))
        self.setFont(QFont("Gidole"))
        w = Window()
        w.show()
        w.windowHandle().setScreen(self.screens()[-1])
        w.setGeometry(self.screens()[-1].availableGeometry())
        w.setWindowState(QtCore.Qt.WindowMaximized)
        sys.exit(self.exec_())

    def setFusion(self):
        self.setStyle("fusion")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(49, 54, 59))
        palette.setColor(QPalette.WindowText, QColor(239, 240, 241))
        palette.setColor(QPalette.Base, QColor(35, 38, 41))
        palette.setColor(QPalette.AlternateBase, QColor(49, 54, 59))
        palette.setColor(QPalette.ToolTipBase, QColor(49, 54, 59))
        palette.setColor(QPalette.ToolTipText, QColor(239, 240, 241))
        palette.setColor(QPalette.Text, QColor(239, 240, 241))
        palette.setColor(QPalette.Button, QColor(49, 54, 59))
        palette.setColor(QPalette.ButtonText, QColor(239, 240, 241))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(41, 128, 185))

        palette.setColor(QPalette.Highlight, QColor(61, 174, 233))
        palette.setColor(QPalette.HighlightedText, QColor(239, 240, 241))

        self.setPalette(palette)
