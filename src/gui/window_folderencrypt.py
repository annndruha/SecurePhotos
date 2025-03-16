from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from src.gui.icons import Icons
from src.gui_generative.ui_folderencrypt import Ui_FolderEncrypt
from src.utils.utils import get_folder_size


class FolderEncryptDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FolderEncrypt()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(Icons.favicon)
        self.cur_path = None
        self.cipher = None

    def set_values(self, cur_path, cipher):
        self.cur_path = cur_path
        self.cipher = cipher
        self.ui.path.setText(cur_path)

    def check_size(self):
        """Disable """
        size = get_folder_size(self.cur_path)
        if size > 1024 * 1024 * 1024 * 2:  # Maximum 2GB
            self.ui.radioButton_one.setDisabled(True)
            self.ui.radioButton_files.setChecked(True)

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
        self.ui.radioButton_one.setEnabled(True)
        self.ui.radioButton_files.setChecked(True)
        print('reset')
