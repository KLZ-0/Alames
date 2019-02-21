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
        self.OpenGLCheckBox.setChecked(serie.useOpenGL())
        self.OpenGLCheckBox.toggled.connect(self.toggleOpenGL)

        # Enable default OpenGL
        # self.OpenGLCheckBox.setChecked(True)

######## Update Actions

    def updateVisibleBox(self):
        self.visibleCheckBox.setChecked(self.serie.isVisible())

    def update(self):
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

    def toggleOpenGL(self):
        if self.OpenGLCheckBox.isChecked():
            self.serie.setUseOpenGL(True)
        else:
            self.serie.setUseOpenGL(False)

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
