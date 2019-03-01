from Alames.importer import *

from Alames import scope

from Alames.window import Window

class Alames(QApplication):
    VERSION = "1.3-r13"

    def __init__(self, argv):
        super(Alames, self).__init__(argv)

        if platform.uname().system == "Linux" and not getattr(scope.settings, "FusionOnLinux", False):
            self.launch(False)
        else:
            self.launch(getattr(scope.settings, "Fusion", True))

    def version(self):
        return self.VERSION

    def launch(self, fusion=True, equalizeBG=False):
        if fusion: # needs to be applied before QApp init
            self.setFusion()
            self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        
        if equalizeBG: # in case it would look ugly..
            palette = self.palette()
            palette.setColor(QtGui.QPalette.Base, palette.color(QtGui.QPalette.Window))
            self.setPalette(palette)

        self.setApplicationDisplayName("Alames")
        # self.setWindowIcon(QtGui.QIcon("icons/main.png"))
        QtGui.QFontDatabase.addApplicationFont(os.path.join(os.path.join(os.path.dirname(__file__), "fonts"), "Gidole-Regular.ttf"))
        self.setFont(QtGui.QFont("Gidole"))
        w = Window()
        w.show()
        w.windowHandle().setScreen(self.screens()[-1])
        # w.setGeometry(self.screens()[-1].availableGeometry())
        w.setWindowState(QtCore.Qt.WindowMaximized)
        sys.exit(self.exec_())

    def setFusion(self):
        self.setStyle("fusion")

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(49, 54, 59))
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(239, 240, 241))
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(35, 38, 41))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(49, 54, 59))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(49, 54, 59))
        palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(239, 240, 241))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(239, 240, 241))
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(49, 54, 59))
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(239, 240, 241))
        palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(41, 128, 185))

        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(61, 174, 233))
        palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(239, 240, 241))

        self.setPalette(palette)
