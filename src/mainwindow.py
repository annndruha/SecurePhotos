import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from gui.ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QTreeWidgetItem


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('images/icon.png'))

        # ===CONNECTS===
        self.ui.actionOpenFolder.triggered.connect(self._select_path)

    # ===SLOTS===
    # ===Main Window Slot
    # Start button
    def _start(self):
        pass
        # try:
        #     path = self.ui.lineEdit_filepath.text()
        #     if self.ui.check_include_subfolder.isChecked():
        #         for top, dirs, files in os.walk(path):
        #             for nm in files:
        #                 self.file_paths.append(os.path.join(top, nm))
        #     else:
        #         files_names = os.listdir(path)
        #         for name in files_names:
        #             self.file_paths.append(os.path.join(path, name))
        #
        #     self.file_paths = list(filter(lambda x: x.endswith('.mp3'), self.file_paths))
        # except:
        #     self.log("ERROR: Incorrect folder path")
        #     self.ui.lineEdit_filepath.setText("ERROR: Incorrect folder path")

    # Select path button
    def _select_path(self):
        folder_dialog = QtWidgets.QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        if folder_path is '':
            return
        # self.ui.lineEdit_filepath.setText(folder_path)
        self.ui.treeWidget.clear()
        def load_project_structure(path, tree):
            dirlist = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
            filelist = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))]
            for element in dirlist + filelist:
                path_info = os.path.join(path, element)
                parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
                if os.path.isdir(path_info):
                    load_project_structure(path_info, parent_itm)
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
