# Alames - Digital signal analysing/logging software
Alames is an open-source digital signal analyser software intended for use with microcontroller driven analysers (wich could be built easily, even at home - the PCB gerbers will be available in the PCB subfolder)

It basically consists of two parts:
 - Measurement - logs the returned data from the Analyser and manages its settings
 - Data analysis - arranges and modifies the existing data in order to create charts, images or reports from it

# Repository info
*GitHub repository of my current SOČ/KOP 2019 project*

This repository was established for tracking changes and managing my workflow..

Lincensed under the MIT license.

# Installation
### Linux

Varies by distribution.. you should install the dependencies using your package manager or if you want you can use pip: `pip install -r ./requirements.txt` or `pip install --user -r ./requirements.txt`

### Windows
**Install dependencies:**

Run (double click on) `install-dependencies.bat`

Set .pyw file type association for Pythonw (needed for launcher):

Run as administrator (right click and select "run as administrator") `install-launcher.bat`

**Launch application:**

Run (double click on) `Alames.pyw`

# Requirements
 - **Linux or Windows**
 - **Python 3 and pip** installed and added to PATH
