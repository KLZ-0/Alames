import sys
"""Definition of variables accessible trought the scope"""

#### Application settings (loaded from user settings.py from the parent folder)
sys.path.append("..")
import settings

#### Main Window
global window

#### Widgets
global rightDock
global centralWidget
global leftDock
global loaderDock

#### Meta-Objects
global chartView

#### Objects
global chart

#### functions
global errorPopup

#### Debug
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def debug(s):
    if not getattr(settings, "Debug", True):
        return

    logging.debug(str(s))

def log(s):
    if not getattr(settings, "Debug", True):
        return

    logging.info(str(s))
