import sys
import shutil
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class Error_database():
    def __init__(self, icon = None):
        self.icon = icon
        self.app = QtWidgets.QApplication([])

    def spawn(self):
        check = QMessageBox()
        
        if self.icon != None:
            check.setWindowIcon(self.icon)

        check.setWindowTitle("Error database")
        
        check.setText("Database not found or corrupted, recreate with default settings?")
        check.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        check = check.exec()

        if check == QMessageBox.Yes:
            try:
                shutil.copy("db_general_defaulf.json", "db_general.json")
                return True
            except Exception as Ex:
                print(Ex)
                self.fatal_error()
        else:
            self.fatal_error()
    
    def fatal_error(self):
        check = QMessageBox()
        check.setWindowTitle("Error database")
        check.setText("Fatal error")
        check = check.exec()
