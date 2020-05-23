import _thread
import json
import os
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from code_helper import MySerial


class AppContext(ApplicationContext):
    def __init__(self):
        super().__init__()
        self.status = None
        self.serialOBJ = None
        self.port = None
        self.statusLed = None
        self.autoLed = None

        self.readKey()
        self.serial()
        self.checkStatusBackground()

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
            time.sleep(2)

            if self.autoLed:
                self.serialOBJ.write(2)
            elif self.statusLed:
                self.serialOBJ.write(1)
            elif not self.statusLed:
                self.serialOBJ.write(0)

        return self.serialOBJ

    def checkStatusBackground(self):
        _thread.start_new_thread(self.checkStatusContinue, ())

    def checkStatusContinue(self):
        while True:
            try:
                self.checkStatus()
            except Exception:
                pass

    def checkStatus(self):
        status = self.serial().read()

        if status is "":
            self.status = None
            return

        self.status = json.loads(status)

    def setPort(self, port):
        self.port = port
        self.serialOBJ = None
        self.serial()
        self.saveKey()

    def setEnable(self, status):
        self.statusLed = status
        self.saveKey()

    def setAuto(self, status):
        self.autoLed = status
        self.saveKey()

    def readKey(self):
        try:
            with open(self.keyPath() + "/settings.json", "r") as read_file:
                data = json.load(read_file)
                self.port = data["port"]
                self.statusLed = bool(data["statusLed"])
                self.autoLed = bool(data["autoLed"])

        except Exception:
            self.port = ""
            self.statusLed = False
            self.autoLed = True

    def saveKey(self):
        data = {"statusLed": self.statusLed, "autoLed": self.autoLed, "port": self.port}
        self.checkfolder(self.keyPath())

        with open(self.keyPath() + "/settings.json", "w") as write_file:
            json.dump(data, write_file, indent=4)

    def checkfolder(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
