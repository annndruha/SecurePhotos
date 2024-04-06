import os
import ctypes
import platform

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QBuffer, QItemSelectionModel, QSize
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtWidgets import (QMainWindow,
                             QFileSystemModel,
                             QGraphicsScene,
                             QFileDialog)

from src.gui_generative.ui_mainwindow import Ui_MainWindow

from src.gui.view_filestree import gettype, is_rotatable, TitleBarWidget
from src.gui.window_usermessage import UserMessage
from src.gui.window_enterkey import EnterKeyDialog
from src.gui.window_folderencrypt import FolderEncrypt
from src.gui.window_progressbar import ProgressBarDialog
from src.gui.window_progressbar_onefile import ProgressBarOneFileDialog
from src.gui.window_graphicsview import FullScreen, ZoomQGraphicsView

from src.utils.aes import AESCipher, DecryptException
from src.utils.crypt_utils import (encrypt_file,
                                   decrypt_file,
                                   encrypt_folder_each_file,
                                   encrypt_folder_to_one_file,
                                   decrypt_folder,
                                   decrypt_folder_file,
                                   decrypt_runtime,
                                   EmptyCipher)
from src.utils.utils import (rotate_file_right,
                             rotate_file_left,
                             delete_path,
                             config_get_last_path,
                             config_set_last_path)
