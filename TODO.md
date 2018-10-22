# OLD

**IDEAs**:
 - Add select time with rubberband and calcRms only from it
 - Add selecting more seconds + calcRms from them
 - Modify menubar to something like in Pymage

**TODOs**:
 - Add select timeRange from timeLineChart
 - Add sequential reading IDEA: Add live reading
 - Add settings reloading
 - update setings/repaint chart maybe
 - HW: Construct DIN voltage Transformer, calibrate    NOTE: Partially done
 - Add scaling of phasor arrows
 - Create scale and valueLabels in phasorWidget

# NEW

**Finishing touch**:
 - add installation guide
 - add requirements.txt

**IDEAs**:
  - customise input byte order/setting when measuring - make compatible with some commercial analysers

**TODOs**:
 - Cleanup the mess I made a year ago ;)
 - Resolution change **not supported!** >> *the widgets only get resized at creation*
 - Re-add functionality
 - Place the charting subsystem in its **own widget** for versatility
 - Add left widget for maybe filters?

**BUGS**:
 - "Empty filename passed to function" - happena when clicking on an item in openFileDialog {effect of an update on my system, may or may not work on other systems - also I had to install python-pyqtchart from the AUR}
 - smetimes this Qt error happens unpredictably, but it does not cause any disturbance and the user is not affected - "qt.qpa.xcb: QXcbConnection: XCB error: 3 (BadWindow), sequence: 1665, resource id: 37781937, major code: 40 (TranslateCoords), minor code: 0"
**NOTES**:
 - workflow: open file > show data > options to modify data [properties] > display graph/chart [keyboard shortcut] > render
 - select measurement [keyboard shortcut] > {to be added}
 - load the interface depending on user's choice
 - three modes:
    - show
    - modify/recalc
    - measure
 - two modes: -- current version
    - show current chart by default and update with changes + modify will be the properties tab -- it must load the series to be modified
    - measure

Basic modifications:
 - Trim series by x range
 - Translate series by function etc.
 - **save the modified file**

**Why don't modify the series on the go??? -- what if too large file?**
