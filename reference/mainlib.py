import os, json
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis

import override
import phasor
import soul
import actions
import sinlib

def setupAll(self, app):
    self.setGeometry(app.desktop().availableGeometry())
    self.move(0, 0)
    self.setWindowState(QtCore.Qt.WindowMaximized)
    self.setWindowTitle("KLZ analyser management console")
    self.setWindowIcon(QtGui.QIcon("./src/main.png"))

    loadSettings(self)
    self.previousCalibration = self.settings["calibration"]
    try:
        self.colors = {"voltage" : self.settings["color"]["voltage"], "current" : self.settings["color"]["current"]} # chart colors
    except KeyError:
        QErrorMessage(self).showMessage("Failed to load colors.. invalid number of curves")
        print("Failed to load colors.. invalid number of curves")
    # defining upper menu
    self.menubar = QMenuBar(self)

    # file menu under menubar
    self.menuFile = QMenu(self.menubar)
    self.setMenuBar(self.menubar)
    self.menuFile.setTitle("File")

    # status bar - on the bottom
    self.statusbar = QStatusBar(self)
    self.setStatusBar(self.statusbar)

    # main widget
    self.mainwidget = QWidget(self)
    self.setCentralWidget(self.mainwidget)

    # tab widget
    self.tabmenu = QTabWidget(self)
    self.tabmenu.setTabPosition(QTabWidget.South)

    self.tab = [QWidget(self), QWidget(self)]
    self.tabmenu.addTab(self.tab[0], "Chart")
    self.tabmenu.addTab(self.tab[1], "Other")

    # under file menu >> open
    self.actionOpen = QAction(self)
    self.actionOpen.triggered.connect(lambda: soul.openfl(self))
    self.actionOpen.setShortcut("Ctrl+O")
    self.actionOpen.setText("Open")

    # under file menu >> record
    self.record = QAction(self)
    self.record.triggered.connect(lambda: self.recordDialog.show())
    self.record.setShortcut("Ctrl+R")
    self.record.setText("Record")

    # remove series
    self.rmseries = QAction(self)
    self.rmseries.triggered.connect(lambda: actions.rmser(self))
    self.rmseries.setShortcut("Ctrl+Shift+R")
    self.rmseries.setText("Remove All Series")

    # under file menu >> settings
    self.actionSettings = QAction(self)
    self.actionSettings.triggered.connect(lambda: self.settingsDialog.show())
    self.actionSettings.setText("Settings")

    # under file menu >> settings
    self.actionCalibrate = QAction(self)
    self.actionCalibrate.triggered.connect(lambda: self.calibrationDialog.show())
    self.actionCalibrate.setText("Calibrate voltage")

    # under file menu >> quit
    self.actionQuit = QAction(self)
    self.actionQuit.triggered.connect(self.exit)
    self.actionQuit.setShortcut("Ctrl+Q")
    self.actionQuit.setText("Quit")

    # positions of actions in file menu
    self.menuFile.addAction(self.actionOpen)
    self.menuFile.addAction(self.record)
    self.menuFile.addAction(self.actionCalibrate)
    self.menuFile.addSeparator()
    self.menuFile.addAction(self.rmseries)
    self.menuFile.addSeparator()
    self.menuFile.addAction(self.actionSettings)
    self.menuFile.addAction(self.actionQuit)

    # menubar info
    self.menubar.addAction(self.menuFile.menuAction())

    # axis = QValueAxis()
    # axis.setLabelFormat("%i")
    # chart.addAxis(axis, Qt.AlignLeft)
    # series.attachAxis(axis)

    self.chart = QChart()
    self.chart.setAnimationOptions(QChart.SeriesAnimations)
    self.chart.legend().hide()
    self.chart.setAcceptHoverEvents(True)

    self.chart_view = override.view(self.chart, self.tab[0], self, app)
    self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
    self.chart_view.lower()

    self.timeLineChart = QChart()
    self.timeLineChart.legend().hide()
    self.timeLineChart.setAcceptHoverEvents(True)

    self.timeLineChartView = QChartView(self.timeLineChart, self)
    self.timeLineChartView.setRenderHint(QtGui.QPainter.Antialiasing)
    self.timeLineChartView.lower()

    self.state = False

    self.date_show = QLabel(self.tabmenu)
    self.timeInfoLabel = QLabel(self)
    self.timeInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
    self.timeInfoLabel.hide()

    self.rmsLabel = QLabel(self)
    self.rmsLabel.setAlignment(QtCore.Qt.AlignRight)
    self.rmsLabel.hide()
    setBoldFont(self.rmsLabel)

    self.rmsValueLabel = QLabel(self)
    self.rmsValueLabel.setAlignment(QtCore.Qt.AlignLeft)
    self.rmsValueLabel.hide()
    self.baseRmsText = ["RMS Current: ", "RMS Voltage: ", "Active Power: ", "Reactive Power: ", "Apparent Power: ", "Power Factor: "]

    self.rmsLabel.setStyleSheet("background-color: #f0f0f0; padding-right: 20px; border-bottom: 3px solid #000000;")
    self.rmsValueLabel.setStyleSheet("background-color: #f0f0f0; border-bottom: 3px solid #000000;")

    self.date_picker = QComboBox(self)
    self.date_picker.hide()
    self.date_picker.currentTextChanged.connect(self.displaynew)

    self.recordDialog = override.recordWindow(self)
    self.settingsDialog = override.settingsWindow(self)
    self.calibrationDialog = override.calibrationWindow(self)

    self.openReadingButton = QPushButton("Open reading file", self)
    self.openReadingButton.clicked.connect(lambda: soul.openfl(self))

    self.selectCurves = override.curveGroupBox("Select curves", self)
    self.selectCurves.hide()
    self.selectCurvesOptions = []

    self.phasorWidget = phasor.Diagram(self)
    self.phasorWidget.hide()

    # self.date_scene = QGraphicsScene(1000, 500, 100, 50, self)
    # self.view_date = QGraphicsView(self.date_scene, self)
    translate(self)

