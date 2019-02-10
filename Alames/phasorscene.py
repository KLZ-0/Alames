import math
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from Alames.dataholder import DataHolder


class PhasorScene(QGraphicsScene):
    """Phasor diagram Scene"""

    dataholder = DataHolder()
    settings = {"show-current-circle": False,
                "current-color": "#ff0000", "voltage-color": "#0000ff"}
    _width = _height = 300
    _radius = _width/2
    _center = QtCore.QPointF(_radius, _radius)
    _arrowLenMax = _radius
    _arrowAngle = 15
    _arrowHeadLen = 15

    _arrowLineThickness = 2
    _helperLineThickness = 1

    _nOfCircles = 4
    _circleOffset = _width/_nOfCircles+1  # Offset between circles

    def __init__(self):
        super(PhasorScene, self).__init__()
        self.currentLabel = QGraphicsTextItem()
        self.voltageLabel = QGraphicsTextItem()
        self.currentLabel.setDefaultTextColor(QtGui.QColor(self.settings["current-color"]))
        self.voltageLabel.setDefaultTextColor(QtGui.QColor(self.settings["voltage-color"]))
        self.labels = [self.currentLabel, self.voltageLabel]
        for label in self.labels:
            self.addItem(label)
            label.hide()

######## Update methods

    def setData(self, dataholder, settings):
        self.dataholder = dataholder
        self.settings = settings
        self.reDraw()

    def setDataHolder(self, dataholder):
        self.dataholder = dataholder
        self.reDraw()

    def setSettings(self, settings):
        self.settings = settings
        self.reDraw()

    def hideEvent(self, event):
        super(PhasorScene, self).hideEvent(event)
        for label in self.labels:
            label.setPlainText("")
            label.hide()

    def reDraw(self):
        """Redraw (or update) the Diagram"""

        if self.dataholder.isLoaded():
            self.tipPoints = []

            if self.dataholder.RMSValues():
                self._drawDiagramBase()
                self._drawHelperCircles()
                self._drawPowerArrows()
                # self.updateValueLabels(qp)        

######## Drawing methods - draw (display) the items on the scene (high level methods)

    def _drawDiagramBase(self):
        """Draw the main circle + x and y axes"""

        circleRect = QtCore.QRectF(0, 0, self._width, self._height)
        self.circle = QGraphicsEllipseItem()
        pen = self.circle.pen()
        pen.setWidthF(self._helperLineThickness)
        pen.setColor(self.palette().color(QtGui.QPalette.Dark))
        self.circle.setPen(pen)
        # self.circle.setBrush(QtGui.QBrush(
        #     self.palette().color(QtGui.QPalette.Mid)))
        self.circle.setRect(circleRect)
        self.addItem(self.circle)

        self.xLine = QGraphicsLineItem(
            pen.widthF(), self.height()/2-pen.widthF()/2, self.width()-2*pen.widthF(), self.height()/2-pen.widthF()/2)
        self.yLine = QGraphicsLineItem(
            self.width()/2-pen.widthF()/2, pen.widthF(), self.width()/2-pen.widthF()/2, self.height()-2*pen.widthF())
        self.addItem(self.xLine)
        self.addItem(self.yLine)
        self.xLine.setPen(pen)
        self.yLine.setPen(pen)
        self.xLine.show()
        self.yLine.show()

    def _drawHelperCircles(self):
        """Draw circles for axis numbering"""

        self.helperCircles = []
        halfset = self._circleOffset/2

        for i in range(1, self._nOfCircles):
            self.helperCircles.append(QGraphicsEllipseItem())
            pen = self.helperCircles[-1].pen()
            pen.setStyle(QtCore.Qt.DashLine)
            pen.setColor(self.palette().color(QtGui.QPalette.Light))
            pen.setWidthF(self._helperLineThickness)
            self.helperCircles[-1].setPen(pen)
            self.helperCircles[-1].setRect(0, 0, self._circleOffset*i, self._circleOffset*i)
            self.helperCircles[-1].setPos(self._radius-halfset*i, self._radius-halfset*i)
            self.addItem(self.helperCircles[-1])

            # TODO: Add axis numbering

    def _drawPowerArrows(self):
        """Create Power Phasor diagram"""

        # reducing reference access time
        dataSet = self.dataholder.powerDataSet()
        maxLineLen = self.width()/2
        lenMultiplier = maxLineLen/max(self.dataholder.powerDataSet())

        # TODO: Reimplement this part
        self.arrowLineItems = []
        self.arrowLineItems.append(self._createArrow(1))
        self.arrowLineItems.append(self._createArrow(1, 90, "#ffffff"))
        self.arrowLineItems.append(
            self._createPytagorasArrow(
                self.arrowLineItems[0], self.arrowLineItems[1], "#888888"))
        self._addDashedSupport(self.arrowLineItems[-1])

