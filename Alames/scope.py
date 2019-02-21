"""Definition of variables accessible trought the scope"""

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
import sys, logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def debug(s):
    logging.debug(str(s))

def log(s):
    logging.info(str(s))
