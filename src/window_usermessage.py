from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon


class UserMessage(QtWidgets.QMessageBox):
    def __init__(self, text, level="Critical"):
        super(UserMessage, self).__init__()
        self.setWindowIcon(QIcon('images/icon.png'))
        if level == "Critical":
            self.setIcon(QtWidgets.QMessageBox.Critical)
            self.setWindowTitle("Critical error")
        elif level == "Warning":
            self.setIcon(QtWidgets.QMessageBox.Warning)
            self.setWindowTitle("Warning")
        else:
            self.setIcon(QtWidgets.QMessageBox.Information)
            self.setWindowTitle("Info")
        self.setText(text)
        self.exec()
