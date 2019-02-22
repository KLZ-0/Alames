import os, sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QLineSeries, QValueAxis, QChart, QChartView, QDateTimeAxis, QValueAxis
import numpy

from Alames.generated.ui_rightwidgetsection import Ui_rightWidgetSection

class RightWidgetSection(QWidget, Ui_rightWidgetSection):

    updated = QtCore.pyqtSignal()

    _scaleMin = 0.01
    _scaleMax = 100

    def __init__(self, parent, serie):
        super(RightWidgetSection, self).__init__(parent)
        self.serie = serie
        self.serie.nameChanged.connect(self.update)

        self.setupUi(self)
        self.scaleSlider.valueChanged.connect(self._updateSerieScale)
        self._resetSerieScale()
        self.scaleValueButton.clicked.connect(self._resetSerieScale)

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

######## Getters

    def getName(self):
        return self.nameLineEdit.text()

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

        self.updated.emit()

######## Actions

    def setSerieVisiblity(self):
        if self.visibleCheckBox.isChecked():
            self.serie.show()
        else:
            self.serie.hide()
        self.updated.emit()

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
            self.updated.emit()
        except ValueError:
            pass

    def _updateSerieScale(self, value):
        self.scaleValueButton.setText(str(self._mapSliderScaleToReal(value)))
        self.serie.setLineScale(self._mapSliderScaleToReal(value))

    def _resetSerieScale(self):
        self.scaleSlider.setValue(
            (self.scaleSlider.minimum() + self.scaleSlider.maximum())/2)

    def _mapSliderScaleToReal(self, sliderValue):
        midSliderScale = (self.scaleSlider.minimum() + self.scaleSlider.maximum())/2
        return round(numpy.interp(sliderValue, [self.scaleSlider.minimum(), midSliderScale, self.scaleSlider.maximum()], [self._scaleMin, 1, self._scaleMax]), 2)
