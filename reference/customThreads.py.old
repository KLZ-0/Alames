import time, datetime
from PyQt5.QtCore import QThread

class rawReadSerial(QThread):
    def __init__(self, ser, save_file, duration, progressBar):
        super(rawReadSerial, self).__init__()
        self.ser = ser
        self.save_file = save_file
        self.duration = int(duration)
        self.progressBar = progressBar

    def __del__(self):
        self.wait()

    def run(self):
        self.duration *= 2850
        f = open(self.save_file, "w")
        f.write(datetime.datetime.today().strftime("%d-%m-%Y") + ",1,1,1\n")
        basetime = datetime.datetime.today().strftime("%H:%M:%S")
        micros = float(datetime.datetime.today().strftime(".%f"))
        i = 0
        self.ser.write(bytes([1]))
        while self.ser.is_open:
            try:
                data = self.ser.read(3)
            except:
                print("Connection interrupted..")
                f.close()
                self.exit(-310)
                break
            if datetime.datetime.today().strftime("%H:%M:%S") != basetime or micros > 1:
                basetime = datetime.datetime.today().strftime("%H:%M:%S")
                micros = float(datetime.datetime.today().strftime(".%f"))
            f.write(basetime + format(micros, '.6f').lstrip("0") + ",")
            f.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "\n")
            if i == self.duration:
                self.ser.write(bytes([0]))
                time.sleep(0.1)
                self.ser.close()
            self.progressBar.setValue(self.progressBar.value() + 1)
            i += 1
            micros += 0.000358
        f.close()

class rawReadContinuous(QThread):
    def __init__(self, ser, save_file, progressBar):
        super(rawReadContinuous, self).__init__()
        self.ser = ser
        self.save_file = save_file
        self.progressBar = progressBar

    def __del__(self):
        self.wait()

    def run(self):
        f = open(self.save_file, "w")
        f.write(datetime.datetime.today().strftime("%d-%m-%Y") + ",1,1,1\n")
        basetime = datetime.datetime.today().strftime("%H:%M:%S")
        micros = float(datetime.datetime.today().strftime(".%f"))
        self.ser.write(bytes([1]))
        while self.ser.is_open:
            try:
                data = self.ser.read(3)
            except:
                print("Connection interrupted..")
                f.close()
                self.exit(-310)
                break
            if datetime.datetime.today().strftime("%H:%M:%S") != basetime or micros > 1:
                basetime = datetime.datetime.today().strftime("%H:%M:%S")
                micros = float(datetime.datetime.today().strftime(".%f"))
            f.write(basetime + format(micros, '.6f').lstrip("0") + ",")
            f.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "\n")
            if self.progressBar.value() != 0:
                self.ser.write(bytes([0]))
                time.sleep(0.1)
                self.ser.close()
            micros += 0.000358
        f.close()

class rawReadCurrent(QThread):
    def __init__(self, ser, save_file, duration, progressBar):
        super(rawReadCurrent, self).__init__()
        self.ser = ser
        self.save_file = save_file
        self.duration = int(duration)
        self.progressBar = progressBar

    def __del__(self):
        self.wait()

    def run(self):
        self.duration *= 2850
        f = open(self.save_file, "w")
        f.write(datetime.datetime.today().strftime("%d-%m-%Y") + ',1,1\n')
        basetime = datetime.datetime.today().strftime("%H:%M:%S")
        micros = float(datetime.datetime.today().strftime(".%f"))
        i = 0
        self.ser.write(bytes([2]))
        while self.ser.is_open:
            try:
                data = self.ser.read(2)
            except:
                print("Connection interrupted..")
                f.close()
                self.exit(-310)
                break
            if datetime.datetime.today().strftime("%H:%M:%S") != basetime or micros > 1:
                basetime = datetime.datetime.today().strftime("%H:%M:%S")
                micros = float(datetime.datetime.today().strftime(".%f"))
            f.write(basetime + format(micros, '.6f').lstrip("0") + ',')
            f.write(str(data[0]) + "," + str(data[1]) + "\n")
            if i == self.duration:
                self.ser.write(bytes([0]))
                time.sleep(0.1)
                self.ser.close()
            self.progressBar.setValue(self.progressBar.value() + 1)
            i += 1
            micros += 0.000358
        f.close()
