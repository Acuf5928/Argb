import _thread
import json
import os
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from code_mySerial import MySerial

from code_readCpuInfo import cpuInfo


class AppContext(ApplicationContext):
    def __init__(self):
        super().__init__()
        self.serialOBJ = None
        self.port = None
        self.effect = None

        self.readKey()
        self.serial()
        _thread.start_new_thread(self.initLed, ())

    def initLed(self):
        time.sleep(3)
        if self.effect is not 12:
            self.serial().write(self.effect)
        else:
            _thread.start_new_thread(readCPUInfo, (self,))

    def run(self):
        return self.app.exec_()

    def appName(self):
        return "ARGB"

    def icon(self):
        return self.get_resource("images/led (1).png")

    def keyPath(self):
        return os.getenv('USERPROFILE') + "/." + self.appName()

    def serial(self):
        if self.serialOBJ is None:
            self.serialOBJ = MySerial(self)

        return self.serialOBJ

    def setPort(self, port):
        self.port = port
        self.serialOBJ = None
        self.serial()
        self.saveKey()

    def setEffect(self, effect):
        self.effect = effect
        self.saveKey()

    def readKey(self):
        try:
            with open(self.keyPath() + "/settings.json", "r") as read_file:
                data = json.load(read_file)
                self.port = data["port"]
                self.effect = data["effect"]

        except Exception:
            self.port = ""
            self.effect = ""

    def saveKey(self):
        data = {"port": self.port, "effect": self.effect}
        self.checkfolder(self.keyPath())

        with open(self.keyPath() + "/settings.json", "w") as write_file:
            json.dump(data, write_file, indent=4)

    def checkfolder(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)


def readCPUInfo(ctx):
    reader = cpuInfo(ctx.get_resource("dll\\OpenHardwareMonitorLib.dll"))
    while True:
        ctx.serial().write(int(reader.fetch_data()[0]["Reading"]) + 12000)
        time.sleep(2)
        if ctx.effect is not 12: break
