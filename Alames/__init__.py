import sys, os, glob, re, io
from PyQt5 import uic

def genUi():
    regex = re.compile(r"\.\.\/(icons)\/", re.IGNORECASE)
    for uiFileName in glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), "forms"), "*.ui")):
        pyFileName = os.path.join(os.path.join(os.path.dirname(__file__), "generated"), "ui_" + os.path.basename(uiFileName).split(".")[0] + ".py")
        os.makedirs(os.path.dirname(pyFileName), exist_ok=True)
        if os.path.isfile(pyFileName) == False or os.path.getmtime(uiFileName) > os.path.getmtime(pyFileName):
            with open(pyFileName, "w+") as f: # regex for translating resource path names
                buf = io.StringIO()
                uic.compileUi(uiFileName, buf)
                buf.seek(0)
                f.write(regex.sub(r"./Alames/\1/", buf.read()))

                print("compiled " + pyFileName)

genUi()

from Alames.alames import Alames
