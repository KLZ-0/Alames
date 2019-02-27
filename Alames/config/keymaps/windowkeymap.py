from PyQt5.QtGui import QKeySequence
from Alames import scope

"""
The main keymap configuration file for window.py

Define actions in the functions below and bind them to a shortcut in keydict
"""

######## Dictionary for keyboard shortcut binding

keydict = {
    "o" : "open",
    "q" : "exit",
    "ctrl+q" : "exit",

    "f12" : "about",

    "ctrl+1": "toggle1",
    "ctrl+2": "toggle2",
    "ctrl+3": "toggle3",
    "ctrl+4": "toggle4",

    "t" : "test",
}

def test():
    scope.log(getattr(scope.settings, "Debug", True))

######## Action definitions

#### miscellaneous

def open():
    scope.window.openFile()

def exit():
    scope.window.close()

#### F keys

def about():
    scope.window.aboutWidget.move(scope.window.frameGeometry().topLeft(
    ) + scope.window.frameGeometry().center() - scope.window.aboutWidget.geometry().center())
    scope.window.aboutWidget.show()

#### Workspace toggle

def toggle1():
        scope.window.chartView.setVisible(
            not scope.window.chartView.isVisible())


def toggle2():
        scope.window.phasorView.setVisible(
            not scope.window.phasorView.isVisible())


def toggle3():
        scope.window.holder1.setVisible(
            not scope.window.holder1.isVisible())

def toggle4():
        scope.window.holder2.setVisible(
            not scope.window.holder2.isVisible())
