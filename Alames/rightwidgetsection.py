import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

from Alames.generated.ui_rightwidgetsection import Ui_rightWidgetSection

class RightWidgetSection(QWidget, Ui_rightWidgetSection):
    def __init__(self, parent, serie):
        super(RightWidgetSection, self).__init__(parent)
        self.setupUi(self)
        self.serie = serie

        self.nOfLines = 4
        self.nameLineEdit.setText(serie.name())
        self.nameLineEdit.editingFinished.connect(self.applySettings)
        self.colorValueLabel.setText(serie.color().name())
        pixRect = QtGui.QPixmap(64,64)
        pixRect.fill(serie.color())
        self.colorPickButton.setIcon(QtGui.QIcon(pixRect))
        self.colorPickButton.pressed.connect(self.pickSerieColor)
        self.visibleCheckBox.setChecked(serie.isVisible())
        self.visibleCheckBox.toggled.connect(self.setSerieVisiblity)

######## Update Actions

    def updateVisibleBox(self):
        self.visibleCheckBox.setChecked(self.serie.isVisible())

    def updateAll(self):
        self.updateVisibleBox()
        self.nameLineEdit.setText(self.serie.name())
        self.colorValueLabel.setText(self.serie.color().name())
        pixRect = QtGui.QPixmap(64,64)
        pixRect.fill(self.serie.color())
        self.colorPickButton.setIcon(QtGui.QIcon(pixRect))

######## Actions

    def setSerieVisiblity(self):
        if self.visibleCheckBox.isChecked():
            self.serie.show()
        else:
            self.serie.hide()

    def pickSerieColor(self):
        if self.colorPickButton.isDown():
            color = QColorDialog.getColor(QtGui.QColor(self.colorValueLabel.text()))
            self.colorValueLabel.setText(color.name())
            self.applySettings()

    def applySettings(self):
        self.serie.setName(self.nameLineEdit.text())
        try:
            self.serie.setColor(QtGui.QColor(self.colorValueLabel.text()))
            pixRect = QtGui.QPixmap(64,64)
            pixRect.fill(self.serie.color())
            self.colorPickButton.setIcon(QtGui.QIcon(pixRect))
        except ValueError:
            pass

######## Event handlers

    def resizeEvent(self, event):
        super(RightWidgetSection, self).resizeEvent(event)
