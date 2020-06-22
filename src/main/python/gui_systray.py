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
        #self.activated.connect(self.setMenu)
        self.setIcon(QtGui.QIcon(self.ctx.icon()))
        self.setMenu()

    # Init sysTray
    def setMenu(self):
        self.monoColor = QtWidgets.QMenu()
        self.monoColor.setTitle("Mono color")

        self.red1 = self.monoColor.addAction("RED")
        self.red1.triggered.connect(self.setRED1)

        self.blue1 = self.monoColor.addAction("BLUE")
        self.blue1.triggered.connect(self.setBLUE1)

        self.green1 = self.monoColor.addAction("GREEN")
        self.green1.triggered.connect(self.setGREEN1)

        self.white1 = self.monoColor.addAction("WHITE")
        self.white1.triggered.connect(self.setWHITE1)

        self.cpu = self.monoColor.addAction("Based on CPU Load")
        self.cpu.triggered.connect(self.setCPU)


        self.theaterChase = QtWidgets.QMenu()
        self.theaterChase.setTitle("Theater Chase")

        self.red2 = self.theaterChase.addAction("RED")
        self.red2.triggered.connect(self.setRED2)

        self.blue2 = self.theaterChase.addAction("BLUE")
        self.blue2.triggered.connect(self.setBLUE2)

        self.green2 = self.theaterChase.addAction("GREEN")
        self.green2.triggered.connect(self.setGREEN2)

        self.white2 = self.theaterChase.addAction("WHITE")
        self.white2.triggered.connect(self.setWHITE2)


        self.rainbowMenu = QtWidgets.QMenu()
        self.rainbowMenu.setTitle("RAINBOW")

        self.rainbow1 = self.rainbowMenu.addAction("RAINBOW")
        self.rainbow1.triggered.connect(self.setRAINBOW)

        self.rainbow2 = self.rainbowMenu.addAction("RAINBOW V2")
        self.rainbow2.triggered.connect(self.setRAINBOW2)

        self.theaterChaseRainbow = self.rainbowMenu.addAction("THEATERCHASERAINBOW")
        self.theaterChaseRainbow.triggered.connect(self.setTHEATERCHASERAINBOW)

        self.menu.addMenu(self.monoColor)
        self.menu.addMenu(self.theaterChase)
        self.menu.addMenu(self.rainbowMenu)

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