######## Constuction methods - construct new objects and return them

    def _createArrow(self, lenmultiplier, angle=0, color="#333333", additem=True):
        """Create and return an arrow LineItem with arrowhead"""

        pen = QtGui.QPen()
        pen.setWidthF(self._arrowLineThickness)
        pen.setColor(QtGui.QColor(color))
        line = QtCore.QLineF(self._center, QtCore.QPointF(
            self._radius + (self._arrowLenMax*lenmultiplier)-pen.widthF()/2, self._center.y()))
        line.setAngle(angle)

        item = QGraphicsLineItem(line)
        item.setPen(pen)

        self._addHeadToLineItem(item, -self._arrowAngle)
        self._addHeadToLineItem(item, self._arrowAngle)
        self._addLabelToLineItem(item)

        if additem: self.addItem(item)
        return item

    def _createPytagorasArrow(self, lineItem1, lineItem2, color="#333333", additem=True):
        """Create a line using the pythagoras theorem with dashed supports to make a triangle - example use: apparent power"""

        endpoint = QtCore.QPointF(
            lineItem1.line().p2().x(), lineItem2.line().p2().y())

        pen = QtGui.QPen()
        pen.setWidthF(self._arrowLineThickness)
        pen.setColor(QtGui.QColor(color))
        line = QtCore.QLineF(self._center, endpoint)

        item = QGraphicsLineItem(line)
        item.setPen(pen)

        self._addHeadToLineItem(item, -self._arrowAngle)
        self._addHeadToLineItem(item, self._arrowAngle)
        self._addLabelToLineItem(item)

        if additem:
            self.addItem(item)
        return item

######## Modifier methods - only modify items (add children to them)

    def _addHeadToLineItem(self, item, angle):
        """Add arrowhead to a QGraphicsLineItem's end"""

        parentline = item.line()
        rhead = QtCore.QLineF(parentline.p2(), parentline.p1())
        rhead.setAngle(rhead.angle() + angle)
        rhead.setLength(self._arrowHeadLen)
        QGraphicsLineItem(rhead, item).setPen(item.pen())

    def _addLabelToLineItem(self, lineItem):
        basepoint = lineItem.line().p2()

        lineItem.label = QGraphicsTextItem(lineItem)
        lineItem.label.setDefaultTextColor(lineItem.pen().color())
        lineItem.label.setPlainText("text")
        lineItem.label.setPos(basepoint.x()+10, basepoint.y())

    def _addDashedSupport(self, lineItem):
        """Add a dashed support to a line"""

        pen = lineItem.pen()
        pen.setStyle(QtCore.Qt.DashLine)
        pen.setWidthF(self._helperLineThickness)

        endpoint = lineItem.line().p2()
        xLine = QtCore.QLineF(QtCore.QPointF(
            self._radius, endpoint.y()), endpoint)
        yLine = QtCore.QLineF(QtCore.QPointF(
            endpoint.x(), self._radius), endpoint)

        QGraphicsLineItem(xLine, lineItem).setPen(pen)
        QGraphicsLineItem(yLine, lineItem).setPen(pen)
