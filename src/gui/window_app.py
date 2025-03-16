import ctypes
import os
import platform

from PyQt5 import QtCore
from PyQt5.QtCore import QBuffer, QByteArray, QItemSelectionModel, QSize
from PyQt5.QtGui import QImageReader, QPixmap
from PyQt5.QtWidgets import (QFileDialog, QFileSystemModel, QGraphicsScene,
                             QMainWindow)

from src.gui.icons import Icons, Placeholders
from src.gui.view_filestree import TitleBarWidget, gettype, is_rotatable
from src.gui.window_enterkey import EnterKeyDialog
from src.gui.window_folderencrypt import FolderEncryptDialog
from src.gui.window_graphicsview import FullScreen
from src.gui.window_progressbar import ProgressBarDialog
from src.gui.window_progressbar_onefile import ProgressBarOneFileDialog
from src.gui.window_settings import SettingsDialog
from src.gui.window_usermessage import UserMessage
from src.gui_generative.ui_mainwindow import Ui_MainWindow
from src.utils.aes import AESCipher, DecryptException
from src.utils.crypt_utils import (EmptyCipher, decrypt_file, decrypt_folder,
                                   decrypt_folder_file, decrypt_runtime,
                                   encrypt_file, encrypt_folder_each_file,
                                   encrypt_folder_to_one_file)
from src.utils.settings import DBJsonFile
from src.utils.utils import (copy_path, delete_path, rotate_file_left,
                             rotate_file_right)


