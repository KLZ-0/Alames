@echo off

FOR /F "tokens=*" %%a in ('where pythonw') do SET pywpath=%%a
Assoc .pyw=pywfile
Ftype pywfile="%pywpath%" %1 && echo File association changed successfully

pause
