Licensing: MIT should be OK.. https://riverbankcomputing.com/pipermail/pyqt/2016-September/038129.html

# NEW

**Settings**:
 - Fusion theme
 - OpenGL on by default
 - option to change default "open file" directory


**Finishing touch**:
 - add installation guide
 - add licensing header to every file
 - simplify imports
 - clean old files
 - exceptions
 - write a documentation
 - Do every possible binding with signals in window instead of scope (see example loaderWidget after RightWidget is loaded) to prevent early accesses
 - unify comments in py files

**IDEAs**:
  - make the serial communication part in C/C++? > if not then add pyserial to requirements.txt > maybe I don't want to do it..
  - use virtualenv for linux installation? (maybe also windows)

**TODOs**:  `in importance order`
 - **Make a settings.py file** [easy]
   - **Add settings to scope - load at the start** [easy]

 - fix color change zoomReset [easy]

 - Make the tooltip respect the chart dimensions and change its alignment accordingly [easy]

 - **Filters** - Add a widget for filters and make them customizable [medium]
 - **Add exporter for csv files also - make a smaller file with only the selected data** [medium]
   - Option to save with or without the modifications - select which modifications [medium]
   - **save the modified file**
   - NOTE: Introduce a modification log to chartmodifier
   

 - Change scaling ratio to be more adaptive and make the ratio copyable, rewritable, maybe +- buttons and more adaptive [easy/medium]

 - pyserial? [hard]

**TODOs done**:
 - Add scrollSpeed slider [easy]

**BUGS**:
 - PositionLineItem and YAxis frags appear when no series are shown -> has to do something with the axis updating and dynamic y axis range [easy/medium]
 - Loading takes a little bit more time than in the previous revision - find out why (maybe numpy.interp in RightWidgetSection? > try to do it manually) [medium]
 - Tooltip line (focusLine) goes under chart when a new file is loaded

**NOTES**:
 - workflow: open file > show data > **options to modify data** [properties] > update chart > render/export chart into image > export/save modified CSV
 - select measurement [keyboard shortcut] > {to be added} - **maybe**
 - two modes: -- current version
    - show current chart by default and update with changes + modify will be the properties tab -- it must load the series to be modified
    - modify and save the file
    - measure - **maybe**
