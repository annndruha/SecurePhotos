import os
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QTreeWidgetItem

from gui.ui_mainwindow import Ui_MainWindow
from src.aes import read_file


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('images/icon.png'))

        self.image = None
        # === TOOLBAR ICONS ===
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
        self.ui.actionFullscreen.setDisabled(True)
        self.ui.actionEnterKey.setDisabled(True)
        self.ui.actionEncrypt.setDisabled(True)

        # ===CONNECTS===
        self.ui.actionOpenFolder.triggered.connect(self._open_folder)
        self.ui.treeWidget.itemSelectionChanged.connect(self._select_item)

        # self.ui.label.resizeEvent.triggered.connect(self._resize_view)
        # .connect(self._resize_view)

    # ===SLOTS===
    # ===Main Window Slot
    # Start button
    def resizeEvent(self, event):
        self._resize_image()

    def _resize_image(self):  # Work only while mainwindows resize
        if self.image is not None:
            w = self.ui.label.width()
            h = self.ui.label.height()
            self.ui.label.setPixmap(self.image.scaled(w, h, QtCore.Qt.KeepAspectRatio))

    def _select_item(self):
        path = self.ui.treeWidget.currentItem().full_path
        print()

        if os.path.isdir(path):
            self.image = None
            self.ui.label.setText("Can't show, folder selected.")
        else:
            ext = os.path.splitext(path)[1].replace('.','')
            supported_ext = QtGui.QImageReader.supportedImageFormats()
            if ext in [str(ext, 'utf-8') for ext in supported_ext]:
                self.image = QPixmap(path)
                w = self.ui.label.width()
                h = self.ui.label.height()
                self.ui.label.setPixmap(self.image.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            else:
                text = 'Can not show. Supported image formats: \n' + \
                       ', '.join([str(ext, 'utf-8') for ext in supported_ext]) + \
                       '\n\bYou still can encrypt ot decrypt file!'
                self.ui.label.setText(text)

    # Select path button
    def _open_folder(self):
        folder_dialog = QtWidgets.QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        if folder_path is '':
            return
        self.ui.treeWidget.clear()

        def load_project_structure(path, tree):
            dirlist = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
            filelist = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))]
            for element in dirlist + filelist:
                parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
                parent_itm.full_path = os.path.join(path, element)
                if os.path.isdir(parent_itm.full_path):
                    load_project_structure(parent_itm.full_path, parent_itm)
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/folder.svg'))
                else:
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/file.svg'))

        load_project_structure(folder_path, self.ui.treeWidget)

# class NameDialog(QtWidgets.QDialog):
#     def __init__(self):
#         super(NameDialog, self).__init__()
#         self.ui = Ui_NameDialog()
#         self.ui.setupUi(self)
#
#         if hasattr(sys, "_MEIPASS"):
#             icondir = os.path.join(sys._MEIPASS, 'img/icon.ico')
#         else:
#             icondir = 'img/icon.ico'
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(icondir), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.setWindowIcon(icon)
#
#         self.clear()
#
#     def clear(self):
#         self.ui.lineEdit_cur_name.clear()
#         self.ui.lineEdit_new_name.clear()
#
#
# class TagsDialog(QtWidgets.QDialog):
#     def __init__(self):
#         super(TagsDialog, self).__init__()
#         self.ui = Ui_TagEditor()
#         self.ui.setupUi(self)
#
#         if hasattr(sys, "_MEIPASS"):
#             icondir = os.path.join(sys._MEIPASS, 'img/icon.ico')
#         else:
#             icondir = 'img/icon.ico'
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(icondir), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.setWindowIcon(icon)
#
#         self.clear()
#
#     def clear(self):
#         self.ui.track_num_0.clear()
