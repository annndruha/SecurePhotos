from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QLineEdit

from src.gui_generative.ui_settings import Ui_SettingsDialog
from src.utils.utils import resource_path as rp


# from src.gui.window_app import MainWindow


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(rp('src/img/icon.svg')))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def apply(self, parent):
        parent.db['action_rotate_left'] = self.ui.checkRotateLeft.isChecked()
        parent.db['action_rotate_right'] = self.ui.checkRotateRight.isChecked()
        parent.db['action_delete'] = self.ui.checkDelete.isChecked()
        parent.db['action_fit_view'] = self.ui.checkFitView.isChecked()
        parent.db['action_fullscreen'] = self.ui.checkFullscreen.isChecked()
        parent.db['action_fullscreen'] = self.ui.checkFullscreen.isChecked()
        parent.db['action_encrypt_decrypt'] = self.ui.checkEncrypt.isChecked()

        parent.update_actions_status(parent.cur_path)

    def reset(self, parent):
        self.ui.checkRotateLeft.setChecked(parent.db['action_rotate_left'])
        self.ui.checkRotateRight.setChecked(parent.db['action_rotate_right'])
        self.ui.checkDelete.setChecked(parent.db['action_delete'])
        self.ui.checkFitView.setChecked(parent.db['action_fit_view'])
        self.ui.checkFullscreen.setChecked(parent.db['action_fullscreen'])
        self.ui.checkFullscreen.setChecked(parent.db['action_fullscreen'])
        self.ui.checkEncrypt.setChecked(parent.db['action_encrypt_decrypt'])
