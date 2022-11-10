import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileSystemModel

from gui.ui_mainwindow import Ui_MainWindow
from gui.ui_enterkey import Ui_EnterKey
from src.aes import AESCipher, encrypt_file, decrypt_file, decrypt_runtime, read_file
from src.utils import rotate_file_right, rotate_file_left, delete_path
from src.filestree import gettype, is_rotatable


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image = None
        self.cipher = None
        self.cur_path = None
        self.full_screen = False
        self.enterKeyDialog = EnterKeyDialog()

        # === TOOLBAR ICONS ===
        self.setWindowIcon(QIcon('images/icon.png'))
        self.ui.actionOpenFolder.setIcon(QIcon('images/icons/folder_open.svg'))
        self.ui.actionTreeView.setIcon(QIcon('images/icons/tree.svg'))
        self.ui.actionRotateLeft.setIcon(QIcon('images/icons/rotate_left.svg'))
        self.ui.actionRotateRight.setIcon(QIcon('images/icons/rotate_right.svg'))
        self.ui.actionDelete.setIcon(QIcon('images/icons/delete.svg'))
        self.ui.actionActualSize.setIcon(QIcon('images/icons/zoom_in.svg'))
        self.ui.actionFitSize.setIcon(QIcon('images/icons/zoom_out.svg'))
        self.ui.actionFullscreen.setIcon(QIcon('images/icons/open_full.svg'))
        self.ui.actionEnterKey.setIcon(QIcon('images/icons/key.svg'))
        self.ui.actionEncrypt.setIcon(QIcon('images/icons/lock.svg'))

        # Not done
        self.ui.actionTreeView.setDisabled(True)
        self.ui.actionActualSize.setDisabled(True)
        self.ui.actionFitSize.setDisabled(True)

        # ===CONNECTS===
        # self.ui.filesTree.itemSelectionChanged.connect(self._select_item)
        self.ui.filesTree.selectionModel().currentChanged.connect(self._select_item)
        self.ui.actionOpenFolder.triggered.connect(self._open_folder)
        self.ui.actionRotateLeft.triggered.connect(self._rotate_left)
        self.ui.actionRotateRight.triggered.connect(self._rotate_right)
        self.ui.actionDelete.triggered.connect(self._delete_file)
        self.ui.actionEnterKey.triggered.connect(self._enter_key)
        self.ui.actionEncrypt.triggered.connect(self._crypt)
        self.ui.actionFullscreen.triggered.connect(self._fullscreen)

        self.enterKeyDialog.ui.pushButton_cancel.clicked.connect(self._cancel_key)
        self.enterKeyDialog.ui.pushButton_apply.clicked.connect(self._apply_key)
        self.update_actions_status('sample.path')
        self.showMaximized()
        self._open_last_folder()

    # ===SLOTS===
    def _fullscreen(self):
        if not self.full_screen:
            self.showFullScreen()
            self.ui.actionFullscreen.setIcon(QIcon('images/icons/close_full.svg'))
            self.ui.actionFullscreen.setText('Window')
        else:
            self.showMaximized()
            self.ui.actionFullscreen.setIcon(QIcon('images/icons/open_full.svg'))
            self.ui.actionFullscreen.setText('Fullscreen')
        self.full_screen = not self.full_screen

    def _exit_fullscreen(self):
        self.showMaximized()

    def _enter_key(self):
        self.enterKeyDialog.show()

    def _cancel_key(self):
        self.enterKeyDialog.ui.keyField.setText('')
        self.enterKeyDialog.done(200)

    def _apply_key(self):
        if self.enterKeyDialog.ui.keyField.text() != '':
            self.cipher = AESCipher(self.enterKeyDialog.ui.keyField.text())
        self.enterKeyDialog.ui.keyField.setText('')
        self.enterKeyDialog.done(200)
        self.update_actions_status(self.cur_path)

    def update_actions_status(self, path):
        # TODO: Is all image type can rotate?
        if gettype(path) == 'image' and is_rotatable(path):
            self.ui.actionRotateLeft.setEnabled(True)
            self.ui.actionRotateRight.setEnabled(True)
        else:
            self.ui.actionRotateLeft.setDisabled(True)
            self.ui.actionRotateRight.setDisabled(True)

        if self.cipher is None:
            self.ui.actionEncrypt.setText('Need key')
            self.ui.actionEncrypt.setDisabled(True)
            self.ui.actionEncrypt.setIcon(QIcon('images/icons/not_locked.svg'))
            self.ui.actionEncrypt.mode = 'disable'
        else:
            if gettype(path) is None:
                self.ui.actionEncrypt.setText('Select file first')
                self.ui.actionEncrypt.setDisabled(True)
                self.ui.actionEncrypt.setIcon(QIcon('images/icons/not_locked.svg'))
                self.ui.actionEncrypt.mode = 'disable'
            elif gettype(path) == 'folder':
                self.ui.actionEncrypt.setText('Folder selected')
                self.ui.actionEncrypt.setDisabled(True)
                self.ui.actionEncrypt.setIcon(QIcon('images/icons/not_locked.svg'))
                self.ui.actionEncrypt.mode = 'disable'
            elif gettype(path) == 'aes':
                self.ui.actionEncrypt.setText('Decrypt on disk')
                self.ui.actionEncrypt.setEnabled(True)
                self.ui.actionEncrypt.setIcon(QIcon('images/icons/lock_open.svg'))
                self.ui.actionEncrypt.mode = 'decrypt'
            else:
                self.ui.actionEncrypt.setText('Encrypt on disk')
                self.ui.actionEncrypt.setEnabled(True)
                self.ui.actionEncrypt.setIcon(QIcon('images/icons/lock.svg'))
                self.ui.actionEncrypt.mode = 'encrypt'

    def _crypt(self):
        try:
            if self.ui.actionEncrypt.mode == 'encrypt':
                encrypt_file(self.cur_path, self.cipher)
            elif self.ui.actionEncrypt.mode == 'decrypt':
                decrypt_file(self.cur_path, self.cipher)
            self._delete_file()
        except FileNotFoundError:
            return None

    def _read_image(self, path):
        try:
            image = QPixmap()
            file_bytes = read_file(path)
            ext = os.path.splitext(os.path.splitext(path)[0])[1]
            read_success = image.loadFromData(file_bytes, ext.upper())
            if not read_success:
                self.ui.actionRotateRight.setDisabled(True)
                self.ui.actionRotateLeft.setDisabled(True)
                file_bytes = read_file('images/broken_image.png')
                image.loadFromData(file_bytes, ext.upper())
        except FileNotFoundError:
            return None
        return image

    def _runtime_decrypt(self, path):
        try:
            image = QPixmap()
            file_bytes, success = decrypt_runtime(path, self.cipher)
            ext = os.path.splitext(os.path.splitext(path)[0])[1]
            read_success = image.loadFromData(file_bytes, ext.upper())
            if not read_success:
                file_bytes = read_file('images/encrypted_with_another_key.png')
                image.loadFromData(file_bytes, ext.upper())
        except FileNotFoundError:
            return None
        return image

    def _update_image(self, lazily=False):
        if not lazily:
            if gettype(self.cur_path) == 'image':
                self.image = self._read_image(self.cur_path)
            elif gettype(self.cur_path) == 'aes':
                self.image = self._runtime_decrypt(self.cur_path)
            else:
                self.image = None

        if self.image is not None:
            w = self.ui.imageView.width()
            h = self.ui.imageView.height()
            # noinspection PyUnresolvedReferences
            self.ui.imageView.setPixmap(self.image.scaled(w, h, QtCore.Qt.KeepAspectRatio))
        else:
            self.ui.imageView.setText("Nothing to show :(")

    def _rotate_left(self):
        rotate_file_left(self.cur_path)
        self._update_image()

    def _rotate_right(self):
        rotate_file_right(self.cur_path)
        self._update_image()

    def _delete_file(self):
        delete_path(self.cur_path)
        self._update_image()

    def resizeEvent(self, event):
        self._update_image(lazily=True)

    def _select_item(self, cur, prev):
        self.cur_path = QFileSystemModel().filePath(cur)
        self.prev_path = QFileSystemModel().filePath(prev)
        # print(self.prev_path, " TO ",self.cur_path)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _open_folder(self):
        folder_dialog = QtWidgets.QFileDialog()
        self.root_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        if self.root_path == '':
            return
        self.ui.filesTree.change_root(self.root_path)
        with open('metadata.txt', 'w+') as f:
            f.write(str(self.root_path))

    def _open_last_folder(self):
        try:
            with open('metadata.txt') as f:
                last_path = f.read()
            if os.path.exists(last_path):
                self.root_path = last_path
                self.ui.filesTree.change_root(self.root_path)
        except FileNotFoundError as err:
            print(err, "metadata.txt not found")


class EnterKeyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(EnterKeyDialog, self).__init__()

        self.ui = Ui_EnterKey()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.png'))
