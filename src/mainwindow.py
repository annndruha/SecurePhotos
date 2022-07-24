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

        # Set icons from generated temp file while launch
        if hasattr(sys, "_MEIPASS"):
            icondir = os.path.join(sys._MEIPASS, 'images/icon.ico')
            folderdir = os.path.join(sys._MEIPASS, 'images/folder.ico')
        else:
            icondir = 'images/icon.ico'
            folderdir = 'images/folder.ico'

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icondir), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(folderdir), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_path.setIcon(icon1)

        self.ui.lineEdit_filepath.setText(str(os.getcwd()))

        # ===SIGNALS===
        # self.ui.pushButton_start.clicked.connect(self._start)
        self.ui.pushButton_path.clicked.connect(self._select_path)
        # self.ui.checkBox_user_replace.stateChanged.connect(self._update_rename_state)
        # self.name.finished.connect(self._name_handler)

    # ===SLOTS===
    # ===Main Window Slot
    # Start button
    def _start(self):
        try:
            path = self.ui.lineEdit_filepath.text()
            if self.ui.check_include_subfolder.isChecked():
                for top, dirs, files in os.walk(path):
                    for nm in files:
                        self.file_paths.append(os.path.join(top, nm))
            else:
                files_names = os.listdir(path)
                for name in files_names:
                    self.file_paths.append(os.path.join(path, name))

            self.file_paths = list(filter(lambda x: x.endswith('.mp3'), self.file_paths))
        except:
            self.log("ERROR: Incorrect folder path")
            self.ui.lineEdit_filepath.setText("ERROR: Incorrect folder path")

    def _get_pathces(self, path, subfolders=False):
        file_paths = []
        if subfolders:
            for top, dirs, files in os.walk(path):
                for nm in files:
                    file_paths.append(os.path.join(top, nm))
        else:
            files_names = os.listdir(path)
            for name in files_names:
                file_paths.append(os.path.join(path, name))
        return file_paths

    # Select path button
    def _select_path(self):
        folder_dialog = QtWidgets.QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        self.ui.lineEdit_filepath.setText(folder_path)

        file_paths = []
        subfolder = self.ui.check_include_subfolder.isChecked()
        file_paths = self._get_pathces(folder_path, subfolder)
        parent_itm = self.ui.treeWidget

        def load_project_structure(startpath, tree):
            for element in os.listdir(startpath):
                path_info = startpath + "/" + element
                print(os.path.basename(element))
                parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
                if os.path.isdir(path_info):
                    load_project_structure(path_info, parent_itm)

        load_project_structure(folder_path, self.ui.treeWidget)
        # self.ui.treeWidget.insertTopLevelItems(0, items)

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
