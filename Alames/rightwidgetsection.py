import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis

class RightWidgetSection(QWidget):
    def __init__(self, parent, serie):
        super(RightWidgetSection, self).__init__(parent)
        self.serie = serie

        self.nOfLines = 4
        self.nameLabel = QLabel("Name: ", self)
        self.nameLineEdit = QLineEdit(serie.name(), self)
        self.nameLineEdit.editingFinished.connect(self.applySettings)
        self.colorLabel = QLabel("Color: ", self)
        self.colorValueLabel = QLabel(serie.color().name(), self)
        self.colorPickButton = QPushButton(self)
        pixRect = QtGui.QPixmap(64,64)
        pixRect.fill(serie.color())
        self.colorPickButton.setIcon(QtGui.QIcon(pixRect))
        self.colorPickButton.pressed.connect(self.pickSerieColor)
        self.visibleToggleButton = QCheckBox("Visible", self)
        self.visibleToggleButton.setChecked(serie.isVisible())
        self.visibleToggleButton.toggled.connect(self.setSerieVisiblity)
        self.hrLine = QLabel("<hr>", self)

######## Update Actions

    def updateVisibleBox(self):
        self.visibleToggleButton.setChecked(self.serie.isVisible())

    def updateAll(self):
        self.updateVisibleBox()
        self.nameLineEdit.setText(self.serie.name())
        self.colorValueLabel.setText(self.serie.color().name())
        pixRect = QtGui.QPixmap(64,64)
        pixRect.fill(self.serie.color())
        self.colorPickButton.setIcon(QtGui.QIcon(pixRect))

######## Actions

    def setSerieVisiblity(self):
        if self.visibleToggleButton.isChecked():
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
        itemHeight = self.nameLineEdit.height()

        self.nameLabel.setGeometry(0, 0, self.width()/3, itemHeight)
        self.nameLineEdit.setGeometry(self.width()/3, 0, self.width()/1.5, itemHeight)

        self.colorLabel.setGeometry(0, itemHeight, self.width()/3, itemHeight)
        self.colorValueLabel.setGeometry(self.width()/3, itemHeight, self.width()/1.5, itemHeight)
        self.colorPickButton.setGeometry(self.width()-itemHeight, itemHeight, itemHeight, itemHeight)
        self.visibleToggleButton.setGeometry(0, itemHeight*2, self.width(), itemHeight)

        self.hrLine.setGeometry(0, self.height()-itemHeight/2, self.width(), itemHeight)
