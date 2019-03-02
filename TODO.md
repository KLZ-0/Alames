Licensing: MIT should be OK.. https://riverbankcomputing.com/pipermail/pyqt/2016-September/038129.html

# NEW

**Settings**:
 - Fusion theme
 - OpenGL on by default
 - option to change default "open file" directory
 - Tooltip precision


**Finishing touch**:
 - add licensing header to every file
 - clean old files [partial]
 - write a documentation
 - unify comments in py files [partial]

**Finishing touch done**:
 - add installation guide
 - simplify imports
 - exceptions

**IDEAs**:
 - make the serial communication part in C/C++? > if not then add pyserial to requirements.txt > maybe I don't want to do it..
 - use virtualenv for linux installation? (maybe also windows)
 - pyserial? NO! [hard]
 - Do every possible binding with signals in window instead of scope (see example loaderWidget after RightWidget is loaded) to prevent early accesses
 - Window title and reading name from CSV [easy]
 - Add xz export [easiest]

**TODOs**:  `in importance order`
 - **Filters** - Add a widget for filters and make them customizable [medium]
   - NOTE: Introduce a modification log to chartmodifier

 - Transform chartmodifier into datamodifier [easy]

**TODOs done**:
 - Add scrollSpeed slider [easy]
 - Make a settings.py file [easy]
  - Add settings to scope - load at the start [easy]
 - Make the tooltip respect the chart dimensions and change its alignment accordingly [easy]
 - fix color change zoomReset [easy]
 - Tooltip line (focusLine) goes under chart when a new file is loaded [easy]
 - PositionLineItem and YAxis frags appear when no series are shown -> has to do something with the axis updating and dynamic y axis range [easy/medium]
 - Change scaling ratio to be more adaptive and make the ratio copyable, rewritable, maybe add +- buttons  [easy/medium] [partial]
 - Create F1 help [easy]
 - Add exporter for csv files also - make a smaller file with only the selected data [medium]
   - Option to save with or without the modifications - select which modifications [medium]
   - save the modified file
 - Add X axis toggle option [easy]

**BUGS**:
 - Loading takes a little bit more time than in the previous revision - find out why (maybe numpy.interp in RightWidgetSection? > try to do it manually) [medium]

**NOTES**:
 - workflow: open file > show data > **options to modify data** [properties] > update chart > render/export chart into image > export/save modified CSV
 - select measurement [keyboard shortcut] > {to be added} - **maybe**
 - two modes: -- current version
    - show current chart by default and update with changes + modify will be the properties tab -- it must load the series to be modified
    - modify and save the file
    - measure - **maybe**
