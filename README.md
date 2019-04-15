# Alames - Slightly advanced CSV visualizer
Alames is an open-source CSV visualizer with the option to edit column names, colors, export rendered charts and extract data from big CSV files.

![Screenshot](/screenshots/sample.png?raw=true "Sample screenshot")

# Repository info
*GitHub repository of my current SOČ/KOP 2019 project - lincensed under the MIT license*

This project was originally developed as a signal analysing software intended for use with microcontroller driven analysers. It also supported CSV readings from KMB Power Quality Analysers exported from Envis.

The project later evolved into a CSV viewer with some editing features.

For the current development progress see the [devel branch](https://github.com/KLZ-0/Alames/tree/devel).

There is no ongoing development for now.

# Installation
### Linux

**Installation:**

Run `./install.sh` from the cloned directory

NOTE: The default installation is on per-user basis - it is not a system-wide install (The installer just copies the `.desktop` file to `~/.local/share/applications/` and updates the exec path)

**Manual installation:**

Run `pip install --user -r ./requirements.txt` to install the dependencies and launch `Alames.pyw` directly or click on `Alames.desktop` to launch the application

Optionally copy the `Alames.desktop` file to `~/.local/share/applications/` for per-user install or `/usr/share/applications/` for system-wide install and change the exec path in the file to point at a valid `Alames.pyw` file

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
