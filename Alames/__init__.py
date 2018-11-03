import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont

from Alames import main

def launch():
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Alames")
    # app.setWindowIcon(QtGui.QIcon("icons/main.png"))
    QFontDatabase.addApplicationFont("fonts/Gidole-Regular.ttf")
    app.setFont(QFont("Gidole"))
    ex = main.Window(app)
    sys.exit(app.exec_())
