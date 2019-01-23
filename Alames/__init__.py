import sys, os, glob
from PyQt5 import uic

def genUi():
        for uiFileName in glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), "forms"), "*.ui")):
            pyFileName = os.path.join(os.path.join(os.path.dirname(__file__), "generated"), "ui_" + os.path.basename(uiFileName).split(".")[0] + ".py")
            os.makedirs(os.path.dirname(pyFileName), exist_ok=True)
            if os.path.isfile(pyFileName) == False or os.path.getmtime(uiFileName) > os.path.getmtime(pyFileName):
                with open(pyFileName, "w") as f:
                    uic.compileUi(uiFileName, f)
                    print("compiled " + pyFileName)

genUi()

from Alames.alames import Alames

