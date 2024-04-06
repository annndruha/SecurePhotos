from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QLineEdit

from src.gui_generative.ui_enterkey import Ui_EnterKey
from src.utils.aes import AESCipher
from src.utils.utils import resource_path as rp


class EnterKeyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(EnterKeyDialog, self).__init__()
        self.ui = Ui_EnterKey()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(rp('src/img/icon.svg')))
        self.ui.keyField.textChanged.connect(self._compare_key)
        self.ui.keyRepeat.textChanged.connect(self._compare_key)
        self.ui.keyField.setEchoMode(QLineEdit.Password)
        self.ui.keyRepeat.setEchoMode(QLineEdit.Password)
        self.palette_ok = QPalette()
        self.palette_ok.setColor(QPalette.WindowText, QColor(0, 180, 0))
        self.palette_not_ok = QPalette()
        self.palette_not_ok.setColor(QPalette.WindowText, QColor(255, 0, 0))
        self.palette_neutral = QPalette()
        self.palette_neutral.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def _recalc_hash(self):
        if self.ui.keyField.text() != '':
            dummy_cipher = AESCipher(self.ui.keyField.text())
            _hash = dummy_cipher.hash()[-4:]
            self.ui.pushButton_apply.setEnabled(True)
            self.ui.hash_field.setText(_hash)
            self.ui.hash_field.setPalette(self.palette_ok)
        else:
            self.ui.pushButton_apply.setDisabled(True)
            self.ui.hash_field.setText('HASH')
            self.ui.hash_field.setPalette(self.palette_neutral)

    def _compare_key(self):
        dummy_cipher1 = AESCipher(self.ui.keyField.text())
        dummy_cipher2 = AESCipher(self.ui.keyRepeat.text())
        if (dummy_cipher1.hash() == dummy_cipher2.hash()) or self.ui.keyRepeat.text() == '':
            self.ui.pushButton_apply.setEnabled(True)
            self._recalc_hash()
        else:
            self.ui.pushButton_apply.setDisabled(True)
            self.ui.hash_field.setText('Password mismatch')
            self.ui.hash_field.setPalette(self.palette_not_ok)

    def reset(self):
        self.ui.keyField.setText('')
        self.ui.keyRepeat.setText('')
        self.ui.hash_field.setPalette(self.palette_neutral)
