from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from gui.progressbar_onefile import Ui_ProgressBarOneFileDialog
from src.utils import size_to_text


class ProgressBarOneFileDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ProgressBarOneFileDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.ui.pushButton_ok.setDisabled(True)
        self._canceled = False

    def set_state(self, state: str, size=None):
        if state == 'calc_size':
            self.ui.label_size.setText('In progress...')
        elif state == 'archiving':
            text = f'[~{size_to_text(size)}]' if size is not None else ''
            self.ui.label_size.setText(f'Done {text}')
            self.ui.label_archiving.setText('In progress...')
        elif state == 'encrypting':
            self.ui.label_archiving.setText('Done')
            self.ui.label_encryption.setText('In progress...')
        elif state == 'deleting':
            self.ui.label_encryption.setText('Done')
            self.ui.label_deleting.setText('In progress...')
        elif state == 'done':
            self.ui.label_deleting.setText('Done')
            self.ui.pushButton_ok.setEnabled(True)
            self.ui.pushButton_abort.setDisabled(True)
        QApplication.processEvents()

    def reset(self):
        self._canceled = False
        self.ui.pushButton_ok.setDisabled(True)
        self.ui.pushButton_abort.setEnabled(True)
        self.ui.label_size.setText('Waiting')
        self.ui.label_archiving.setText('Waiting')
        self.ui.label_encryption.setText('Waiting')
        self.ui.label_deleting.setText('Waiting')
        QApplication.processEvents()

    def was_canceled(self):
        QApplication.processEvents()
        return self._canceled

    def cancel(self):
        self._canceled = True
