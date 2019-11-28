import sys
import time
import _thread
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QCoreApplication, QDir, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QMainWindow, QMenu, QPushButton, QSystemTrayIcon,
                             QVBoxLayout, QWidget, QListWidget, QAction,
                             QErrorMessage, QMessageBox,
                             QFileDialog)

class Debug(QMainWindow):
    def __init__(self, icon):
        QMainWindow.__init__(self)
        self.setWindowIcon(icon)
        self.setMinimumSize(QSize(700, 400))
        self.setMaximumSize(QSize(700, 400))
        self.index = 0
        self.view_error = False
        
    def initUI(self):
        self.setWindowTitle(self.data.language_class.r_string(self.data.s_language(), "debug"))
    
        #Creo i campi di testo
        self.text1 = QListWidget()
        
        self.checkbox = QCheckBox((self.data.language_class.r_string(self.data.s_language(), "view_only_error")), self)
        self.checkbox.stateChanged.connect(self.error_select)

        # Setup OK button
        self.button1 = QPushButton(self.data.language_class.r_string(self.data.s_language(), "clean"), self)
        self.button1.clicked.connect(self.clean)
        
        self.button2 = QPushButton(self.data.language_class.r_string(self.data.s_language(), "update"), self)
        self.button2.clicked.connect(self.update)
        
        self.button3 = QPushButton(self.data.language_class.r_string(self.data.s_language(), "save_on_file"), self)
        self.button3.clicked.connect(self.save)
        
        self.exit_button = QPushButton(self.data.language_class.r_string(self.data.s_language(), "exit"), self)
        self.exit_button.clicked.connect(self.hide)
        
        #Creo i diversi layout
        myQWidget = QWidget()
        self.setCentralWidget(myQWidget)

        VerticalLayoutA = QVBoxLayout()
        HorizontalLayoutA = QHBoxLayout()

        HorizontalLayoutA.addWidget(self.button1)
        HorizontalLayoutA.addWidget(self.button2)
        HorizontalLayoutA.addWidget(self.button3)
        HorizontalLayoutA.addWidget(self.exit_button)

        VerticalLayoutA.addWidget(self.text1)
        VerticalLayoutA.addWidget(self.checkbox)
        VerticalLayoutA.addLayout(HorizontalLayoutA)

        myQWidget.setLayout(VerticalLayoutA)

        _thread.start_new_thread(self.update_rec, ())
    
    def set_data(self, data):
        self.data = data
    
    def error_select(self):
        if self.checkbox.isChecked() == False:
            self.view_error = False
        else:
            self.view_error = True
        self.update()

    def save(self):
        try:
            with open(self.saveFileDialog(), "a") as ptrfile:
                for element in self.data.debug_class.return_data():
                    ptrfile.write(element + "\n")
            QMessageBox.question(self, self.data.language_class.r_string(self.data.s_language(), "title"), self.data.language_class.r_string(self.data.s_language(), "save_complete"), QMessageBox.Cancel)
            self.data.debug_class.add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.data.language_class.r_string(self.data.s_language(), "export_file"))

        except Exception as ex:
            self.data.debug_class.add(str(time.asctime( time.localtime(time.time()) )) + ": " + self.data.language_class.r_string(self.data.s_language(), "export_error") + str(ex), 1)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, self.data.language_class.r_string(self.data.s_language(), "debug"),"","All files(*)", options=options)
        return(fileName)

    def update_rec(self, sec = 5):
        while True:
            self.update()
            time.sleep(sec)

    #to-do: optimize
    def update(self):
        self.text1.clear()
        for item in self.data.debug_class.return_data().items():
            if self.view_error == True and item[1] == 1:
                self.text1.addItem(item[0])
                self.index = 1

            if self.view_error == False:
                self.text1.addItem(item[0])
                self.index = 1

        if self.index == 0:
            self.text1.addItem(self.data.language_class.r_string(self.data.s_language(), "no_element"))

        else:
            self.index = 0

    def clean(self):
        self.data.debug_class.clean()
        self.update()

    def closeEvent(self, event):
        self.hide()
        event.ignore()
