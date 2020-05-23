import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot


class App(QtWidgets.QMainWindow):

    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setWindowIcon(QtGui.QIcon(ctx.icon()))
        self.setMinimumSize(QtCore.QSize(500, 130))
        self.setMaximumSize(QtCore.QSize(500, 130))

        self.initUI()

    # Init Ui
    def initUI(self):
        self.setWindowTitle(self.ctx.appName())

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.move(165, 10)
        self.comboBox.resize(325, 30)
        self.comboBox.addItem("")
        self.comboBox.addItems(self.ctx.serial().listDevice())
        self.comboBox.setCurrentText(self.ctx.port)
        self.comboBox.currentIndexChanged.connect(self.comboBoxActivate)

        self.textbox1 = QtWidgets.QCheckBox(self)
        self.textbox1.move(165, 50)
        self.textbox1.resize(325, 30)
        self.textbox1.setChecked(self.ctx.statusLed)
        self.textbox1.stateChanged.connect(self.textbox1Activate)

        self.textbox2 = QtWidgets.QCheckBox(self)
        self.textbox2.move(165, 90)
        self.textbox2.resize(325, 30)
        self.textbox2.setChecked(self.ctx.autoLed)
        self.textbox2.stateChanged.connect(self.textbox2Activate)

        self.text = QtWidgets.QLabel('Serial port:', self)
        self.text.move(10, 10)
        self.text.resize(130, 30)

        self.text1 = QtWidgets.QLabel('Set ON on connect:', self)
        self.text1.move(10, 50)
        self.text1.resize(130, 30)

        self.text2 = QtWidgets.QLabel('Auto on connect:', self)
        self.text2.move(10, 90)
        self.text2.resize(130, 30)

    @pyqtSlot()
    def comboBoxActivate(self):
        self.ctx.setPort(self.comboBox.currentText())

    @pyqtSlot()
    def textbox1Activate(self):
        self.ctx.setEnable(self.textbox1.isChecked())

    @pyqtSlot()
    def textbox2Activate(self):
        self.ctx.setAuto(self.textbox2.isChecked())

    # Prevent program exit when clik on X button
    def closeEvent(self, event):
        self.hide()
        event.ignore()
