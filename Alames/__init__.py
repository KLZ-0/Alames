import sys, os, glob
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont, QPalette, QColor
from PyQt5 import uic

def genUi():
    for uiFileName in glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), "forms"), "*.ui")):
        pyFileName = os.path.join(os.path.join(os.path.dirname(__file__), "generated"), "ui_" + os.path.basename(uiFileName).split(".")[0] + ".py")
        os.makedirs(os.path.dirname(pyFileName), exist_ok=True)
        if os.path.isfile(pyFileName) == False or os.path.getmtime(uiFileName) > os.path.getmtime(pyFileName):
            with open(pyFileName, "w") as f:
                uic.compileUi(uiFileName, f)
                print("compiled " + pyFileName)

genUi()

from Alames.window import Window

VERSION = "1.1-r2"

def setStyle():
    QApplication.setStyle("fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53,53,53))
    palette.setColor(QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QPalette.Base, QColor(25,25,25))
    palette.setColor(QPalette.AlternateBase, QColor(53,53,53))
    palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QPalette.Text, QtCore.Qt.white)
    palette.setColor(QPalette.Button, QColor(53,53,53))
    palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))

    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)

    QApplication.setPalette(palette)

def launch(fusion=True):
    if fusion: # needs to be applied before QApp init
        setStyle()
    app = QApplication(sys.argv)
    if fusion: # needs to be applied after QApp init
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    app.setApplicationDisplayName("Alames")
    # app.setWindowIcon(QtGui.QIcon("icons/main.png"))
    QFontDatabase.addApplicationFont(os.path.join(os.path.join(os.path.dirname(__file__), "fonts"), "Gidole-Regular.ttf"))
    app.setFont(QFont("Gidole"))
    w = Window()
    w.show()
    w.windowHandle().setScreen(app.screens()[-1])
    w.setGeometry(app.screens()[-1].availableGeometry())
    w.setWindowState(QtCore.Qt.WindowMaximized)
    sys.exit(app.exec_())

def version():
    return VERSION
