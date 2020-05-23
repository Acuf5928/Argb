import _thread

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import sys

import gui_settings

from appContext import readCPUInfo


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, ctx):
        super(SystemTrayIcon, self).__init__()
        self.ctx = ctx
        self.menu = QtWidgets.QMenu()
        self.activated.connect(self.setMenu)
        self.setIcon(QtGui.QIcon(self.ctx.icon()))
        self.setMenu()

    # Init sysTray
    def setMenu(self):
        self.menu.clear()

        self.menu.addSeparator()

        self.stat1 = self.menu.addAction("Mono color")
        self.stat1.setEnabled(False)

        self.menu.addSeparator()

        self.red1 = self.menu.addAction("RED")
        self.red1.triggered.connect(self.setRED1)

        self.blue1 = self.menu.addAction("BLUE")
        self.blue1.triggered.connect(self.setBLUE1)

        self.green1 = self.menu.addAction("GREEN")
        self.green1.triggered.connect(self.setGREEN1)

        self.white1 = self.menu.addAction("WHITE")
        self.white1.triggered.connect(self.setWHITE1)

        self.menu.addSeparator()

        self.stat2 = self.menu.addAction("theaterChase")
        self.stat2.setEnabled(False)

        self.menu.addSeparator()

        self.red2 = self.menu.addAction("RED")
        self.red2.triggered.connect(self.setRED2)

        self.blue2 = self.menu.addAction("BLUE")
        self.blue2.triggered.connect(self.setBLUE2)

        self.green2 = self.menu.addAction("GREEN")
        self.green2.triggered.connect(self.setGREEN2)

        self.white2 = self.menu.addAction("WHITE")
        self.white2.triggered.connect(self.setWHITE2)

        self.menu.addSeparator()

        self.rainbow1 = self.menu.addAction("RAINBOW")
        self.rainbow1.triggered.connect(self.setRAINBOW)

        self.rainbow2 = self.menu.addAction("RAINBOW V2")
        self.rainbow2.triggered.connect(self.setRAINBOW2)

        self.theaterChaseRainbow = self.menu.addAction("THEATERCHASERAINBOW")
        self.theaterChaseRainbow.triggered.connect(self.setTHEATERCHASERAINBOW)

        self.menu.addSeparator()

        self.cpu = self.menu.addAction("Based on CPU Load")
        self.cpu.triggered.connect(self.setCPU)

        self.menu.addSeparator()

        self.off = self.menu.addAction("OFF")
        self.off.triggered.connect(self.setOFF)

        self.menu.addSeparator()

        self.windows = self.menu.addAction("Settings")
        self.windows.triggered.connect(self.openWindows)

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)

        self.setContextMenu(self.menu)

    # Set functions of all menu elements, from here:
    def setRED1(self):
        self.ctx.setEffect(1)
        self.ctx.serial().write(1)

    def setBLUE1(self):
        self.ctx.setEffect(3)
        self.ctx.serial().write(3)

    def setGREEN1(self):
        self.ctx.setEffect(2)
        self.ctx.serial().write(2)

    def setWHITE1(self):
        self.ctx.setEffect(5)
        self.ctx.serial().write(5)

    def setRED2(self):
        self.ctx.setEffect(6)
        self.ctx.serial().write(6)

    def setBLUE2(self):
        self.ctx.setEffect(8)
        self.ctx.serial().write(8)

    def setGREEN2(self):
        self.ctx.setEffect(7)
        self.ctx.serial().write(7)

    def setWHITE2(self):
        self.ctx.setEffect(9)
        self.ctx.serial().write(9)

    def setOFF(self):
        self.ctx.setEffect(4)
        self.ctx.serial().write(4)

    def setRAINBOW(self):
        self.ctx.setEffect(10)
        self.ctx.serial().write(10)

    def setRAINBOW2(self):
        self.ctx.setEffect(11)
        self.ctx.serial().write(11)

    def setTHEATERCHASERAINBOW(self):
        self.ctx.setEffect(12)
        self.ctx.serial().write(12)

    def setCPU(self):
        self.ctx.setEffect(13)
        _thread.start_new_thread(readCPUInfo, (self.ctx, ))

    def openWindows(self):
        self.window = gui_settings.App(self.ctx)
        self.window.show()

    def exit(self):
        sys.exit()
    # To here


# Start gui_sysTray
def main(appctxt):
    trayIcon = SystemTrayIcon(appctxt)
    trayIcon.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
