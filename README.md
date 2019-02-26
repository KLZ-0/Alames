# Alames - Digital signal analysing/logging software
Alames is an open-source signal analyser software intended for use with microcontroller driven analysers

It can also work with Power Quality Analysers from KMB with CSV files exported from Envis

# Repository info
*GitHub repository of my current SOČ/KOP 2019 project - lincensed under the MIT license*

This repository was established for tracking changes and managing my workflow

For the current development progress see the [devel branch](https://github.com/KLZ-0/Alames/tree/devel)

I merge to master only if the software is in stable (or partially stable) development state

# Installation
### Linux

Varies by distribution.. you should install the dependencies using your package manager or if you want you can use pip: `pip install -r ./requirements.txt` or `pip install --user -r ./requirements.txt`

### Windows
**Install dependencies:**

Run (double click on) `install-dependencies.bat`

If an editor would open instead of the app - set .pyw file type association for Pythonw manually or run as administrator `install-launcher.bat`

**Launch application:**

Run (double click on) `Alames.pyw`

# Requirements
 - **Linux or Windows**
 - **Python 3 and pip** installed and added to PATH

# Known bugs

 - "qt.qpa.xcb: QXcbConnection: XCB error: 3 (BadWindow), sequence: 1665, resource id: 37781937, major code: 40 (TranslateCoords), minor code: 0"
    - Sometimes this Qt error happens unpredictably, but it does not cause any disturbance and the user is not affected - this error happened to me when PyQt5 was installed using pacman, swithing to a pip install solves this problem
