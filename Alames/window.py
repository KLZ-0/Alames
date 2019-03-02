#!/usr/bin/python

from Alames.importer import *

from Alames import scope
from Alames.generated.ui_mainwindow import Ui_MainWindow
from Alames.generated.ui_aboutwidget import Ui_AboutWidget
from Alames.generated.ui_helpwidget import Ui_HelpWidget

from Alames.config.keymaps import windowkeymap

from Alames import chart

class Window(QMainWindow, Ui_MainWindow):
    """
    Purpose: setup and modify the QMainWindow
    Manages the whole window except for the charting subsystem which is managed by Chart.
    Initializes Chart as its own property
    """

    _shortcuts = []

    def __init__(self):
        super(Window, self).__init__()
        scope.window = self

        self.setupUi(self)
        self.centralWidget.hide()
        self.rightDock.hide()
        self.leftDock.hide()
        self.loaderDock.hide()
        self.rightDock.widget().loaded.connect(self.loaderDock.widget().setup)
        self.leftDock.widget().exportTriggered.connect(self.exportWidget.toggleVisible)

        # Temporary
        self.phasorView.hide()
        self.exportWidget.hide()

        #### Assign scope
        scope.errorPopup = self.errorPopup
        scope.chartView = self.chartView
        scope.rightDock = self.rightDock
        scope.centralWidget = self.centralWidget
        scope.leftDock = self.leftDock
        scope.loaderDock = self.loaderDock

        self.setWindowTitle("Alames")
        self.setAcceptDrops(True)

        self.aboutWidget = QWidget()
        QShortcut(QtGui.QKeySequence.Quit, self.aboutWidget, self.aboutWidget.close)
        self.aboutWidget.ui = Ui_AboutWidget()
        self.aboutWidget.ui.setupUi(self.aboutWidget)

        self.helpWidget = QWidget()
        QShortcut(QtGui.QKeySequence.Quit, self.helpWidget, self.helpWidget.close)
        self.helpWidget.ui = Ui_HelpWidget()
        self.helpWidget.ui.setupUi(self.helpWidget)
        self.helpWidget.ui.label.setText(
            self.helpWidget.ui.label.text() + self.shortcutsToStr())
        

        # self.initLabel = QLabel("Drag & Drop a CSV file, or press:\n\nO - to open and load data\n\nS - to draw the file contents into a chart\n\nQ - to quit", self)
        self.initLabel = QLabel("Drag & Drop a CSV file or press O to open one", self)
        self.initLabel.setAlignment(QtCore.Qt.AlignCenter)
        f = self.initLabel.font()
        f.setPointSize(24)
        self.initLabel.setFont(f)

        self._setupShortcuts()

    def shortcutsToStr(self):
        basestr = ""
        for keymapmodule in self.loadKeymaps():
            basestr += "".join(["-" for i in range(20)]) + "<br>"
            basestr += "= " + keymapmodule.__name__.split(".")[-1] + ".py<br>"
            for key, action in keymapmodule.keydict.items():
                basestr += str(action) + ": " + str(key).upper() + "<br>"
        return basestr

    def loadKeymaps(self):
        keymaps = []
        for module in pkgutil.iter_modules([os.path.dirname(__file__) + "/config/keymaps"]):
            if not module.name.startswith('__'):
                keymaps.append(importlib.import_module("Alames.config.keymaps." + module.name))
        return keymaps

######## Update methods

    def updateChildren(self):
        self.rightDock.widget().update()
        self.leftDock.widget().update()
        self.chartView.chart().updateChildren()

