import _thread

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import sys

import gui_settings
import gui_colorPicker
from PyQt5.QtCore import pyqtSlot

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

        self.setColor1 = self.monoColor.addAction("Set color from palette")
        self.setColor1.triggered.connect(self.setColorFromPalette1)

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

        self.setColor2 = self.theaterChase.addAction("Set color from palette")
        self.setColor2.triggered.connect(self.setColorFromPalette2)

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
        self.ctx.setEffect(10255000000)
        self.ctx.serial().write(10255000000)

    def setBLUE1(self):
        self.ctx.setEffect(10000000255)
        self.ctx.serial().write(10000000255)

    def setGREEN1(self):
        self.ctx.setEffect(10000255000)
        self.ctx.serial().write(10000255000)

    def setWHITE1(self):
        self.ctx.setEffect(10255255255)
        self.ctx.serial().write(10255255255)

    def setRED2(self):
        self.ctx.setEffect(11255000000)
        self.ctx.serial().write(11255000000)

    def setBLUE2(self):
        self.ctx.setEffect(11000000255)
        self.ctx.serial().write(11000000255)

    def setGREEN2(self):
        self.ctx.setEffect(11000255000)
        self.ctx.serial().write(11000255000)

    def setWHITE2(self):
        self.ctx.setEffect(11255255255)
        self.ctx.serial().write(11255255255)

    def setOFF(self):
        self.ctx.setEffect(0)
        self.ctx.serial().write(0)

    def setRAINBOW(self):
        self.ctx.setEffect(130)
        self.ctx.serial().write(130)

    def setRAINBOW2(self):
        self.ctx.setEffect(131)
        self.ctx.serial().write(131)

    def setTHEATERCHASERAINBOW(self):
        self.ctx.setEffect(132)
        self.ctx.serial().write(132)

    def setCPU(self):
        self.ctx.setEffect(12)
        _thread.start_new_thread(readCPUInfo, (self.ctx, ))

    @pyqtSlot()
    def setColorFromPalette1(self):
        self.window = gui_colorPicker.App(self.ctx, "10")
        self.window.show()

    @pyqtSlot()
    def setColorFromPalette2(self):
        self.window = gui_colorPicker.App(self.ctx, "11")
        self.window.show()

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
