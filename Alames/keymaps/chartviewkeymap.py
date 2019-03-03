from PyQt5.QtGui import QKeySequence
from Alames import scope

"""
The main keymap configuration file for chartview.py

Define actions in the functions below and bind them to a shortcut in keydict
"""

######## Dictionary for keyboard shortcut binding

keydict = {
    "s": "save",
    "a": "toggleAnimation",
    "p": "toggleProperties",
    "l": "toggleLeftWidget",
    "r": "resetZoom",
    "i": "testRange",
    "d": "filterAlamesOne",
    "e": "exportCSV",
    "x": "toggleXAxis",
}

######## Action definitions

#### miscellaneous

def save():
    scope.chartView.saveToFile()

def toggleAnimation():
    scope.chart.toggleAnimatable()

def toggleProperties():
    scope.chart.toggleProperties()

def toggleLeftWidget():
    scope.chart.toggleLeftWidget()

def resetZoom():
    scope.chart.zoomReset()

def testRange():
    scope.chart.setRange(100, 200)

def filterAlamesOne():
    scope.chart.filterAlamesOne()

def exportCSV():
    scope.window.exportWidget.toggleVisible()

def toggleXAxis():
    scope.leftDock.widget().showXCheckBox.toggle()
