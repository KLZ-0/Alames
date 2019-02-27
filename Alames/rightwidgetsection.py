from Alames.importer import *

from Alames import scope

from Alames.generated.ui_rightwidgetsection import Ui_rightWidgetSection

class RightWidgetSection(QWidget, Ui_rightWidgetSection):

    updated = QtCore.pyqtSignal()

    _scaleMax = getattr(scope.settings, "ScalingRatio", 100)
    _scaleMin = 1/_scaleMax

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
        realVal = self._mapSliderScaleToReal(value)
        self.scaleValueButton.setText(str(realVal))
        self.serie.setLineScale(realVal)

    def _resetSerieScale(self):
        self.scaleSlider.setValue(
            (self.scaleSlider.minimum() + self.scaleSlider.maximum())/2)

    def _mapSliderScaleToReal(self, sliderValue):
        midSliderScale = (self.scaleSlider.minimum() + self.scaleSlider.maximum())/2

        if sliderValue == midSliderScale:
            return 1.00
        elif sliderValue < midSliderScale:
            return round(self._mapRange(sliderValue, self.scaleSlider.minimum(), midSliderScale, self._scaleMin, 1), 2)
        elif sliderValue > midSliderScale:
            return round(self._mapRange(sliderValue, midSliderScale, self.scaleSlider.maximum(), 1, self._scaleMax), 2)

    def _mapRange(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)
