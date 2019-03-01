from PyQt5.QtGui import QKeySequence
from Alames import scope

"""
The main keymap configuration file for window.py

Define actions in the functions below and bind them to a shortcut in keydict
"""

######## Dictionary for keyboard shortcut binding

keydict = {
    "o": "open",
    "q": "exit",
    "ctrl+q": "exit",

    "f1": "help",
    "f12": "about",

    "ctrl+1": "toggle1",
    "ctrl+2": "toggle2",
    "ctrl+3": "toggle3",

    "t": "test",
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

def help():
    scope.window.helpWidget.show()
    scope.window.helpWidget.move(scope.window.frameGeometry().center() - scope.window.helpWidget.rect().center())

def about():
    scope.window.aboutWidget.show()
    scope.window.aboutWidget.move(scope.window.frameGeometry().center() - scope.window.aboutWidget.rect().center())

#### Workspace toggle

def toggle1():
        scope.window.chartView.setVisible(
            not scope.window.chartView.isVisible())


def toggle2():
        scope.window.phasorView.setVisible(
            not scope.window.phasorView.isVisible())


def toggle3():
        scope.window.exportWidget.setVisible(
            not scope.window.exportWidget.isVisible())