def translate(self):
    if self.settings["language"] == "Slovak":
        self.menuFile.setTitle("Súbor")
        self.actionOpen.setText("Otvoriť meranie")
        self.record.setText("Nové meranie")
        self.actionCalibrate.setText("Kalibrácia napätia")
        self.rmseries.setText("Zatvoriť meranie")
        self.actionSettings.setText("Nastavenia")
        self.actionQuit.setText("Zatvoriť aplikáciu")

        self.tabmenu.setTabText(0, "Graf")
        self.tabmenu.setTabText(1, "Iné")

        self.openReadingButton.setText("Otvoriť súbor merania")

        self.selectCurves.setTitle("Vyberte priebehy")
        self.baseRmsText = ["Prúd: ", "Napätie: ", "Činný Výkon: ", "Jalový Výkon: ", "Zdanlivý Výkon: ", "cosφ: "]

def resizeDynamicContent(self):
    soul.setDynamicGeometry(self)

def loadSettings(self):
    try:
        if os.path.isfile("config.json"):
            self.settings = json.load(open("config.json"))
        else:
            self.settings = reloadSettings("Error loading settings.. Created new config file", self)

        if validateSettings(self.settings) == False:
            self.settings = reloadSettings("Corrupted config file.. Created new config file", self)
    except:
        self.settings = reloadSettings("Unexpected exception - corrupted config file.. Created new config file", self)

def validateSettings(settings):
    required = ["language", "color", "dynamic-axis-scaling", "calibration", "show-current-circle"]
    for requirement in required:
        if requirement not in settings or settings[requirement] == "":
            return False
    return True

def reloadSettings(message, self):
    config = {"color": {"voltage": "#0000ff", "current": "#ff0000"}, "language": "English", "dynamic-axis-scaling": False, "show-current-circle": True, "calibration": 1}
    json.dump(config, open("config.json", "w"), sort_keys=True, indent=4, separators=(',', ': '))
    QErrorMessage(self).showMessage(message)
    return json.load(open("config.json"))

def seriesInChart(series, chart):
    if series in chart.series():
        return True
    else:
        return False

def setRmsLabel(ydata, lang, fi, powerDataSet, valueLabel, label, baseRmsText, units, translate):
    if len(ydata) == 1: cycles = 1
    else: cycles = len(baseRmsText)
    labelText = ""
    valueText = ""
    rmsData = []
    for data in ydata:
        rmsData.append(sinlib.calcRms(data))

    if len(ydata) > 1:
        if lang == "English":
            labelText += "Load Type: \n"
            if fi == 0:
                valueText += "Resistive\n"
            elif fi > 0:
                valueText += "Inductive\n"
            else:
                valueText += "Capacitive\n"
        elif lang == "Slovak":
            labelText += "Charakter záťaže: \n"
            if fi == 0:
                valueText += "Odporový\n"
            elif fi > 0:
                valueText += "Indukčný\n"
            else:
                valueText += "Kapacitný\n"
        rmsData += powerDataSet

    for i in range(cycles):
        labelText += baseRmsText[i] + "\n"
        valueText += str(rmsData[i]) + " " + units[translate[i]] + "\n"

    valueLabel.setText(valueText)
    label.setText(labelText)

def setBoldFont(label):
    font = label.font()
    font.setWeight(QtGui.QFont.DemiBold)
    label.setFont(font)
