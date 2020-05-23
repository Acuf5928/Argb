import serial
import serial.tools.list_ports


class MySerial:
    def __init__(self, ctx):
        self.ctx = ctx
        self.s = None
        self.checkSerial()

    def write(self, message):
        try:
            self.checkSerial()
            self.s.write(reformatString(message))
        except Exception:
            pass

    def checkSerial(self):
        if self.s is None:
            try:
                self.s = serial.Serial(port=self.ctx.port, baudrate=115200, timeout=.1)
            except Exception:
                self.s = None

    def listDevice(self):
        list = []
        for port in serial.tools.list_ports.comports(include_links=False):
            list.append(port[0])
        list.sort()
        return list


def reformatString(message):
    strMessage = str(message)
    if strMessage[-1] != "\n":
        return (strMessage + "\n").encode("utf8")
    else:
        return strMessage.encode("utf8")
