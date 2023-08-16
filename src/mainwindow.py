import os
import ctypes
import platform

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QByteArray, QBuffer, QSize, QItemSelectionModel
from PyQt5.QtGui import QIcon, QPixmap, QImageReader, QPalette, QColor
from PyQt5.QtWidgets import QFileSystemModel, QGraphicsScene, QLineEdit

from gui.ui_mainwindow import Ui_MainWindow
from gui.ui_enterkey import Ui_EnterKey
from src.aes import AESCipher, encrypt_file, decrypt_file, decrypt_runtime, EmptyCipher, DecryptException
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
        self.fit_in_view = True
        self.enterKeyDialog = EnterKeyDialog()

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

        # Not done
        self.ui.actionTreeView.setDisabled(True)

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

        self.enterKeyDialog.ui.pushButton_cancel.clicked.connect(self._reject_enter_key)
        self.enterKeyDialog.ui.pushButton_apply.clicked.connect(self._apply_enter_key)
        self.enterKeyDialog.rejected.connect(self._reject_enter_key)

        self.fs.escapeSignal.connect(self._change_fullscreen)
        self.fs.nextSignal.connect(self._next)
        self.fs.prevSignal.connect(self._prev)

        self.update_actions_status('sample.path')
        self.showMaximized()
        self._open_last_folder()

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

    def _next(self):
        cur = self.ui.filesTree.selectionModel().currentIndex()
        self.ui.filesTree.selectionModel()
        idx = cur.siblingAtRow(cur.row() + 1)

        if idx.isValid() and gettype(QFileSystemModel().filePath(idx)) != 'folder':
            self.ui.filesTree.selectionModel().setCurrentIndex(idx, QItemSelectionModel.ToggleCurrent)
            self.fs.update_image()
        else:
            self._change_fullscreen()

    def _prev(self):
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
        # TODO: Is all image type can rotate?
        if gettype(path) == 'image' and is_rotatable(path):
            self.ui.actionRotateLeft.setEnabled(True)
            self.ui.actionRotateRight.setEnabled(True)
        else:
            self.ui.actionRotateLeft.setDisabled(True)
            self.ui.actionRotateRight.setDisabled(True)

        if gettype(path) == 'image':
            self.ui.actionFullscreen.setEnabled(True)
        else:
            self.ui.actionFullscreen.setDisabled(True)

        self._update_fit_status()

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
        except FileNotFoundError as err:
            print("Last opened folder not found")


class EnterKeyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(EnterKeyDialog, self).__init__()
        self.ui = Ui_EnterKey()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/icon.ico'))
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


class UserMessage(QtWidgets.QMessageBox):
    def __init__(self, text, level="Critical"):
        super(UserMessage, self).__init__()
        if level == "Critical":
            self.setIcon(QtWidgets.QMessageBox.Critical)
            self.setWindowTitle("Critical error")
        elif level == "Warning":
            self.setIcon(QtWidgets.QMessageBox.Warning)
            self.setWindowTitle("Warning")
        else:
            self.setIcon(QtWidgets.QMessageBox.Information)
            self.setWindowTitle("Info")
        self.setText(text)
        self.exec()


class FullScreen(QtWidgets.QGraphicsView):
    escapeSignal = QtCore.pyqtSignal()
    nextSignal = QtCore.pyqtSignal()
    prevSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(FullScreen, self).__init__()

    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.escapeSignal.emit()
        elif event.key() == 16777236:
            self.nextSignal.emit()
        elif event.key() == 16777234:
            self.prevSignal.emit()

    def update_image(self):
        self.resize(QSize(1920, 1080))  # TODO: Get screen size
        self.fitInView(self.scene().itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
