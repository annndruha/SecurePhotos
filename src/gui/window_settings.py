from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QLineEdit

from src.gui_generative.ui_settings import Ui_SettingsDialog
from src.utils.utils import resource_path as rp


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(rp('src/img/icon.svg')))
        # self.ui.keyField.textChanged.connect(self._compare_key)
        # self.ui.keyRepeat.textChanged.connect(self._compare_key)
        # self.ui.keyField.setEchoMode(QLineEdit.Password)
        # self.ui.keyRepeat.setEchoMode(QLineEdit.Password)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def apply(self):
        pass

    def reset(self):
        pass
        # self.ui.keyField.setText('')
        # self.ui.keyRepeat.setText('')
        # self.ui.hash_field.setPalette(self.palette_neutral)
