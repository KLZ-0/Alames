from Alames.importer import *

from Alames.config.keymaps import chartviewkeymap

from Alames import scope

class View(QChartView):
    """
    Purpose: displaying and interacting with the rendered QChart
    Creates a widget inside MainWindow which is shared for max 3 widgets
    An object from this class is created in Chart
    """

    # Store the settings internally  for faster access speed
    _valueTextItemScale = getattr(scope.settings, "TooltipTextScale", 1.5)
    _valueTextItemMargin = getattr(scope.settings, "TooltipTextMargin", 10)
    _valueTextItemOptimalPos = getattr(scope.settings, "TooltipOptimalPosition", True)

    _shortcuts = []

    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.setMouseTracking(True)
        self.setInteractive(True)
        self.setRubberBand(self.HorizontalRubberBand)
        self._setupShortcuts()

######## Shortcut binding

    def _setupShortcuts(self):
        for key, method in chartviewkeymap.keydict.items():
            self._shortcuts.append(QShortcut(QtGui.QKeySequence(key), self, getattr(chartviewkeymap, method, scope.shortcutBindError)))

######## overrides

    def setChart(self, chart):
        super(View, self).setChart(chart)
        self._createTrackingTools()

######## Init - tracking tools setup

    def _createTrackingTools(self):
        self.focusLine = QGraphicsLineItem(0, 0, 0, 10, self.chart())
        focusPen = QtGui.QPen()
        focusPen.setWidthF(1)
        focusPen.setStyle(QtCore.Qt.DashLine)
        focusPen.setColor(QtGui.QColor("#999999"))
        self.focusLine.setPen(focusPen)
        self.focusLine.setZValue(1500)

        self.focusValueTextItem = QGraphicsTextItem(self.chart())
        self.focusValueTextItem.setScale(self._valueTextItemScale)
        self.focusValueTextItem.setZValue(100)
        self.focusValueTextItem.setDefaultTextColor(QtGui.QColor("#333333"))

######## Actions

    def saveToFile(self):
        pixmap = self.grab()
        filename = scope.window.getSaveFile("Images (*.png *.jpg)")
        if filename == None:
            return

        result = pixmap.save(filename)
        if result:
            scope.log("Render saved successfully to " + filename)
        else:
            scope.log("Render save failec to " + filename)


    def renderToFile(self, filename):
        pixmap = self.grab()
        return pixmap.save(filename)

    def toggleVisible(self):
        self.setVisible(not self.isVisible())

######## Event handlers

    def mouseMoveEvent(self, event):
        super(View, self).mouseMoveEvent(event)
        if not self.focusLine.isVisible(): self.focusLine.show()
        if not self.focusValueTextItem.isVisible(): self.focusValueTextItem.show()

        xVal = self.chart().mapToValue(QtCore.QPointF(event.x(), 0), self.chart().getDummyQSerie()).x()
        if xVal < 0 or xVal >= self.chart().getEnd():
            # When the end of the chart is reached
            self.focusValueTextItem.hide()
            self.focusLine.hide()
            return

        html = str(self.chart().getXData()[round(xVal)]) + "<br>"
        for serie in self.chart().series():
            if serie.isVisible():
                html += "<font color=\"" + serie.color().name() + "\">" + "{0:.3f}<br>".format(self.chart().getYData(serie.property("number"))[round(xVal)])
        self.focusValueTextItem.setHtml(html)

        if self._valueTextItemOptimalPos:
            self.focusValueTextItem.setPos(self._calculateOptimalTextPos(event.pos()))
        else:
            self.focusValueTextItem.setPos(event.pos())

        focusLineX = self.chart().mapToPosition(QtCore.QPointF(round(xVal), 0), self.chart().getDummyQSerie()).x()
        self.focusLine.setPos(focusLineX, 0)

    def _calculateOptimalTextPos(self, basepoint):
        margin = self._valueTextItemMargin
        textRect = self.focusValueTextItem.boundingRect()
        xpos = basepoint.x()
        ypos = basepoint.y()

        if xpos+(textRect.width()*self._valueTextItemScale+margin) > self.contentsRect().width():
            xpos = self.contentsRect().width()-(textRect.width() *
                                                self._valueTextItemScale + margin)

        if ypos+(textRect.height()*self._valueTextItemScale+margin) > self.contentsRect().height():
            ypos = self.contentsRect().height()-(textRect.height() *
                                                self._valueTextItemScale + margin)
        
        return QtCore.QPointF(xpos, ypos)

    def leaveEvent(self, event):
        super(View, self).leaveEvent(event)
        if self.chart().series():
            self.focusLine.hide()
            self.focusValueTextItem.hide()

    def enterEvent(self, event):
        super(View, self).enterEvent(event)
        line = self.focusLine.line()
        line.setLength(self.height())
        self.focusLine.setLine(line)

    def keyPressEvent(self, event):
        super(View, self).keyPressEvent(event)
        key = event.text()
        if key in ["1","2","3","4","5","6","7","8","9"]:
            self.chart().toggleSerieVisiblity(key)

    def mousePressEvent(self, event):
        super(View, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.MiddleButton:
            self.chart().zoomReset()

    def mouseReleaseEvent(self, event):
        ######## set range values to left widget
        super(View, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton or event.button() == QtCore.Qt.RightButton:
            scope.leftDock.widget().updateValuesFromChart()

    def wheelEvent(self, event):
        super(View, self).wheelEvent(event)
        self.chart().scroll((event.angleDelta().y()/120)*self.chart().getScrollSpeed(), 0)
        scope.rightDock.widget().update()
