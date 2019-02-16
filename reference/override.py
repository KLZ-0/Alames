import time, datetime, serial, json
from PyQt5 import QtCore, QtGui
from PyQt5.QtChart import QChartView
from PyQt5.QtWidgets import *

import actions
import customThreads

class view(QChartView):
    def __init__(self, chart, parent, ex, app):
        super(view, self).__init__(chart, parent)
        self.app = app
        self.ex = ex
        self.setMouseTracking(True)
        self.setInteractive(True)
        self.setRubberBand(self.HorizontalRubberBand)
    def mouseMoveEvent(self, event):
        super(view, self).mouseMoveEvent(event)
        if self.chart().series():
            actions.tooltip(self.ex, event)
    def leaveEvent(self, event):
        self.app.changeOverrideCursor(QtCore.Qt.ArrowCursor)
        # self.app.restoreOverrideCursor()
        actions.ChartViewLeave(self.ex)

    def enterEvent(self, event):
        self.app.setOverrideCursor(QtCore.Qt.CrossCursor)

class recordWindow(QWidget):
    def __init__(self, parent):
        super(recordWindow, self).__init__()
        self.parent = parent
        self.setWindowTitle("Record")
        self.setWindowIcon(QtGui.QIcon("./src/record.png"))
        self.setGeometry(0, 0, self.parent.width()*0.3, self.parent.height()*0.6)
        self.saveFile = False

        self.mainLabel = QLabel("Welcome in the recording dialog", self)
        self.mainLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.selectMethod = QGroupBox("Select recording mode", self)
        self.select = [QRadioButton("Raw", self.selectMethod), QRadioButton("Only current", self.selectMethod), QRadioButton("Continuous", self.selectMethod)]
        for i in range(len(self.select)):
            self.select[i].clicked.connect(lambda: actions.radioChanged(self))
            self.select[i].setObjectName(self.select[i].text())

        self.baudrateLabel = QLabel("Baudrate:", self)
        self.baudrateEdit = QTextEdit("115200", self)
        self.portLabel = QLabel("Serial port:", self)
        self.portEdit = QTextEdit("/dev/ttyUSB0", self)

        self.durationSelect = QSpinBox(self)
        self.durationSelect.setMinimum(1)
        self.durationSelect.setMaximum(60)
        self.durationSelect.hide()
        self.durationSelectLabel = QLabel("Select duration:", self)
        self.durationSelectLabel.hide()

        self.saveFileButton = QPushButton("Choose file", self)
        self.saveFileButton.released.connect(self.requestSaveFile)
        self.stopButton = QPushButton("Stop recording", self)
        self.stopButton.released.connect(self.stopRecording)
        self.stopButton.hide()

        self.progressBar = QProgressBar(self)

        self.submitButton = QPushButton("Submit", self)
        self.submitButton.released.connect(self.formSubmit)
        self.translate()

    def stopRecording(self):
        self.progressBar.setValue(self.progressBar.maximum())

    def requestSaveFile(self):
        self.saveFile = QFileDialog.getSaveFileName(self, 'Save image As..', '/home', "KLZ archives (*.klz)")[0]
        if self.saveFile:
            if ".klz" not in self.saveFile:
                self.saveFile += ".klz"
        else:
            self.saveFile = False

    def formSubmit(self):
        if self.saveFile:
            try:
                ser = serial.Serial(self.portEdit.toPlainText(), int(self.baudrateEdit.toPlainText()))
                if self.select[0].isChecked():
                    self.submitButton.setDisabled(True)
                    self.progressBar.setMaximum(self.durationSelect.value() * 2850)
                    self.progressBar.setValue(0)
                    process = customThreads.rawReadSerial(ser, self.saveFile, self.durationSelect.value(), self.progressBar)
                    process.finished.connect(lambda: self.threadFinished(process))
                    process.start()
                elif self.select[1].isChecked():
                    self.submitButton.setDisabled(True)
                    self.progressBar.setMaximum(self.durationSelect.value() * 2850)
                    self.progressBar.setValue(0)
                    process = customThreads.rawReadCurrent(ser, self.saveFile, self.durationSelect.value(), self.progressBar)
                    process.finished.connect(lambda: self.threadFinished(process))
                    process.start()
                elif self.select[2].isChecked():
                    self.submitButton.setDisabled(True)
                    self.progressBar.setMaximum(self.durationSelect.value() * 2850)
                    self.progressBar.setValue(0)
                    self.stopButton.show()
                    process = customThreads.rawReadContinuous(ser, self.saveFile, self.progressBar)
                    process.finished.connect(lambda: self.threadFinished(process))
                    process.start()
            except serial.serialutil.SerialException as e:
                print(str(e))
                QErrorMessage(self).showMessage(str(e))
    def threadFinished(self, process):
        self.stopButton.hide()
        self.submitButton.setDisabled(False)
        if process.exec_() == -310:
            self.progressBar.setValue(0)
            QErrorMessage(self).showMessage("Connection interrupted, check USB connection..")
        else:
            self.progressBar.setValue(self.progressBar.maximum())

    def translate(self):
        if self.parent.settings["language"] == "Slovak":
            self.setWindowTitle("Meranie")
            self.mainLabel.setText("Nové meranie")
            self.selectMethod.setTitle("Výber metódy merania")
            self.select[0].setText("Nespracované meranie")
            self.select[1].setText("Nespracované meranie - len prúd")
            self.select[2].setText("Meranie bez časového limitu")

            self.durationSelectLabel.setText("Dĺžka merania")
            self.saveFileButton.setText("Uložiť ako..")
            self.stopButton.setText("Zastaviť meranie")
            self.submitButton.setText("Merať")

    def resizeEvent(self, event):
        self.mainLabel.setGeometry(0, 0, self.width(), self.mainLabel.height())
        self.selectMethod.setGeometry(0, self.mainLabel.height(), self.width(), self.select[0].height()*(1+len(self.select)*0.6))
        for i in range(len(self.select)):
            self.select[i].setGeometry(10, self.select[i].height()*0.6*(i+1), self.width(), self.select[i].height())
        self.baudrateLabel.setGeometry(0, self.selectMethod.frameGeometry().y() + self.selectMethod.frameGeometry().height() + 10, self.width()/3, self.baudrateEdit.fontWeight()/2)
        self.baudrateEdit.setGeometry(self.width()/3, self.selectMethod.frameGeometry().y() + self.selectMethod.frameGeometry().height() + 10, self.width()/3*2, self.baudrateEdit.fontWeight()/2)
        self.portLabel.setGeometry(0, self.baudrateEdit.frameGeometry().y() + self.baudrateEdit.frameGeometry().height() + 10, self.width()/3, self.portEdit.fontWeight()/2)
        self.portEdit.setGeometry(self.width()/3, self.baudrateEdit.frameGeometry().y() + self.baudrateEdit.frameGeometry().height() + 10, self.width()/3*2, self.portEdit.fontWeight()/2)
        self.durationSelect.setGeometry(self.width()/3, self.portEdit.frameGeometry().y() + self.portEdit.frameGeometry().height() + 10, self.durationSelect.width(), self.durationSelect.height())
        self.durationSelectLabel.setGeometry(0,  self.portEdit.frameGeometry().y() + self.portEdit.frameGeometry().height() + 10, self.durationSelect.width(), self.durationSelect.height())
        actions.resizeSaveButton(self)
        self.stopButton.setGeometry(0, self.height() - self.submitButton.height() - self.progressBar.height() - self.progressBar.height() - 30, self.width(), self.progressBar.height())
        self.progressBar.setGeometry(0, self.height() - self.submitButton.height() - self.progressBar.height() - 20, self.width(), self.progressBar.height())
        self.submitButton.setGeometry(self.geometry().center().x()-50, self.height() - self.submitButton.height() - 10, self.submitButton.width(), self.submitButton.height())

