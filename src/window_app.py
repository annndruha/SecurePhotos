import os
import ctypes
import platform
import logging

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QByteArray, QBuffer, QItemSelectionModel
from PyQt5.QtGui import QIcon, QPixmap, QImageReader
from PyQt5.QtWidgets import QFileSystemModel, QGraphicsScene, QProgressDialog
from gui.ui_mainwindow import Ui_MainWindow
from src.aes import (AESCipher,
                     encrypt_file, decrypt_file,
                     encrypt_folder, decrypt_folder, decrypt_folder_file,
                     decrypt_runtime, EmptyCipher, DecryptException)
from src.utils import rotate_file_right, rotate_file_left, delete_path
from src.filestree import gettype, is_rotatable

from src.window_usermessage import UserMessage
from src.window_enterkey import EnterKeyDialog
from src.window_fullscreen import FullScreen
from src.window_folderencrypt import FolderEncrypt
from src.window_progressbar import ProgressBarDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image = None
        self.cipher = None
        self.cur_path = None
        self.full_screen = False
        self.fit_in_view = True
        self.enterKeyDialog = EnterKeyDialog()
        self.folderEncrypt = FolderEncrypt()
        self.progressBarDialog = ProgressBarDialog()
        # self.progress = QProgressDialog(parent=self)

        # === Image scene ===
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.fs = FullScreen()
        self.fs.setScene(self.scene)

        # === APP ICON ===
        if platform.uname()[0] == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('annndruha.SecurePhotos')
        self.setWindowIcon(QIcon('images/icon.png'))

        # === TOOLBAR ICONS ===
        self.ui.actionOpenFolder.setIcon(QIcon('images/icons/folder_open.svg'))
        self.ui.actionTreeView.setIcon(QIcon('images/icons/tree.svg'))
        self.ui.actionRotateLeft.setIcon(QIcon('images/icons/rotate_left.svg'))
        self.ui.actionRotateRight.setIcon(QIcon('images/icons/rotate_right.svg'))
        self.ui.actionDelete.setIcon(QIcon('images/icons/delete.svg'))
        self.ui.actionChangeFit.setIcon(QIcon('images/icons/zoom_none.svg'))
        self.ui.actionFullscreen.setIcon(QIcon('images/icons/open_full.svg'))
        self.ui.actionEnterKey.setIcon(QIcon('images/icons/key.svg'))
        self.ui.actionEncrypt.setIcon(QIcon('images/icons/lock.svg'))
        self.ui.actionFoldeDecrypt.setIcon(QIcon('images/icons/folder_lock_open.svg'))

        # Not done
        self.ui.actionTreeView.setVisible(False)

        # ===CONNECTS===
        self.ui.filesTree.selectionModel().currentChanged.connect(self._select_item)
        self.ui.actionOpenFolder.triggered.connect(self._open_folder)
        self.ui.actionRotateLeft.triggered.connect(self._rotate_left)
        self.ui.actionRotateRight.triggered.connect(self._rotate_right)
        self.ui.actionDelete.triggered.connect(self._delete_file)
        self.ui.actionEnterKey.triggered.connect(self._open_enter_key)
        self.ui.actionEncrypt.triggered.connect(self._crypt)
        self.ui.actionFullscreen.triggered.connect(self._change_fullscreen)
        self.ui.actionChangeFit.triggered.connect(self._change_fit)
        self.ui.actionFoldeDecrypt.triggered.connect(self._decrypt_folder)

        self.enterKeyDialog.ui.pushButton_cancel.clicked.connect(self._reject_enter_key)
        self.enterKeyDialog.ui.pushButton_apply.clicked.connect(self._apply_enter_key)
        self.enterKeyDialog.rejected.connect(self._reject_enter_key)

        self.folderEncrypt.ui.pushButton_cancel.clicked.connect(self._reject_folder_encrypt)
        self.folderEncrypt.ui.pushButton_apply.clicked.connect(self._apply_folder_encrypt)

        self.progressBarDialog.ui.pushButton_abort.clicked.connect(self._abort_folder_crypt)

        self.fs.escapeSignal.connect(self._change_fullscreen)
        self.fs.nextSignal.connect(self._fullscreen_next)
        self.fs.prevSignal.connect(self._fullscreen_prev)

        self.showMaximized()
        self._open_last_folder()
        self.update_actions_status('sample.path')

    # ===SLOTS===
    def _change_fullscreen(self):
        self.full_screen = not self.full_screen
        if self.full_screen:
            self.fs.show()
            self.fs.showFullScreen()
            self.fs.update_image()
            self.ui.actionFullscreen.setIcon(QIcon('images/icons/close_full.svg'))
            self.ui.actionFullscreen.setText('Window')
        else:
            self.fs.showMinimized()
            self.fs.close()
            self.ui.actionFullscreen.setIcon(QIcon('images/icons/open_full.svg'))
            self.ui.actionFullscreen.setText('Fullscreen')

    def _fullscreen_next(self):
        cur = self.ui.filesTree.selectionModel().currentIndex()
        self.ui.filesTree.selectionModel()
        idx = cur.siblingAtRow(cur.row() + 1)

        if idx.isValid() and gettype(QFileSystemModel().filePath(idx)) != 'folder':
            self.ui.filesTree.selectionModel().setCurrentIndex(idx, QItemSelectionModel.ToggleCurrent)
            self.fs.update_image()
        else:
            self._change_fullscreen()

    def _fullscreen_prev(self):
        cur = self.ui.filesTree.selectionModel().currentIndex()
        idx = cur.siblingAtRow(cur.row() - 1)
        if idx.isValid() and gettype(QFileSystemModel().filePath(idx)) != 'folder':
            self.ui.filesTree.selectionModel().setCurrentIndex(idx, QItemSelectionModel.ToggleCurrent)
            self.fs.update_image()
        else:
            self._change_fullscreen()

    def _open_enter_key(self):
        if self.cipher is not None:
            UserMessage("Be careful! This action will delete previous saved password!", "Info")
        self.enterKeyDialog.show()
        self.enterKeyDialog.ui.pushButton_apply.setDisabled(True)

    def _reject_enter_key(self):
        self.enterKeyDialog.reset()
        self.enterKeyDialog.done(200)

    def _apply_enter_key(self):
        if self.enterKeyDialog.ui.keyField.text() != '':
            self.cipher = AESCipher(self.enterKeyDialog.ui.keyField.text())
        self.enterKeyDialog.reset()
        self.enterKeyDialog.done(200)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _reject_folder_encrypt(self):
        print('reject')
        self.folderEncrypt.reset()
        self.folderEncrypt.done(200)

    def _apply_folder_encrypt(self):
        encrypt_type = self.folderEncrypt.get_select()
        path = self.folderEncrypt.cur_path
        cipher = self.folderEncrypt.cipher

        self.folderEncrypt.reset()
        self.folderEncrypt.done(200)
        if encrypt_type == 'files':
            self.progressBarDialog.show()

        try:
            encrypt_folder(encrypt_type, path, cipher, self.progressBarDialog, delete_original=True)
        except EmptyCipher:
            UserMessage("No key!")
        except DecryptException:
            UserMessage("Decrypt error, file probably broken!")
        except FileNotFoundError:
            return None

        self.progressBarDialog.reset()
        self.progressBarDialog.done(200)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _decrypt_folder(self):
        try:
            if gettype(self.cur_path) == 'aes_zip':
                decrypt_folder_file(self.cur_path, self.cipher, delete_original=True)
            else:
                self.progressBarDialog.show()
                decrypt_folder(self.cur_path, self.cipher, self.progressBarDialog, delete_original=True)
                self.progressBarDialog.reset()
                self.progressBarDialog.done(200)
        except EmptyCipher:
            UserMessage("No key!")
        except DecryptException:
            UserMessage("Decrypt error, file probably broken!")
        except FileNotFoundError:
            return None

    def _abort_folder_crypt(self):
        self.progressBarDialog.cancel()

    def _change_fit(self):
        self.fit_in_view = not self.fit_in_view
        self._update_image(lazily=False)

    def _update_fit_status(self):
        nothing_to_fit = self.ui.graphicsView.sceneRect().width() > self.ui.graphicsView.rect().width() or \
                         self.ui.graphicsView.sceneRect().height() > self.ui.graphicsView.rect().height()
        if gettype(self.cur_path) not in ['image', 'aes']:
            nothing_to_fit = True
        if self.fit_in_view and not nothing_to_fit:
            self.ui.actionChangeFit.setEnabled(True)
            self.ui.actionChangeFit.setText('Fit view')
            self.ui.actionChangeFit.setIcon(QIcon('images/icons/zoom_in.svg'))
        elif not self.fit_in_view and not nothing_to_fit:
            self.ui.actionChangeFit.setEnabled(True)
            self.ui.actionChangeFit.setText('Fit view')
            self.ui.actionChangeFit.setIcon(QIcon('images/icons/zoom_out.svg'))
        else:
            self.ui.actionChangeFit.setText("Fit view")
            self.ui.actionChangeFit.setIcon(QIcon('images/icons/zoom_none.svg'))
            self.ui.actionChangeFit.setDisabled(True)

    def update_actions_status(self, path):
        rotation_available = is_rotatable(path)
        self.ui.actionRotateLeft.setEnabled(rotation_available)
        self.ui.actionRotateRight.setEnabled(rotation_available)

        is_fullscreen_available = gettype(path) == 'image'
        self.ui.actionFullscreen.setEnabled(is_fullscreen_available)

        self._update_fit_status()
        self.ui.actionFoldeDecrypt.setVisible(False)
        self.ui.actionEncrypt.setVisible(True)

        if self.cipher is None:
            self.ui.actionEncrypt.setText('Need key')
            self.ui.actionEncrypt.setDisabled(True)
            self.ui.actionEncrypt.setIcon(QIcon('images/icons/not_locked.svg'))
            self.ui.actionEncrypt.mode = 'disable'
            return

        if gettype(path) is None:
            self.ui.actionEncrypt.setText('Select file first')
            self.ui.actionEncrypt.setDisabled(True)
            self.ui.actionEncrypt.setIcon(QIcon('images/icons/not_locked.svg'))
            self.ui.actionEncrypt.mode = 'disable'
        elif gettype(path) == 'folder':
            self.ui.actionEncrypt.setText('Encrypt folder')
            self.ui.actionEncrypt.setEnabled(True)
            self.ui.actionEncrypt.setIcon(QIcon('images/icons/folder_lock.svg'))
            self.ui.actionEncrypt.mode = 'folder'
            self.ui.actionFoldeDecrypt.setVisible(True)
        elif gettype(path) == 'aes_zip':
            self.ui.actionEncrypt.setVisible(False)
            self.ui.actionFoldeDecrypt.setVisible(True)
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
            if self.ui.actionEncrypt.mode == 'folder':
                self.folderEncrypt.set_values(self.cur_path, self.cipher)
                self.folderEncrypt.show()
            elif self.ui.actionEncrypt.mode == 'encrypt':
                encrypt_file(self.cur_path, self.cipher, delete_original=True)
            elif self.ui.actionEncrypt.mode == 'decrypt':
                decrypt_file(self.cur_path, self.cipher, delete_original=True)
            self._update_image()
        except EmptyCipher:
            UserMessage("No key!")
        except DecryptException:
            UserMessage("Decrypt error, file probably broken!")
        except FileNotFoundError:
            return None

    def _read_image(self, path):
        try:
            img_reader = QImageReader(path)
            img_reader.setAutoTransform(True)
            image = img_reader.read()
            if img_reader.error() != 0:
                self.ui.actionRotateRight.setDisabled(True)
                self.ui.actionRotateLeft.setDisabled(True)
                img_reader = QImageReader('images/broken_image.png')
                image = img_reader.read()
                return QPixmap.fromImage(image)
            else:
                return QPixmap.fromImage(image)
        except FileNotFoundError:
            return None

    def _runtime_decrypt(self, path):
        try:
            file_bytes = decrypt_runtime(path, self.cipher)
            ba = QByteArray(file_bytes)
            iod = QBuffer(ba)
            img_reader = QImageReader(iod)
            ext_ba = QByteArray(os.path.splitext(os.path.splitext(path)[0])[1].encode())
            img_reader.setFormat(ext_ba)
            img_reader.setAutoTransform(True)
            qimage = img_reader.read()
            if img_reader.error() != 0:
                img_reader = QImageReader('images/encrypted_with_another_key.png')
                return QPixmap.fromImage(img_reader.read())
            else:
                return QPixmap.fromImage(qimage)
        except EmptyCipher:
            img_reader = QImageReader('images/encrypted_placeholder.png')
            return QPixmap.fromImage(img_reader.read())
        except DecryptException:
            img_reader = QImageReader('images/encrypted_with_another_key.png')
            return QPixmap.fromImage(img_reader.read())
        except FileNotFoundError:
            return None

    def _update_image(self, lazily=False):
        if not lazily:
            if gettype(self.cur_path) == 'image':
                self.image = self._read_image(self.cur_path)
            elif gettype(self.cur_path) == 'aes':
                self.image = self._runtime_decrypt(self.cur_path)
            elif gettype(self.cur_path) == 'aes_zip':
                img_reader = QImageReader('images/encrypted_placeholder.png')
                self.image = QPixmap.fromImage(img_reader.read())
            elif gettype(self.cur_path) == 'video':
                img_reader = QImageReader('images/video_placeholder.png')
                self.image = QPixmap.fromImage(img_reader.read())
            else:
                self.image = None

        if self.image is not None:
            self.scene.clear()
            self.scene.addPixmap(self.image)
            self.scene.setSceneRect(0, 0, self.image.width(), self.image.height())
            if self.fit_in_view or (self.ui.graphicsView.sceneRect().width() > self.ui.graphicsView.rect().width() or
                                    self.ui.graphicsView.sceneRect().height() > self.ui.graphicsView.rect().height()):
                self.ui.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
            else:
                self.ui.graphicsView.resetTransform()
            self._update_fit_status()
        else:
            img_reader = QImageReader('images/nothing_to_show.png')
            image = QPixmap.fromImage(img_reader.read())
            self.scene.clear()
            self.scene.addPixmap(image)
            self.scene.setSceneRect(0, 0, image.width(), image.height())
            self.ui.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

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
        self._update_fit_status()

    def _select_item(self, cur, prev):
        # idx = self.ui.filesTree.selectionModel().currentIndex()
        # flag = self.ui.filesTree.selectionModel().SelectionFlag.Select
        # self.ui.filesTree.selectionModel().setCurrentIndex(idx, flag)
        self.cur_path = QFileSystemModel().filePath(cur)
        self.prev_path = QFileSystemModel().filePath(prev)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _open_folder(self):
        folder_dialog = QtWidgets.QFileDialog()
        self.root_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        if self.root_path == '':
            return
        self.ui.filesTree.change_root(self.root_path)
        with open('metadata.txt', 'w+', encoding="utf-8") as f:
            f.write(str(self.root_path))

        self.cur_path = None
        self.prev_path = None
        self.image = None
        self._update_image()

    def _open_last_folder(self):
        try:
            with open('metadata.txt', encoding="utf-8") as f:
                last_path = f.read()
            if os.path.exists(last_path):
                self.root_path = last_path
                self.ui.filesTree.change_root(self.root_path)
        except FileNotFoundError:
            logging.info("Last opened folder not found")