def crypt_errors(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except EmptyCipher:
            UserMessage("No key!")
        except DecryptException:
            UserMessage("Decrypt error, file probably broken!")
        except FileNotFoundError:
            return None
        except FileExistsError as err:
            self.progressBarDialog.reset()
            self.progressBarDialog.done(200)
            UserMessage(f"{err.args[0]}\nFile already exist!\nOperation aborted.")

    return wrapper


class MainWindow(QMainWindow):
    def __init__(self, version):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"SecurePhotos v{version}")

        self.image = None
        self.cipher = None
        self.cur_path = None
        self.full_screen = False
        self.fit_in_view = True
        self.enterKeyDialog = EnterKeyDialog()
        self.folderEncryptDialog = FolderEncryptDialog()
        self.progressBarDialog = ProgressBarDialog()
        self.progressBarOneFileDialog = ProgressBarOneFileDialog()
        self.settingsDialog = SettingsDialog()
        self.db = DBJsonFile()

        # === Widget settings ===
        self.ui.dockFilesTree.setTitleBarWidget(TitleBarWidget())
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.fs = FullScreen()
        self.fs.setScene(self.scene)
        self.file_sys = QFileSystemModel()

        # === IMAGE RESOURCES ===
        self.icons = Icons()
        self.placeholders = Placeholders()

        # === APP ICON ===
        if platform.uname()[0] == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('annndruha.SecurePhotos')
        self.setWindowIcon(self.icons.favicon)

        # === TOOLBAR ICONS ===
        self.ui.actionOpenFolder.setIcon(self.icons.folder_open)
        self.ui.actionSettings.setIcon(self.icons.settings)
        self.ui.actionRotateLeft.setIcon(self.icons.rotate_left)
        self.ui.actionRotateRight.setIcon(self.icons.rotate_right)
        self.ui.actionDelete.setIcon(self.icons.delete)
        self.ui.actionChangeFit.setIcon(self.icons.zoom_none)
        self.ui.actionFullscreen.setIcon(self.icons.open_full)
        self.ui.actionEnterKey.setIcon(self.icons.key)
        self.ui.actionEncrypt.setIcon(self.icons.lock)
        self.ui.actionFolderDecrypt.setIcon(self.icons.folder_lock_open)
        self.ui.actionCopyToTarget.setIcon(self.icons.copy)
        self.ui.toolBar.setStyleSheet("QToolBar { border-style: none; }")

        # ===CONNECTS===
        self.ui.filesTree.selectionModel().currentChanged.connect(self._select_item)
        self.ui.filesTree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy(3))

        # toolBar buttons
        self.ui.actionOpenFolder.triggered.connect(self._open_folder)
        self.ui.actionSettings.triggered.connect(self._open_settings)
        self.ui.actionRotateLeft.triggered.connect(self._rotate_left)
        self.ui.actionRotateRight.triggered.connect(self._rotate_right)
        self.ui.actionDelete.triggered.connect(self._delete_file)
        self.ui.actionEnterKey.triggered.connect(self._open_enter_key)
        self.ui.actionEncrypt.triggered.connect(self._crypt)
        self.ui.actionFullscreen.triggered.connect(self._change_fullscreen)
        self.ui.actionChangeFit.triggered.connect(self._change_fit)
        self.ui.actionFolderDecrypt.triggered.connect(self._decrypt_folder)
        self.ui.actionCopyToTarget.triggered.connect(self._copy_to_target)

        # settingsDialog buttons
        self.settingsDialog.ui.pushButton_cancel.clicked.connect(self._reject_settings)
        self.settingsDialog.ui.pushButton_apply.clicked.connect(self._apply_settings)
        self.settingsDialog.rejected.connect(self._reject_settings)
        self._reject_settings()

        # enterKeyDialog buttons
        self.enterKeyDialog.ui.pushButton_cancel.clicked.connect(self._reject_enter_key)
        self.enterKeyDialog.ui.pushButton_apply.clicked.connect(self._apply_enter_key)
        self.enterKeyDialog.rejected.connect(self._reject_enter_key)

        # folderEncryptDialog buttons
        self.folderEncryptDialog.ui.pushButton_cancel.clicked.connect(self._reject_folder_encrypt)
        self.folderEncryptDialog.ui.pushButton_apply.clicked.connect(self._apply_folder_encrypt)
        self.folderEncryptDialog.rejected.connect(self._reject_folder_encrypt)

        # progressBarDialog buttons
        self.progressBarDialog.ui.pushButton_abort.clicked.connect(self._abort_folder_crypt)
        self.progressBarDialog.rejected.connect(self._abort_folder_crypt)

        # progressBarOneFileDialog buttons
        self.progressBarOneFileDialog.ui.pushButton_ok.clicked.connect(self._done_onefile)
        self.progressBarOneFileDialog.ui.pushButton_abort.clicked.connect(self._abort_onefile)
        self.progressBarOneFileDialog.rejected.connect(self._abort_onefile)

        self.fs.escapeSignal.connect(self._change_fullscreen)
        self.fs.nextSignal.connect(self._fullscreen_next)
        self.fs.prevSignal.connect(self._fullscreen_prev)

        self.ui.graphicsView.zoomedSignal.connect(self._update_action_fit_status)

        self.showMaximized()
        self.update_actions_status('sample.path')
        self._open_last_folder()

    # SLOTS: FullScreen
    def _change_fullscreen(self):
        self.full_screen = not self.full_screen
        if self.full_screen:
            self.fs.show()
            self.fs.showFullScreen()
            self.fs.update_image()
            self.ui.actionFullscreen.setIcon(self.icons.close_full)
            self.ui.actionFullscreen.setText('Window')
        else:
            self.fs.showNormal()
            self.fs.close()
            self.ui.actionFullscreen.setIcon(self.icons.open_full)
            self.ui.actionFullscreen.setText('Fullscreen')

    def _fullscreen_next(self):
        cur = self.ui.filesTree.selectionModel().currentIndex()
        self.ui.filesTree.selectionModel()
        idx = cur.siblingAtRow(cur.row() + 1)

        if idx.isValid() and gettype(self.file_sys.filePath(idx)) != 'folder':
            self.ui.filesTree.selectionModel().setCurrentIndex(idx, QItemSelectionModel.ToggleCurrent)
            self.fs.update_image()
        else:
            self._change_fullscreen()

    def _fullscreen_prev(self):
        cur = self.ui.filesTree.selectionModel().currentIndex()
        idx = cur.siblingAtRow(cur.row() - 1)
        if idx.isValid() and gettype(self.file_sys.filePath(idx)) != 'folder':
            self.ui.filesTree.selectionModel().setCurrentIndex(idx, QItemSelectionModel.ToggleCurrent)
            self.fs.update_image()
        else:
            self._change_fullscreen()

    # SLOTS: settingsDialog
    def _open_settings(self):
        self.settingsDialog.show()

    def _apply_settings(self):
        self.settingsDialog.apply(parent=self)
        self.settingsDialog.reset(parent=self)
        self.settingsDialog.done(200)

    def _reject_settings(self):
        self.settingsDialog.reset(parent=self)
        self.settingsDialog.done(200)

    # SLOTS: enterKeyDialog
    def _open_enter_key(self):
        if self.cipher is not None:
            UserMessage("Be careful! This action will delete previous saved password!", "Info")
        self.enterKeyDialog.show()
        self.enterKeyDialog.ui.pushButton_apply.setDisabled(True)

    def _apply_enter_key(self):
        if self.enterKeyDialog.ui.keyField.text() != '':
            self.cipher = AESCipher(self.enterKeyDialog.ui.keyField.text())
        self.enterKeyDialog.reset()
        self.enterKeyDialog.done(200)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _reject_enter_key(self):
        self.enterKeyDialog.reset()
        self.enterKeyDialog.done(200)

    # SLOTS: Encrypt and Decrypt one file or folder
    @crypt_errors
    def _crypt(self, _=None):
        """
        Encrypt or decrypt file or folder.
        If folder selected, open folderEncryptDialog
        """
        if self.ui.actionEncrypt.mode == 'folder':
            self.folderEncryptDialog.set_values(self.cur_path, self.cipher)
            self.folderEncryptDialog.check_size()
            self.folderEncryptDialog.show()
        elif self.ui.actionEncrypt.mode == 'encrypt':
            encrypt_file(self.cur_path, self.cipher, delete_original=True)
        elif self.ui.actionEncrypt.mode == 'decrypt':
            decrypt_file(self.cur_path, self.cipher, delete_original=True)
        self._update_image()

    @crypt_errors
    def _apply_folder_encrypt(self, _=None):
        """Open proper progress bar depending on chosen folder encrypt mode"""
        encrypt_type = self.folderEncryptDialog.get_select()
        path = self.folderEncryptDialog.cur_path
        cipher = self.folderEncryptDialog.cipher
        self.folderEncryptDialog.reset()
        self.folderEncryptDialog.done(200)

        if encrypt_type == 'files':
            self.progressBarDialog.show()
            encrypt_folder_each_file(path, cipher, self.progressBarDialog, delete_original=True)
        elif encrypt_type == 'one':
            self.progressBarOneFileDialog.show()
            encrypt_folder_to_one_file(path, cipher, self.progressBarOneFileDialog, delete_original=True)
        else:
            raise ValueError(f'Unknown encrypt type: {encrypt_type}')

        if self.progressBarOneFileDialog.was_canceled():
            self.progressBarOneFileDialog.reset()
            self.progressBarOneFileDialog.done(200)
        self.progressBarDialog.reset()
        self.progressBarDialog.done(200)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _reject_folder_encrypt(self):
        """Cancel or exit folderEncryptDialog (cancel mode select)"""
        self.folderEncryptDialog.reset()
        self.folderEncryptDialog.done(200)

    @crypt_errors
    def _decrypt_folder(self, _=None):
        """Decrypt one-file-folder or all aes-files in unencrypted folder"""
        if gettype(self.cur_path) == 'aes_zip':
            decrypt_folder_file(self.cur_path, self.cipher, delete_original=True)
        else:
            self.progressBarDialog.show()
            decrypt_folder(self.cur_path, self.cipher, self.progressBarDialog, delete_original=True)
        self.progressBarDialog.reset()
        self.progressBarDialog.done(200)

    def _abort_folder_crypt(self):
        """Emit internal progressBarDialog signal for stop file encrypt loop"""
        self.progressBarDialog.cancel()

    def _done_onefile(self):
        """Close progressBarOneFileDialog after finish"""
        self.progressBarOneFileDialog.done(200)
        self.progressBarOneFileDialog.reset()

    def _abort_onefile(self):
        """Emit internal progressBarOneFileDialog signal for cancel crypt"""
        self.progressBarOneFileDialog.cancel()

    # SLOTS: Fit image
    def _change_fit(self):
        """Change fit (resize) mode"""
        self.fit_in_view = not self.fit_in_view
        self._update_image(lazily=False)
        self.ui.graphicsView.reset_zoomed()
        self._update_action_fit_status()

    # SLOTS: toolBar behaviour (buttons availability)
    def _update_action_fit_status(self):
        """Update fit button"""
        width_not_fitted = self.ui.graphicsView.sceneRect().width() > self.ui.graphicsView.rect().width()
        height_not_fitted = self.ui.graphicsView.sceneRect().height() > self.ui.graphicsView.rect().height()
        nothing_to_fit = width_not_fitted or height_not_fitted

        if self.ui.graphicsView.zoomed():
            nothing_to_fit = False
        if gettype(self.cur_path) not in ['image', 'aes']:
            nothing_to_fit = True
        if self.fit_in_view and not nothing_to_fit:
            self.ui.actionChangeFit.setEnabled(True)
            self.ui.actionChangeFit.setText('Fit view')
            self.ui.actionChangeFit.setIcon(self.icons.zoom_in)
        elif not self.fit_in_view and not nothing_to_fit:
            self.ui.actionChangeFit.setEnabled(True)
            self.ui.actionChangeFit.setText('Fit view')
            self.ui.actionChangeFit.setIcon(self.icons.zoom_out)
        else:
            self.ui.actionChangeFit.setText("Fit view")
            self.ui.actionChangeFit.setIcon(self.icons.zoom_none)
            self.ui.actionChangeFit.setDisabled(True)

    def _update_actions_visible(self):
        """Update actions buttons visibility by settings"""
        self.ui.actionRotateLeft.setVisible(self.db['action_rotate_left'])
        self.ui.actionRotateRight.setVisible(self.db['action_rotate_right'])
        self.ui.actionDelete.setVisible(self.db['action_delete'])
        self.ui.actionChangeFit.setVisible(self.db['action_fit_view'])
        self.ui.actionFullscreen.setVisible(self.db['action_fullscreen'])
        self.ui.actionFolderDecrypt.setVisible(self.db['action_encrypt_decrypt'])
        self.ui.actionEncrypt.setVisible(self.db['action_encrypt_decrypt'])
        self.ui.actionEnterKey.setVisible(self.db['action_encrypt_decrypt'])
        self.ui.actionCopyToTarget.setVisible(self.db['copy_to_target'])

    def _update_actions_crypt(self, path):
        """
        Update visible status for crypt actions,
         according to selected file and cipher status
        """
        if self.db['action_encrypt_decrypt']:
            self.ui.actionFolderDecrypt.setVisible(False)
            self.ui.actionEncrypt.setVisible(True)

        if self.cipher is None:
            self.ui.actionEncrypt.setText('Need key')
            self.ui.actionEncrypt.setDisabled(True)
            self.ui.actionEncrypt.setIcon(self.icons.not_locked)
            self.ui.actionEncrypt.mode = 'disable'
            return

        if gettype(path) is None:
            self.ui.actionEncrypt.setText('Select file first')
            self.ui.actionEncrypt.setDisabled(True)
            self.ui.actionEncrypt.setIcon(self.icons.not_locked)
            self.ui.actionEncrypt.mode = 'disable'
        elif gettype(path) == 'folder':
            self.ui.actionEncrypt.setText('Encrypt folder')
            self.ui.actionEncrypt.setEnabled(True)
            self.ui.actionEncrypt.setIcon(self.icons.folder_lock)
            self.ui.actionEncrypt.mode = 'folder'
            if self.db['action_encrypt_decrypt']:
                self.ui.actionFolderDecrypt.setVisible(True)
        elif gettype(path) == 'aes_zip':
            if self.db['action_encrypt_decrypt']:
                self.ui.actionEncrypt.setVisible(False)
                self.ui.actionFolderDecrypt.setVisible(True)
        elif gettype(path) == 'aes':
            self.ui.actionEncrypt.setText('Decrypt on disk')
            self.ui.actionEncrypt.setEnabled(True)
            self.ui.actionEncrypt.setIcon(self.icons.lock_open)
            self.ui.actionEncrypt.mode = 'decrypt'
        else:
            self.ui.actionEncrypt.setText('Encrypt on disk')
            self.ui.actionEncrypt.setEnabled(True)
            self.ui.actionEncrypt.setIcon(self.icons.lock)
            self.ui.actionEncrypt.mode = 'encrypt'

    def update_actions_status(self, path: str):
        """Update all toolBar actions statuses"""
        self.ui.actionRotateLeft.setEnabled(is_rotatable(path))
        self.ui.actionRotateRight.setEnabled(is_rotatable(path))
        self.ui.actionFullscreen.setEnabled(gettype(path) == 'image')
        self.ui.actionDelete.setEnabled(gettype(path) is not None and path != 'sample.path')
        # Update complex status logic
        self._update_action_fit_status()
        self._update_actions_visible()
        self._update_actions_crypt(path)

    # IMAGES: Image actions and changes
    def _read_image(self, path):
        """Return QPixmap of image"""
        try:
            img_reader = QImageReader(path)
            if img_reader.format() == 'svg':
                # TODO: Fix cut svg images. Maybe not here
                sz = img_reader.size()
                hw_ratio = sz.height() / sz.width()
                widget_width = self.ui.graphicsView.frameSize().width()
                img_reader.setScaledSize(QSize(widget_width, int(widget_width * hw_ratio)))
            img_reader.setAutoTransform(True)
            image = img_reader.read()
            if img_reader.error() != 0:
                self.ui.actionRotateRight.setDisabled(True)
                self.ui.actionRotateLeft.setDisabled(True)
                return self.placeholders.broken_image
            else:
                return QPixmap.fromImage(image)
        except FileNotFoundError:
            return None

    def _runtime_decrypt(self, path):
        """Return QPixmap of runtime decrypted image"""
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
                return self.placeholders.try_another_key
            else:
                return QPixmap.fromImage(qimage)
        except EmptyCipher:
            return self.placeholders.encrypted
        except DecryptException:
            return self.placeholders.try_another_key
        except FileNotFoundError:
            return None

    def _update_image(self, lazily=False):
        """Update showing image"""
        if not lazily:
            if gettype(self.cur_path) == 'image':
                self.image = self._read_image(self.cur_path)
            elif gettype(self.cur_path) == 'aes':
                self.image = self._runtime_decrypt(self.cur_path)
            elif gettype(self.cur_path) == 'aes_zip':
                self.image = self.placeholders.encrypted
            elif gettype(self.cur_path) == 'video':
                self.image = self.placeholders.video
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
            self._update_action_fit_status()
        else:
            image = self.placeholders.nothing_to_show
            self.scene.clear()
            self.scene.addPixmap(image)
            self.scene.setSceneRect(0, 0, image.width(), image.height())
            self.ui.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self._update_image(lazily=True)
        self._update_action_fit_status()

    # ACTIONS: Actions from toolBar
    def _rotate_left(self):
        rotate_file_left(self.cur_path)
        self._update_image()

    def _rotate_right(self):
        rotate_file_right(self.cur_path)
        self._update_image()

    def _delete_file(self):
        delete_path(self.cur_path)
        self._update_image()

    def _select_item(self, cur, prev):
        self.cur_path = self.file_sys.filePath(cur)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _open_folder(self):
        folder_dialog = QFileDialog()
        self.root_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        if not self.root_path:
            return
        self.db['last_path'] = str(self.root_path)
        self.ui.filesTree.change_root(self.root_path)
        self.cur_path = None
        self.image = None
        self._update_image()

    def _open_last_folder(self):
        last_path = self.db['last_path']
        if last_path and os.path.exists(last_path) and os.path.isdir(last_path):
            self.root_path = last_path
            self.ui.filesTree.change_root(self.root_path)
        else:
            self._open_folder()

    def _copy_to_target(self):
        if not self.cur_path and self.cur_path != 'sample.path':
            UserMessage("Select file first", "Info")
            return
        if not self.db['copy_to_target']:
            UserMessage("Copy to target disabled!", "Info")
            return
        if not self.db['copy_to_target_path']:
            UserMessage("Target path is empty!\nSelect target path in settings", "Error")
            return
        if not os.path.exists(self.db['copy_to_target_path']):
            UserMessage("Target path doesn't exist!\nCreate it ot select another target path in settings", "Error")
            return
        try:
            copy_path(self.cur_path, self.db['copy_to_target_path'])
        except Exception as e:
            UserMessage(str(e), "Error")
