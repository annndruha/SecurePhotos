from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QLineEdit

from gui.ui_enterkey import Ui_EnterKey
from src.aes import AESCipher
from gui.ui_folderencrypt import Ui_FolderEncrypt


class FolderEncrypt(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FolderEncrypt()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.png'))
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
