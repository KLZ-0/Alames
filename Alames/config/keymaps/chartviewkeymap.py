from PyQt5.QtGui import QKeySequence
from Alames import scope

"""
The main keymap configuration file for chartview.py

Define actions in the functions below and bind them to a shortcut in keydict
"""

######## Dictionary for keyboard shortcut binding

keydict = {
    "s": "save",
}

######## Action definitions

#### miscellaneous

def save():
    scope.chartView.saveToFile()
