import sys, os, glob
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5 import uic

from Alames.window import Window

VERSION = "1.0-r1"

def genUi():
    for uiFileName in glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), "forms"), "*.ui")):
        pyFileName = os.path.join(os.path.join(os.path.dirname(__file__), "generated"), "ui_" + os.path.basename(uiFileName).split(".")[0] + ".py")
        os.makedirs(os.path.dirname(pyFileName), exist_ok=True)
        if os.path.isfile(pyFileName) == False or os.path.getmtime(uiFileName) > os.path.getmtime(pyFileName):
            with open(pyFileName, "w") as f:
                uic.compileUi(uiFileName, f)
                print("compiled " + pyFileName)

def launch():
    genUi()
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Alames")
    # app.setWindowIcon(QtGui.QIcon("icons/main.png"))
    QFontDatabase.addApplicationFont(os.path.join(os.path.join(os.path.dirname(__file__), "fonts"), "Gidole-Regular.ttf"))
    app.setFont(QFont("Gidole"))
    Window(app)
    sys.exit(app.exec_())

def version():
    return VERSION
