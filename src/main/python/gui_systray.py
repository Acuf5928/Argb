import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import sys

import gui_settings


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
        status = self.ctx.status
        self.menu.clear()

        if status is None:
            self.on = self.menu.addAction("ON")
            self.on.triggered.connect(self.setON)

            self.off = self.menu.addAction("OFF")
            self.off.triggered.connect(self.setOFF)
        else:

            self.lux = self.menu.addAction("Lux: " + str(status["lux"]))
            self.lux.setEnabled(False)

            self.menu.addSeparator()

            if status["statusLed"] is 0:
                self.on = self.menu.addAction("ON")
                self.on.triggered.connect(self.setON)
            else:
                self.off = self.menu.addAction("OFF")
                self.off.triggered.connect(self.setOFF)

        self.auto = self.menu.addAction("AUTO")
        self.auto.triggered.connect(self.setAUTO)

        self.windows = self.menu.addAction("Settings")
        self.windows.triggered.connect(self.openWindows)

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)

        self.setContextMenu(self.menu)

    # Set functions of all menu elements, from here:
    def setAUTO(self):
        self.ctx.serial().write(2)

    def setON(self):
        self.ctx.serial().write(1)

    def setOFF(self):
        self.ctx.serial().write(0)

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
