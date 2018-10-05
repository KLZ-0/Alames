import serial
import datetime as dt

# NOTE: Data consist of 3 Bytes >> first, second are data and the third is a status byte indicating whether some of the data bytes are negative
# BUG <important>: can reverse order of bytes >> fixed with adding an initial signal
# NOTE: Little differences between micros in seconds, but acceptable because arduino moves the the bytes to a buffer before sending

def readSerial(self, port, baudrate, save_file):
    f = open(save_file, "w") # add test "if exists"
    f.write(dt.datetime.today().strftime("%d-%m-%Y") + ',1,1,1\n') # as many 1 as fields
    ser = serial.Serial(port, baudrate) # e.g. "COM1" or "/dev/ttyUSB0", e.g. 115200
    basetime = dt.datetime.today().strftime("%H:%M:%S")
    micros = float(dt.datetime.today().strftime(".%f"))
    i = 0
    if ser.read(1)[0] != 36:
        ser.read(1)
    while ser.is_open:
        data = ser.read(3)
        if dt.datetime.today().strftime("%H:%M:%S") != basetime or micros > 1:
            basetime = dt.datetime.today().strftime("%H:%M:%S")
            micros = float(dt.datetime.today().strftime(".%f"))
        f.write(basetime + format(micros, '.6f').lstrip("0") + ',')
        f.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "\n")
        if i > 1150:
            ser.close()
        i += 1
        micros += 0.00085
    f.close()

def readCurrent(self, port, baudrate, save_file):
    f = open(save_file, "w") # add test "if exists"
    f.write(dt.datetime.today().strftime("%d-%m-%Y") + ',1,1\n') # as many 1 as fields
    ser = serial.Serial(port, baudrate) # e.g. "COM1" or "/dev/ttyUSB0", e.g. 115200
    basetime = dt.datetime.today().strftime("%H:%M:%S")
    micros = float(dt.datetime.today().strftime(".%f"))
    i = 0
    if ser.read(1)[0] != 36:
        ser.read(1)
    while ser.is_open:
        data = ser.read(3)
        if dt.datetime.today().strftime("%H:%M:%S") != basetime or micros > 1:
            basetime = dt.datetime.today().strftime("%H:%M:%S")
            micros = float(dt.datetime.today().strftime(".%f"))
        f.write(basetime + format(micros, '.6f').lstrip("0") + ',')
        f.write(str(data[1]) + "," + str(data[2]) + "\n")
        if i > 1150:
            ser.close()
        i += 1
        micros += 0.00085
    f.close()

readCurrent(None, "/dev/ttyUSB0", 115200, "current.ktemp")
