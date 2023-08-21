from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from gui.ui_folderencrypt import Ui_FolderEncrypt
from gui.ui_folderdecrypt import Ui_FolderDecrypt


class FolderEncrypt(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FolderEncrypt()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.ui.progressBar.setVisible(False)
        self.cur_path = None
        self.cipher = None

    def set_values(self, cur_path, cipher):
        self.cur_path = cur_path
        self.cipher = cipher
        self.ui.path.setText(cur_path)

    def get_select(self):
        if self.ui.radioButton_one.isChecked():
            return 'one'
        elif self.ui.radioButton_files.isChecked():
            return 'files'
        else:
            return None

    def reset(self):
        self.cur_path = None
        self.cipher = None
        self.ui.progressBar.setVisible(False)
        self.ui.progressBar.setValue(0)

    def set_progress_bar_value(self, procent: int):
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setValue(procent)


class FolderDecrypt(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FolderDecrypt()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.cur_path = None

    def set_values(self, cur_path):
        self.cur_path = cur_path
        self.ui.path.setText(cur_path)

    def reset(self):
        self.cur_path = None
        self.ui.progressBar.setValue(0)

    def set_progress_bar_value(self, procent: int):
        self.ui.progressBar.setValue(procent)