######## Open file methods

    def openFile(self):
        f = self.getOpenFile("CSV files (*.csv *.csv.xz)")
        if f == None:
            return

        timer = QtCore.QElapsedTimer()
        timer.start()
        if self.createChart(f):
            self.statusBar().showMessage("Chart loaded in " + str(timer.elapsed()) + " milliseconds from " + f, getattr(scope.settings, "StatusbarMessageTimeout", 0)*1000)
        else:
            self.statusBar().showMessage("Chart load failed in " + str(timer.elapsed()) + " milliseconds from " + f, getattr(scope.settings, "StatusbarMessageTimeout", 0)*1000)

    def createChart(self, csvFile):
        if getattr(scope, "chart", False) and not scope.chart.property("deceased"):
            oldchart = scope.chart
            oldchart.setProperty("deceased", True)
            oldchart.deleteLater()

        scope.chart = chart.Chart() # FIXME: Two functions
        if not scope.chart.constructChart(csvFile): # FIXME: Two functions
            return False
        scope.chartView.setChart(scope.chart)
        self.rightDock.widget().setChart(scope.chart)
        self.leftDock.widget().setChart(scope.chart)
        self.exportWidget.setChart(scope.chart)

        self.initLabel.hide()
        scope.centralWidget.show()
        scope.rightDock.show()
        scope.loaderDock.show()
        scope.leftDock.show()
        scope.chartView.show()

        # send signal to window->phasorWidget to update
        self.phasorView.scene().setData(scope.chart.selectionDataHolder, {"show-current-circle": False, "current-color": "#ff0000", "voltage-color": "#0000ff"})

        # scope.chart.chartView = scope.chartView

        # needed when opening a new file
        self.updateChildren()

        return True

    def getOpenFile(self, typeFilter="CSV files (*.csv *.csv.xz)"):
        f = QFileDialog.getOpenFileName(self, "Open..", str(
            Path(__file__).parents[1]), typeFilter)

        # If windows sometimes problems with the encoding happen
        fileName = f[0]
        if platform.uname().system != "Linux":
            fileName = fileName.encode("utf-8").decode("utf-8", "replace")

        # Extract suffixes from filter
        fileSuffixes = f[1][f[1].find("(")+1:f[1].find(")")].split()
        fileSuffixes = [suffix.lstrip("*") for suffix in fileSuffixes]

        # Test if exists
        if not Path(fileName).is_file() or not fileName.endswith(tuple(fileSuffixes)):
            return None

        return fileName

    def getSaveFile(self, typeFilter="Images (*.png *.jpg)"):
        f = QFileDialog.getSaveFileName(self, "Save as..", str(
            Path(__file__).parents[1]), typeFilter)

        # If windows sometimes problems with the encoding happen
        fileName = f[0]
        if platform.uname().system != "Linux":
            fileName = fileName.encode("utf-8").decode("utf-8", "replace")

        # Test whether the returned filename is not empty
        if fileName == "":
            return None

        # Extract suffixes from filter
        fileSuffixes = f[1][f[1].find("(")+1:f[1].find(")")].split()
        fileSuffixes = [suffix.lstrip("*") for suffix in fileSuffixes]

        # If returned filename does not have a suffix, append the first one (the default)
        if not fileName.endswith(tuple(fileSuffixes)):
            fileName += fileSuffixes[0]

        return fileName

    def errorPopup(self, title, text=None, details=None, level=0):
        if level < 0 or level > 2:
            level = 2

        errorLevels = {
            0: QMessageBox.Information,
            1: QMessageBox.Warning,
            2: QMessageBox.Critical,
        }
        self.messageBox = getattr(self, "messageBox", QMessageBox())
        self.messageBox.setIcon(errorLevels[level])

        self.messageBox.setWindowTitle(str(title))
        self.messageBox.setText(str(title))
        if text != None:
            self.messageBox.setInformativeText(str(text))
        if details != None:
            self.messageBox.setDetailedText(str(details))

        self.messageBox.show()

######## Shortcut binding

    def _setupShortcuts(self):
        for key, method in windowkeymap.keydict.items():
            self._shortcuts.append(QShortcut(QtGui.QKeySequence(key), self, getattr(windowkeymap, method, scope.shortcutBindError)))

######## Actions

    def hideUi(self):
        self.chartView.hide()
        self.rightDock.hide()
        self.leftDock.hide()
        self.loaderDock.hide()
        self.phasorView.hide()
        self.exportWidget.hide()

        self.initLabel.show()

######## Event handlers

    def dragEnterEvent(self, event):
        super(Window, self).dragEnterEvent(event)
        if event.mimeData().text()[-4:].lower() == ".csv":
            event.acceptProposedAction()

    def dropEvent(self, event):
        super(Window, self).dropEvent(event)
        self.createChart(event.mimeData().text())

    def resizeEvent(self, event):
        super(Window, self).resizeEvent(event)
        self.initLabel.setGeometry(self.contentsRect())

    def keyPressEvent(self, event):
        super(Window, self).keyPressEvent(event)
        key = event.text()
        if getattr(scope, "chart", False) and key in ["1","2","3","4","5","6","7","8","9"]:
            scope.chart.toggleSerieVisiblity(key)
