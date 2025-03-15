from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog

from src.gui_generative.ui_settings import Ui_SettingsDialog
from src.utils.utils import resource_path as rp
from src.utils.utils import about


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(rp('src/img/icon.svg')))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.ui.selectCopyFolder.clicked.connect(self._select_target_folder)
        self.ui.enableCopyToTarget.clicked.connect(self._disable_enable_target)

    def apply(self, parent):
        parent.db['action_rotate_left'] = self.ui.checkRotateLeft.isChecked()
        parent.db['action_rotate_right'] = self.ui.checkRotateRight.isChecked()
        parent.db['action_delete'] = self.ui.checkDelete.isChecked()
        parent.db['action_fit_view'] = self.ui.checkFitView.isChecked()
        parent.db['action_fullscreen'] = self.ui.checkFullscreen.isChecked()
        parent.db['action_fullscreen'] = self.ui.checkFullscreen.isChecked()
        parent.db['action_encrypt_decrypt'] = self.ui.checkEncrypt.isChecked()
        parent.db['copy_to_target'] = self.ui.enableCopyToTarget.isChecked()
        if self.ui.labelTarget.text().strip() != 'Copy target path':
            parent.db['copy_to_target_path'] = self.ui.labelTarget.text()
        parent.update_actions_status(parent.cur_path)

    def reset(self, parent):
        self.ui.checkRotateLeft.setChecked(parent.db['action_rotate_left'])
        self.ui.checkRotateRight.setChecked(parent.db['action_rotate_right'])
        self.ui.checkDelete.setChecked(parent.db['action_delete'])
        self.ui.checkFitView.setChecked(parent.db['action_fit_view'])
        self.ui.checkFullscreen.setChecked(parent.db['action_fullscreen'])
        self.ui.checkFullscreen.setChecked(parent.db['action_fullscreen'])
        self.ui.checkEncrypt.setChecked(parent.db['action_encrypt_decrypt'])
        self.ui.enableCopyToTarget.setChecked(parent.db['copy_to_target'])
        self.ui.labelTarget.setEnabled(parent.db['copy_to_target'])
        self.ui.selectCopyFolder.setEnabled(parent.db['copy_to_target'])
        if 'copy_to_target_path' in parent.db:
            self.ui.labelTarget.setText(str(parent.db['copy_to_target_path']))
        else:
            self.ui.labelTarget.setText('Copy target path')
        self.ui.label_about.setText(about())

    def _select_target_folder(self):
        folder_dialog = QFileDialog()
        self.ui.labelTarget.setText(folder_dialog.getExistingDirectory(None, "Select Folder"))

    def _disable_enable_target(self):
        self.ui.labelTarget.setEnabled(self.ui.enableCopyToTarget.isChecked())
        self.ui.selectCopyFolder.setEnabled(self.ui.enableCopyToTarget.isChecked())
