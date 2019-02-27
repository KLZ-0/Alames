# Import global libraries

import os
import sys
import platform
import math
import traceback
import lzma
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView
from pathlib import Path
from datetime import datetime
from six import string_types
from pandas import read_csv
