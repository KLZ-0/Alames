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

**Finishing touch**:
 - add installation guide
 - add licensing header to every file
 - simplify imports

**IDEAs**:
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

**BUGS**:
 - sometimes this Qt error happens unpredictably, but it does not cause any disturbance and the user is not affected - "qt.qpa.xcb: QXcbConnection: XCB error: 3 (BadWindow), sequence: 1665, resource id: 37781937, major code: 40 (TranslateCoords), minor code: 0"

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
