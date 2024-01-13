from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from gui.ui_progressbar import Ui_ProgressBarDialog


class ProgressBarDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ProgressBarDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self._canceled = False

    def set_progress_bar_value(self, percent: int):
        self.ui.progressBar.setValue(percent)

    def set_progress_text(self, text):
        self.ui.progress_text.setText(text)

    def reset(self):
        self.ui.progressBar.setValue(0)
        self.ui.progress_text.setText('Initializing...')

    def was_canceled(self):
        return self._canceled

    def cancel(self):
        self._canceled = True
