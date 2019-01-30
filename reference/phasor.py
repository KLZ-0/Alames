import math
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class Diagram(QWidget):
    def __init__(self, parent):
        super(Diagram, self).__init__(parent)
        self.parent = parent
        self.currentLabel = QLabel(self)
        self.voltageLabel = QLabel(self)
        self.labels = [self.currentLabel, self.voltageLabel]
        for label in self.labels:
            label.hide()
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("background-color: #eeeeee")

    def hideEvent(self, event):
        for label in self.labels:
            label.setText("")
            label.hide()

    def paintEvent(self, event):
        super(Diagram, self).paintEvent(event)
        if self.parent.voltages:
            qp = QtGui.QPainter(self)
            qp.setRenderHint(QtGui.QPainter.Antialiasing)
            pen = qp.pen()
            pen.setCapStyle(QtCore.Qt.RoundCap)
            pen.setWidth(2)
            pen.setColor(QtGui.QColor("#333333"))
            qp.setPen(pen)
            mainCircleOffset = 15 # offset from edges of widget
            self.tipPoints = []

            if self.parent.actualValues:
                self.drawCircle(qp, pen, mainCircleOffset)
                self.drawDashedCircles(qp, mainCircleOffset)
                self.drawArrows(qp, pen)
                self.updateValueLabels(qp)

    def drawCircle(self, qp, pen, offset):
        pen.setWidth(1)
        qp.setPen(pen)
        qp.drawEllipse(offset, offset, self.width()-2*offset-1, self.height()-2*offset-1)
        qp.drawLine(0, self.height()/2, self.width(), self.height()/2)
        qp.drawLine(self.width()/2, 0, self.width()/2, self.height())

    def drawDashedCircles(self, qp, offset):
        pen = qp.pen()
        pen.setStyle(QtCore.Qt.DashLine)
        pen.setColor(QtGui.QColor("#999999"))
        qp.setPen(pen)
        nOfCircles = 5
        radius = (self.width()-2*offset)/2

        for i in range(nOfCircles):
            offset += radius/nOfCircles
            qp.drawEllipse(offset, offset, self.width()-2*offset-1, self.height()-2*offset-1)

    def drawArrows(self, qp, pen):
        center = self.contentsRect().center()
        actualVal = self.parent.actualValues
        dataSet = self.parent.powerDataSet
        pen.setWidth(2)

        maxCurrentTreshold = 50
        scales = range(0, maxCurrentTreshold + 5, 5)
        scale = 0
        for i in scales:
            if self.parent.actualValues[0] > i:
                scale = i
            else:
                scale = i # this is what we are searching for
                break

        lines = []
        for i in range(2):
            lines.append(QtCore.QLineF(center, QtCore.QPoint(self.width(), center.y())))

        lines[0].setLength((self.width()/2)*self.parent.actualValues[0]/scale)
        if self.parent.settings["show-current-circle"]:
            self.drawCurrentCircle(qp, lines[0])
        lines[1].setAngle(self.parent.fi)

        if lines[0].p2().y() == lines[1].p2().y():
            points = [lines[0].p1(), lines[0].p2()]
            for point in points:
                point.setY(point.y()+1)
            lines[0].setPoints(points[0], points[1])

            points = [lines[1].p1(), lines[1].p2()]
            for point in points:
                point.setY(point.y()-1)
            lines[1].setPoints(points[0], points[1])

        for i in reversed(range(len(lines))):
            pen.setColor(QtGui.QColor(self.parent.colors[self.parent.translateIndex[i]]))
            qp.setPen(pen)
            brush = qp.brush()
            brush.setColor(QtGui.QColor(self.parent.colors[self.parent.translateIndex[i]]))
            brush.setStyle(QtCore.Qt.SolidPattern)
            qp.setBrush(brush)
            qp.drawLine(lines[i])
            self.tipPoints = [lines[i].p2()] + self.tipPoints # appending in reversed list
            self.drawArrowHead(qp, lines[i].p2(), lines[i])

    def drawArrowHead(self, qp, tipPoint, line):
        arrowLen = 16
        arrowHeight = 4
        line.setLength(line.length()-arrowLen)
        centerP = line.p2()
        rightLine = QtCore.QLineF(centerP, tipPoint)
        rightLine.setAngle(line.angle() + 90)
        rightLine.setLength(arrowHeight)
        leftLine = QtCore.QLineF(centerP, tipPoint)
        leftLine.setAngle(line.angle() - 90)
        leftLine.setLength(arrowHeight)

        pointsPolygon = QtGui.QPolygonF([tipPoint, rightLine.p2(), leftLine.p2()])
        qp.drawPolygon(pointsPolygon, QtCore.Qt.WindingFill)

    def drawCurrentCircle(self, qp, currentLine):
        pen = qp.pen()
        pen.setColor(QtGui.QColor(self.parent.colors[self.parent.translateIndex[0]]))
        pen.setStyle(QtCore.Qt.DashLine)
        pen.setWidthF(1.5)
        qp.setPen(pen)
        qp.drawEllipse(currentLine.p1().x()-currentLine.length(), currentLine.p1().y()-currentLine.length(), currentLine.length()*2+1, currentLine.length()*2+1)

    def updateValueLabels(self, qp):
        qp.setBrush(QtGui.QBrush())
        qp.setPen(QtGui.QColor("#999999"))
        labelWidth = self.width()/6
        labelHeight = self.height()/20
        for i in range(len(self.labels)):
            if self.labels[i].isVisible() == False:
                self.labels[i].show()
            font = self.labels[i].font()
            font.setPixelSize(labelHeight*0.9)
            self.labels[i].setFont(font)

            self.labels[i].setText("<font color=\"" + self.parent.colors[self.parent.translateIndex[i]] + "\">" + str(self.parent.actualValues[i]) + "</font><br>")
            x = self.tipPoints[i].x() - labelWidth - 1
            y = self.tipPoints[i].y() - labelHeight*1.5
            labelRect = QtCore.QRect(x, y, labelWidth, labelHeight)
            qp.drawRect(labelRect)
            self.labels[i].setGeometry(labelRect)
