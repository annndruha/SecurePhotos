from PyQt5 import QtWidgets

from src.gui.icons import Icons


class UserMessage(QtWidgets.QMessageBox):
    """Info or error message window"""
    def __init__(self, text, level="Critical"):
        super(UserMessage, self).__init__()
        self.setWindowIcon(Icons.favicon)
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
