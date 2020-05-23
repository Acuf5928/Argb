import _thread
import json
import os
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from code_helper import MySerial


class AppContext(ApplicationContext):
    def __init__(self):
        super().__init__()
        self.serialOBJ = None
        self.port = None

        self.readKey()
        self.serial()

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

    def readKey(self):
        try:
            with open(self.keyPath() + "/settings.json", "r") as read_file:
                data = json.load(read_file)
                self.port = data["port"]

        except Exception:
            self.port = ""

    def saveKey(self):
        data = {"port": self.port}
        self.checkfolder(self.keyPath())

        with open(self.keyPath() + "/settings.json", "w") as write_file:
            json.dump(data, write_file, indent=4)

    def checkfolder(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