class settingsWindow(QWidget):
    def __init__(self, parent):
        super(settingsWindow, self).__init__()
        self.parent = parent
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("./src/settings.png"))
        self.setGeometry(0, 0, self.parent.width()*0.3, self.parent.height()*0.6)

        self.mainLabel = QLabel("Welcome in the settings dialog", self)
        self.mainLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.selectLang = QGroupBox("Language", self)
        self.select = [QRadioButton("English", self.selectLang), QRadioButton("Slovak", self.selectLang)]
        if self.parent.settings["language"] == "English":
            self.select[0].setChecked(True)
        elif self.parent.settings["language"] == "Slovak":
            self.select[1].setChecked(True)
        else:
            QErrorMessage(self).showMessage("Corrupted settings file..invalid language specified")
            print("Corrupted settings file..invalid language specified")

        self.currentLabel = QLabel("Current curve color:", self)
        self.currentEdit = QTextEdit(self.parent.settings["color"]["current"], self)
        self.voltageLabel = QLabel("Volage curve color:", self)
        self.voltageEdit = QTextEdit(self.parent.settings["color"]["voltage"], self)

        self.curveGroupBox = QGroupBox("Chart settings", self)
        self.curveCheckBoxes = [QCheckBox("Dynamically scale Axes", self.curveGroupBox), QCheckBox("Show current circle (in Phasor Diagram)", self.curveGroupBox)]
        self.curveCheckBoxes[0].setChecked(self.parent.settings["dynamic-axis-scaling"])
        self.curveCheckBoxes[1].setChecked(self.parent.settings["show-current-circle"])

        self.submitButton = QPushButton("Save", self)
        self.submitButton.released.connect(self.saveSettings)

        self.infoLabel = QLabel(self)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.translate()

    def translate(self):
        if self.parent.settings["language"] == "Slovak":
            self.setWindowTitle("Nastavenia")
            self.mainLabel.setText("Vitajte v nastaveniach")
            self.selectLang.setTitle("Jazyk")
            self.currentLabel.setText("Farba krivky prúdu")
            self.voltageLabel.setText("Farba krivky napätia")
            self.submitButton.setText("Uložiť")
            self.curveGroupBox.setTitle("Nastavenia grafu")
            self.curveCheckBoxes[0].setText("Dynamická mierka")
            self.curveCheckBoxes[1].setText("Zobraziť kružnicu pre prúd (vo fázorovom diagrame)")

    def saveSettings(self):
        try:
            config = {}
            config["color"] = {}
            if self.select[0].isChecked():
                config["language"] = "English"
                self.infoLabel.setText("Success!\nRestart application for the changes to take effect")
            elif self.select[1].isChecked():
                config["language"] = "Slovak"
                self.infoLabel.setText("Nastavenia sa uložili!\nReštartujte aplikáciu aby sa zmeny prejavili")
            config["color"]["voltage"] = self.voltageEdit.toPlainText()
            config["color"]["current"] = self.currentEdit.toPlainText()
            config["dynamic-axis-scaling"] = self.curveCheckBoxes[0].isChecked()
            config["show-current-circle"] = self.curveCheckBoxes[1].isChecked()
            config["calibration"] = self.parent.settings["calibration"]
            json.dump(config, open("config.json", "w"), sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            self.infoLabel.setText(str(e))

    def resizeEvent(self, event):
        self.mainLabel.setGeometry(0, 0, self.width(), self.mainLabel.height())
        self.selectLang.setGeometry(0, self.mainLabel.height(), self.width(), self.select[0].height()*(1+len(self.select)*0.6))
        for i in range(len(self.select)):
            self.select[i].setGeometry(10, self.select[i].height()*0.6*(i+1), self.width(), self.select[i].height())
        self.currentLabel.setGeometry(0, self.selectLang.frameGeometry().y() + self.selectLang.frameGeometry().height() + 10, self.width()/3, self.currentEdit.fontWeight()/2)
        self.currentEdit.setGeometry(self.width()/3, self.selectLang.frameGeometry().y() + self.selectLang.frameGeometry().height() + 10, self.width()/3*2, self.currentEdit.fontWeight()/2)
        self.voltageLabel.setGeometry(0, self.currentEdit.frameGeometry().y() + self.currentEdit.frameGeometry().height() + 10, self.width()/3, self.voltageEdit.fontWeight()/2)
        self.voltageEdit.setGeometry(self.width()/3, self.currentEdit.frameGeometry().y() + self.currentEdit.frameGeometry().height() + 10, self.width()/3*2, self.voltageEdit.fontWeight()/2)
        self.curveGroupBox.setGeometry(0, self.voltageEdit.frameGeometry().y() + self.voltageEdit.frameGeometry().height() + 10, self.width(), self.curveCheckBoxes[0].height()*(1+len(self.curveCheckBoxes)*0.6))
        for i in range(len(self.curveCheckBoxes)):
            self.curveCheckBoxes[i].setGeometry(10, self.curveCheckBoxes[i].height()*0.6*(i+1), self.width(), self.curveCheckBoxes[i].height())
        self.submitButton.setGeometry(self.geometry().center().x()-50, self.height() - self.submitButton.height() - 10, self.submitButton.width(), self.submitButton.height())
        self.infoLabel.setGeometry(0,  self.submitButton.y() - 60, self.width(), 50)

class calibrationWindow(QWidget):
    def __init__(self, parent):
        super(calibrationWindow, self).__init__()
        self.parent = parent
        self.setWindowTitle("Calibration")
        self.setWindowIcon(QtGui.QIcon("./src/calibrate.png"))
        self.setGeometry(0, 0, self.parent.width()*0.3, self.parent.height()*0.2)

        self.mainLabel = QLabel("Adjust calibration..\n\nFor permanent save, press the submit button in settings dialog", self)
        self.mainLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.calibrationSelect = QDoubleSpinBox(self)
        self.calibrationSelect.setSingleStep(0.01)
        self.calibrationSelect.setValue(self.parent.settings["calibration"])
        self.calibrationSelect.setMinimum(0.01)
        self.calibrationSelect.setMaximum(60)
        self.calibrationSelect.valueChanged.connect(self.spinBoxChange)
        self.calibrationSelectLabel = QLabel("Set difference constant:", self)

        self.currentValueLabel = QLabel(self)
        self.currentValueLabel.setText("Current RMS value: ")

        self.translate()

    def spinBoxChange(self, val):
        self.parent.settings["calibration"] = val
        text = "Current RMS value: "
        if self.parent.settings["language"] == "Slovak": text = "Aktuálna efektívna hodnota: "
        try:
            text += str((sum(self.parent.rmsValues[1])/float(len(self.parent.rmsValues[1])))/self.parent.previousCalibration * val)
        except Exception as e:
            print(e)
        finally:
            self.currentValueLabel.setText(text)
    def translate(self):
        if self.parent.settings["language"] == "Slovak":
            self.setWindowTitle("Kalibrácia napätia")
            self.mainLabel.setText("Nastavenie kalibrácie napätia..\n\nPre permanentnú zmenu uložte nastavenia")
            self.calibrationSelectLabel.setText("Nastavte konštantu kalibrácie:")
            self.currentValueLabel.setText("Aktuálna efektívna hodnota: ")

    def resizeEvent(self, event):
        self.mainLabel.setGeometry(0, 10, self.width(), self.mainLabel.font().weight())
        self.calibrationSelect.setGeometry(self.width()/1.5, self.mainLabel.frameGeometry().y() + self.mainLabel.frameGeometry().height() + 10, self.width()/3, self.calibrationSelect.height())
        self.calibrationSelectLabel.setGeometry(0,  self.mainLabel.frameGeometry().y() + self.mainLabel.frameGeometry().height() + 10, self.width()/1.5, self.calibrationSelect.height())
        self.currentValueLabel.setGeometry(0, self.calibrationSelectLabel.frameGeometry().y() + self.calibrationSelectLabel.frameGeometry().height() + 10, self.width()/1.5, self.calibrationSelectLabel.height())

class curveGroupBox(QGroupBox):
    def __init__(self, title, parent):
        super(curveGroupBox, self).__init__(title, parent)
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.parent = parent

    def paintEvent(self, event):
        super(curveGroupBox, self).paintEvent(event)
        qp = QtGui.QPainter(self)
        self.drawLine(qp)

    def drawLine(self, qp):
        pen = qp.pen()
        pen.setCapStyle(QtCore.Qt.FlatCap)
        pen.setWidth(3)

        for option in self.parent.selectCurvesOptions:
            pen.setColor(QtGui.QColor(self.parent.colors[self.parent.synonyms[option.text().lower()]]))
            qp.setPen(pen)
            qp.drawLine(option.x() + option.width()/3, option.geometry().center().y(), option.x() + option.width()/1.5, option.geometry().center().y())
