import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
# from PyQt5.QtWidgets import QTreeWidgetItem

from gui.ui_mainwindow import Ui_MainWindow
from gui.ui_enterkey import Ui_EnterKey
from src.aes import AESCipher, encrypt_file, decrypt_file, decrypt_runtime
from src.utils import rotate_file_right, rotate_file_left, delete_path


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image = None
        self.cipher = None
        self.fullscreen = False
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
        self.ui.filesTree.itemSelectionChanged.connect(self._select_item)
        self.ui.actionOpenFolder.triggered.connect(self._open_folder)
        self.ui.actionRotateLeft.triggered.connect(self._rotate_left)
        self.ui.actionRotateRight.triggered.connect(self._rotate_right)
        self.ui.actionDelete.triggered.connect(self._delete_file)
        self.ui.actionEnterKey.triggered.connect(self._enter_key)
        self.ui.actionEncrypt.triggered.connect(self._crypt)
        self.ui.actionFullscreen.triggered.connect(self._fullscreen)

        self.enterKeyDialog.ui.pushButton_cancel.clicked.connect(self._cancel_key)
        self.enterKeyDialog.ui.pushButton_apply.clicked.connect(self._apply_key)
        self.update_crypt_status('sample.path')
        # self.showFullScreen()
        self._open_folder()
        self.showMaximized()

    # ===SLOTS===
    def _fullscreen(self):
        if not self.fullscreen:
            self.showFullScreen()
            self.ui.actionFullscreen.setIcon(QIcon('images/icons/close_full.svg'))
            self.ui.actionFullscreen.setText('Window')
            # close_full.svg
        else:
            self.showMaximized()
            self.ui.actionFullscreen.setIcon(QIcon('images/icons/open_full.svg'))
            self.ui.actionFullscreen.setText('Fullscreen')
        self.fullscreen = not self.fullscreen

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
        self._select_item()
        self.enterKeyDialog.ui.keyField.setText('')
        self.enterKeyDialog.done(200)

    def update_crypt_status(self, path):
        ext = os.path.splitext(path)[1]
        if self.cipher is None:
            self.ui.actionEncrypt.setText('Need key')
            self.ui.actionEncrypt.setDisabled(True)
            self.ui.actionEncrypt.setIcon(QIcon('images/icons/not_locked.svg'))
            self.ui.actionEncrypt.mode = 'disable'
        else:
            if ext == '.aes':
                self.ui.actionEncrypt.setText('Decrypt')
                self.ui.actionEncrypt.setEnabled(True)
                self.ui.actionEncrypt.setIcon(QIcon('images/icons/lock_open.svg'))
                self.ui.actionEncrypt.mode = 'decrypt'
            else:
                self.ui.actionEncrypt.setText('Encrypt')
                self.ui.actionEncrypt.setEnabled(True)
                self.ui.actionEncrypt.setIcon(QIcon('images/icons/lock.svg'))
                self.ui.actionEncrypt.mode = 'encrypt'

    def _crypt(self):
        try:
            path = self.ui.filesTree.get_path()
        except AttributeError:  # TODO: Temp solution
            self.ui.actionEncrypt.setText('Select file first')
            self.ui.actionEncrypt.setEnabled(False)
        else:
            if self.ui.actionEncrypt.mode == 'encrypt':
                encrypt_file(path, self.cipher)
                self._delete_file()
                self._select_item(path + '.aes')
            elif self.ui.actionEncrypt.mode == 'decrypt':
                decrypt_file(path, self.cipher)
                self._delete_file()
                self._select_item(os.path.splitext(path)[0])

    def _runtime_decrypt(self, path):
        image = QPixmap()
        file_bytes, success = decrypt_runtime(path, self.cipher)
        ext = os.path.splitext(os.path.splitext(path)[0])[1]
        image.loadFromData(file_bytes, ext.upper())
        if success:
            pass
        return image

    def _update_image(self):
        if self.image is not None:
            w = self.ui.imageView.width()
            h = self.ui.imageView.height()
            self.ui.imageView.setPixmap(self.image.scaled(w, h, QtCore.Qt.KeepAspectRatio))
        else:
            self.ui.imageView.setText("Nothing to show :(")

    def _rotate_left(self):
        path = self.ui.filesTree.get_path()
        rotate_file_left(path)
        self.image = QPixmap(path)
        self._update_image()

    def _rotate_right(self):
        path = self.ui.filesTree.get_path()
        rotate_file_right(path)
        self.image = QPixmap(path)
        self._update_image()

    def _delete_file(self):
        delete_path(self.ui.filesTree.get_path())
        self.image = None
        self._update_image()
        self.ui.filesTree.delete_item()

    def resizeEvent(self, event):  # Work only while mainwindow resize
        self._resize_image()

    def _resize_image(self):
        if self.image is not None:
            self._update_image()

    def _select_item(self, old_path_if_changed=None):
        if old_path_if_changed is not None:
            path = old_path_if_changed  # TODO: Need real selection
        else:
            path = self.ui.filesTree.get_path()

        self.update_crypt_status(path)
        if os.path.isdir(path):
            self.image = None
            self.ui.imageView.setText("Can't show, folder selected.")
        else:
            ext = os.path.splitext(path)[1].replace('.', '')
            supported_ext = QtGui.QImageReader.supportedImageFormats()
            if ext in [str(ext, 'utf-8') for ext in supported_ext]:
                self.image = QPixmap(path)
                self._update_image()
            elif ext == 'aes':
                try:
                    self.image = self._runtime_decrypt(path)
                except FileNotFoundError:
                    pass
                self._update_image()
            else:
                text = 'Can not show. Supported image formats: \n' + \
                       ', '.join([str(ext, 'utf-8') for ext in supported_ext]) + \
                       '\n\nYou still can encrypt ot decrypt file!'
                self.ui.imageView.setText(text)

    # Select path button
    def _open_folder(self):
        folder_dialog = QtWidgets.QFileDialog()
        self.root_path = folder_dialog.getExistingDirectory(None, "Select Folder")  # TODO: Why is this to slow?
        if self.root_path == '':
            return
        self.ui.filesTree.clear()
        self.ui.filesTree.load_project_structure(self.root_path)


class EnterKeyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(EnterKeyDialog, self).__init__()
        self.ui = Ui_EnterKey()
        self.ui.setupUi(self)

        icon = QtGui.QIcon('images/icon.png')
        self.setWindowIcon(icon)

# msg = QtWidgets.QMessageBox()
# msg.setIcon(QtWidgets.QMessageBox.Warning)
# msg.setWindowTitle("Enter key to decrypt")
# msg.setText('Enter key to decrypt. ')
# msg.setInformativeText('Enter key to decrypt')
# msg.setDefaultButton(QtWidgets.QMessageBox.Save)
# msg.exec()
