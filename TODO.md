Licensing: MIT should be OK.. https://riverbankcomputing.com/pipermail/pyqt/2016-September/038129.html

# OLD

**IDEAs**:
 - Modify menubar to something like in Pymage

**TODOs**:
 - Add sequential reading IDEA: Add live reading
 - Add settings reloading
 - update setings/repaint chart maybe
 - HW: Construct DIN voltage Transformer, calibrate    NOTE: Partially done
 - Add scaling of phasor arrows
 - Create scale and valueLabels in phasorWidget

# NEW

**Settings**:
 - Fusion theme
 - OpenGL on by default

**Finishing touch**:
 - add installation guide
 - add licensing header to every file
 - simplify imports

**IDEAs**:
  - **When large numbers of points are concentrated on a small area, they should be merged to represent RMS values**
  - customise input byte order/setting when measuring - make compatible with some commercial analysers
  - make the serial communication part in C/C++? > if not then add pyserial to requirements.txt
  - use virtualenv for linux installation? (maybe also windows)
  - versioning
  - option to change default "open file" directory

**TODOs**:
 - Re-add functionality from reference/
 - Add left widget for maybe filters?
 - add exporter
 - scroll - https://www.advsofteng.com/doc/cdcppdoc/realtimezoomscrollqt.htm
 - implement RMS calculation
 - add scrollSpeed slider
 - Save modified ranges in dataholder instead of lineseries [solved]
    - make a second dataholder, the first is for overall values and the second for selected range values see todo below
 - after zooming the chart (connect some event) also modify the selection dataholder (get start and end of the chart and calculate) - the qlineseries does not need to be altered (maybe) **!!!plan it!!!**
 - there is also another kind of change to data, filters -> the overall dataholders data will change and also the selection dataholders, retaining its currently selected range (or just zoom out.. idk)

**BUGS**:
 - sometimes this Qt error happens unpredictably, but it does not cause any disturbance and the user is not affected - "qt.qpa.xcb: QXcbConnection: XCB error: 3 (BadWindow), sequence: 1665, resource id: 37781937, major code: 40 (TranslateCoords), minor code: 0" [solved]
    - This error happened when PyQt5 was installed using pacman, swithing to a pip install solves this problem
 - update left dock after multiply filter applied does not update

**NOTES**:
 - workflow: open file > show data > options to modify data [properties] > display graph/chart [keyboard shortcut] > render
 - select measurement [keyboard shortcut] > {to be added}
 - load the interface depending on user's choice
 - two modes: -- current version
    - show current chart by default and update with changes + modify will be the properties tab -- it must load the series to be modified
    - modify and save the file
    - measure

Basic modifications:
 - Translate series by function etc.
 - **save the modified file**
