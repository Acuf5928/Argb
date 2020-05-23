import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot


class App(QtWidgets.QMainWindow):

    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setWindowIcon(QtGui.QIcon(ctx.icon()))
        self.setMinimumSize(QtCore.QSize(500, 50))
        self.setMaximumSize(QtCore.QSize(500, 50))

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

        self.text = QtWidgets.QLabel('Serial port:', self)
        self.text.move(10, 10)
        self.text.resize(130, 30)

    @pyqtSlot()
    def comboBoxActivate(self):
        self.ctx.setPort(self.comboBox.currentText())

    # Prevent program exit when clik on X button
    def closeEvent(self, event):
        self.hide()
        event.ignore()
