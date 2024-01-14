from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from gui.ui_progressbar import Ui_ProgressBarDialog


class ProgressBarDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ProgressBarDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self._canceled = False

    def set_state(self, percent: int, text: str):
        self.ui.progress_text.setText(text)
        self.ui.progressBar.setValue(percent)
        QApplication.processEvents()

    def reset(self):
        self._canceled = False
        self.ui.progressBar.setValue(0)
        self.ui.progress_text.setText('Initializing...')

    def was_canceled(self):
        return self._canceled

    def cancel(self):
        self._canceled = True