from src.gui.icons import SPIcon, SPPlaceholder


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
        self.folderEncrypt = FolderEncrypt()
        self.progressBarDialog = ProgressBarDialog()
        self.progressBarOneFileDialog = ProgressBarOneFileDialog()

        # === Widget settings ===
        self.scene = QGraphicsScene()
        self.ui.graphicsView = ZoomQGraphicsView(self.ui.widget)
        self.ui.graphicsView.setObjectName("graphicsView")
        self.ui.horizontalLayout.setContentsMargins(5, 15, 5, 5)
        self.ui.horizontalLayout.addWidget(self.ui.graphicsView)

        self.ui.dockFilesTree.setContentsMargins(5, 0, 5, 5)
        self.ui.dockFilesTree.setTitleBarWidget(TitleBarWidget())

        self.ui.graphicsView.setScene(self.scene)
        self.fs = FullScreen()
        self.fs.setScene(self.scene)

        # === IMAGE RESOURCES ===
        self.sp_icon = SPIcon()
        self.sp_placeholder = SPPlaceholder()

        # === APP ICON ===
        if platform.uname()[0] == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('annndruha.SecurePhotos')
        self.setWindowIcon(self.sp_icon.favicon)

        # === TOOLBAR ICONS ===
        self.ui.actionOpenFolder.setIcon(self.sp_icon.folder_open)
        self.ui.actionRotateLeft.setIcon(self.sp_icon.rotate_left)
        self.ui.actionRotateRight.setIcon(self.sp_icon.rotate_right)
        self.ui.actionDelete.setIcon(self.sp_icon.delete)
        self.ui.actionChangeFit.setIcon(self.sp_icon.zoom_none)
        self.ui.actionFullscreen.setIcon(self.sp_icon.open_full)
        self.ui.actionEnterKey.setIcon(self.sp_icon.key)
        self.ui.actionEncrypt.setIcon(self.sp_icon.lock)
        self.ui.actionFoldeDecrypt.setIcon(self.sp_icon.folder_lock_open)
        self.ui.toolBar.setStyleSheet("QToolBar { border-style: none; }")

        # ===CONNECTS===
        self.ui.filesTree.selectionModel().currentChanged.connect(self._select_item)
        self.ui.filesTree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy(3))

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
        self.progressBarOneFileDialog.ui.pushButton_ok.clicked.connect(self._done_onefile)
        self.progressBarOneFileDialog.ui.pushButton_abort.clicked.connect(self._abort_onefile)

        self.fs.escapeSignal.connect(self._change_fullscreen)
        self.fs.nextSignal.connect(self._fullscreen_next)
        self.fs.prevSignal.connect(self._fullscreen_prev)

        self.ui.graphicsView.zoomedSignal.connect(self._update_fit_status)

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
            self.ui.actionFullscreen.setIcon(self.sp_icon.close_full)
            self.ui.actionFullscreen.setText('Window')
        else:
            self.fs.showNormal()
            self.fs.close()
            self.ui.actionFullscreen.setIcon(self.sp_icon.open_full)
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
        self.folderEncrypt.reset()
        self.folderEncrypt.done(200)

    @crypt_errors
    def _apply_folder_encrypt(self, _=None):
        encrypt_type = self.folderEncrypt.get_select()
        path = self.folderEncrypt.cur_path
        cipher = self.folderEncrypt.cipher

        self.folderEncrypt.reset()
        self.folderEncrypt.done(200)
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

    @crypt_errors
    def _decrypt_folder(self, _=None):
        if gettype(self.cur_path) == 'aes_zip':
            decrypt_folder_file(self.cur_path, self.cipher, delete_original=True)
        else:
            self.progressBarDialog.show()
            decrypt_folder(self.cur_path, self.cipher, self.progressBarDialog, delete_original=True)
        self.progressBarDialog.reset()
        self.progressBarDialog.done(200)

    def _done_onefile(self):
        self.progressBarOneFileDialog.done(200)
        self.progressBarOneFileDialog.reset()

    def _abort_onefile(self):
        self.progressBarOneFileDialog.cancel()

    def _abort_folder_crypt(self):
        self.progressBarDialog.cancel()

    def _change_fit(self):
        self.fit_in_view = not self.fit_in_view
        self._update_image(lazily=False)
        self.ui.graphicsView.reset_zoomed()
        self._update_fit_status()

    def _update_fit_status(self):
        nothing_to_fit = self.ui.graphicsView.sceneRect().width() > self.ui.graphicsView.rect().width() or \
                         self.ui.graphicsView.sceneRect().height() > self.ui.graphicsView.rect().height()
        if self.ui.graphicsView.zoomed():
            nothing_to_fit = False
        if gettype(self.cur_path) not in ['image', 'aes']:
            nothing_to_fit = True
        if self.fit_in_view and not nothing_to_fit:
            self.ui.actionChangeFit.setEnabled(True)
            self.ui.actionChangeFit.setText('Fit view')
            self.ui.actionChangeFit.setIcon(self.sp_icon.zoom_in)
        elif not self.fit_in_view and not nothing_to_fit:
            self.ui.actionChangeFit.setEnabled(True)
            self.ui.actionChangeFit.setText('Fit view')
            self.ui.actionChangeFit.setIcon(self.sp_icon.zoom_out)
        else:
            self.ui.actionChangeFit.setText("Fit view")
            self.ui.actionChangeFit.setIcon(self.sp_icon.zoom_none)
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
            self.ui.actionEncrypt.setIcon(self.sp_icon.not_locked)
            self.ui.actionEncrypt.mode = 'disable'
            return

        if gettype(path) is None:
            self.ui.actionEncrypt.setText('Select file first')
            self.ui.actionEncrypt.setDisabled(True)
            self.ui.actionEncrypt.setIcon(self.sp_icon.not_locked)
            self.ui.actionEncrypt.mode = 'disable'
        elif gettype(path) == 'folder':
            self.ui.actionEncrypt.setText('Encrypt folder')
            self.ui.actionEncrypt.setEnabled(True)
            self.ui.actionEncrypt.setIcon(self.sp_icon.folder_lock)
            self.ui.actionEncrypt.mode = 'folder'
            self.ui.actionFoldeDecrypt.setVisible(True)
        elif gettype(path) == 'aes_zip':
            self.ui.actionEncrypt.setVisible(False)
            self.ui.actionFoldeDecrypt.setVisible(True)
        elif gettype(path) == 'aes':
            self.ui.actionEncrypt.setText('Decrypt on disk')
            self.ui.actionEncrypt.setEnabled(True)
            self.ui.actionEncrypt.setIcon(self.sp_icon.lock_open)
            self.ui.actionEncrypt.mode = 'decrypt'
        else:
            self.ui.actionEncrypt.setText('Encrypt on disk')
            self.ui.actionEncrypt.setEnabled(True)
            self.ui.actionEncrypt.setIcon(self.sp_icon.lock)
            self.ui.actionEncrypt.mode = 'encrypt'

    @crypt_errors
    def _crypt(self, _=None):
        if self.ui.actionEncrypt.mode == 'folder':
            self.folderEncrypt.set_values(self.cur_path, self.cipher)
            self.folderEncrypt.check_size()
            self.folderEncrypt.show()
        elif self.ui.actionEncrypt.mode == 'encrypt':
            encrypt_file(self.cur_path, self.cipher, delete_original=True)
        elif self.ui.actionEncrypt.mode == 'decrypt':
            decrypt_file(self.cur_path, self.cipher, delete_original=True)
        self._update_image()

    def _read_image(self, path):
        try:
            img_reader = QImageReader(path)
            if img_reader.format() == 'svg':
                # TODO: Fix cut svg images. May by not here
                sz = img_reader.size()
                hw_ratio = sz.height() / sz.width()
                widget_width = self.ui.graphicsView.frameSize().width()
                img_reader.setScaledSize(QSize(widget_width, int(widget_width * hw_ratio)))
            img_reader.setAutoTransform(True)
            image = img_reader.read()
            if img_reader.error() != 0:
                self.ui.actionRotateRight.setDisabled(True)
                self.ui.actionRotateLeft.setDisabled(True)
                return self.sp_placeholder.broken_image
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
                return self.sp_placeholder.try_another_key
            else:
                return QPixmap.fromImage(qimage)
        except EmptyCipher:
            return self.sp_placeholder.encrypted
        except DecryptException:
            return self.sp_placeholder.try_another_key
        except FileNotFoundError:
            return None

    def _update_image(self, lazily=False):
        if not lazily:
            if gettype(self.cur_path) == 'image':
                self.image = self._read_image(self.cur_path)
            elif gettype(self.cur_path) == 'aes':
                self.image = self._runtime_decrypt(self.cur_path)
            elif gettype(self.cur_path) == 'aes_zip':
                self.image = self.sp_placeholder.encrypted
            elif gettype(self.cur_path) == 'video':
                self.image = self.sp_placeholder.video
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
            image = self.sp_placeholder.nothing_to_show
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
        self.cur_path = QFileSystemModel().filePath(cur)
        self.prev_path = QFileSystemModel().filePath(prev)
        self.update_actions_status(self.cur_path)
        self._update_image()

    def _open_folder(self):
        folder_dialog = QFileDialog()
        self.root_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        if self.root_path == '':
            return
        config_set_last_path(str(self.root_path))

        self.ui.filesTree.change_root(self.root_path)
        self.cur_path = None
        self.prev_path = None
        self.image = None
        self._update_image()

    def _open_last_folder(self):
        last_path = config_get_last_path()
        if last_path is not None:
            self.root_path = last_path
            self.ui.filesTree.change_root(self.root_path)
