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

        # === TOOLBAR ICONS ===
        self.ui.actionOpenFolder.setIcon(QIcon('images/icons/folder_open.svg'))
        self.ui.actionTreeView.setIcon(QIcon('images/icons/tree.svg'))
        self.ui.actionRotateLeft.setIcon(QIcon('images/icons/rotate_left.svg'))
        self.ui.actionRotateRight.setIcon(QIcon('images/icons/rotate_right.svg'))
        self.ui.actionFullscreen.setIcon(QIcon('images/icons/open_full.svg'))
        self.ui.actionEnter_Key.setIcon(QIcon('images/icons/key.svg'))
        self.ui.actionEncrypt.setIcon(QIcon('images/icons/lock.svg'))

        # ===CONNECTS===
        self.ui.actionOpenFolder.triggered.connect(self._open_folder)
        self.ui.treeWidget.itemSelectionChanged.connect(self._select_item)

    # ===SLOTS===
    # ===Main Window Slot
    # Start button
    def _select_item(self):
        print(self.ui.treeWidget.currentItem().full_path)

        self.ui.label.setPixmap(QPixmap(self.ui.treeWidget.currentItem().full_path))
        # print(read_file(self.ui.treeWidget.currentItem().full_path))

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
