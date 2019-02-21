from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

from Alames.generated.ui_loaderwidget import Ui_LoaderWidget

from Alames import scope

class LoaderWidget(QWidget, Ui_LoaderWidget):
    """
    Purpose: Select which RightWidgetSections to show in RightDock
    """

    _checkBoxes = []

    def __init__(self, parent=None):
        super(LoaderWidget, self).__init__(parent)

######## Widget setup

    def setup(self): 
        """
        Args: ()
        Setup chackboxes
        Called on RightWidget.loaded.emit()
        """

        self.setupUi(self)

        rightWidget = scope.rightDock.widget()
        rightWidget.sectionUpdated.connect(self._updateNames)
        targetLayout = self.scrollArea.widget().layout()
        
        # TODO: Do this to every DockWidget
        # Empty the container in case a new file is loaded
        self._checkBoxes = []

        for i in range(rightWidget.getSectionLen()):
            self._checkBoxes.append(QCheckBox(self))
            self._checkBoxes[-1].setChecked(rightWidget.isVisibleSectionByDefault(i))
            self._checkBoxes[-1].setText(rightWidget.getSectionName(i))
            self._checkBoxes[-1].stateChanged.connect(self._updateRightWidgetSectionVisibility)
            targetLayout.addWidget(self._checkBoxes[-1])

    def _updateRightWidgetSectionVisibility(self):
        rightWidget = scope.rightDock.widget()

        for i in range(rightWidget.getSectionLen()):
            rightWidget.setVisibleSection(i, self._checkBoxes[i].isChecked())

    def _updateNames(self):
        rightWidget = scope.rightDock.widget()

        for i in range(rightWidget.getSectionLen()):
            self._checkBoxes[i].setChecked(rightWidget.isVisibleSection(i))
            self._checkBoxes[i].setText(rightWidget.getSectionName(i))

            font = self._checkBoxes[i].font()
            font.setBold(rightWidget.isVisibleSectionSerie(i))
            font.setItalic(rightWidget.isVisibleSectionSerie(i))
            self._checkBoxes[i].setFont(font)
