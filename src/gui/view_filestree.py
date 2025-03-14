import os
import shutil
import webbrowser

from PyQt5.QtCore import QFileInfo, Qt, QEvent
from PyQt5.QtWidgets import (QWidget,
                             QTreeView,
                             QFileSystemModel,
                             QApplication,
                             QFileIconProvider, QVBoxLayout, QSizePolicy, QMenu)

from src.gui.icons import SPIcon

SUPPORTED_EXT = {'image': ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'ppm', 'xbm', 'xpm', 'svg'],
                 'aes': ['aes'],
                 'text': ['txt', 'md', 'doc', 'docx', 'pdf', 'rtf', 'odt'],
                 'audio': ['aac', 'wav', 'mp3', 'ac3', 'ogg', 'wma'],
                 'video': ['mkv', 'mp4', 'avi', 'mov', 'webm'],
                 'zip': ['rar', 'zip'],
                 'aes_zip': ['aes_zip']}


def is_rotatable(fullpath):
    try:
        ext = os.path.splitext(os.path.basename(fullpath))[1].replace('.', '').lower()
    except Exception:
        return False
    if ext in ['bmp', 'jpg', 'jpeg', 'png']:
        return True
    return False


def gettype(fullpath):
    if fullpath is None:
        return None
    if os.path.isdir(fullpath):
        return 'folder'
    ext = os.path.splitext(os.path.basename(fullpath))[1].replace('.', '').lower()
    for key in SUPPORTED_EXT.keys():
        if ext in SUPPORTED_EXT[key]:
            return key
    return 'file'


class IconProvider(QFileIconProvider):
    def icon(self, parameter):
        if isinstance(parameter, QFileInfo):
            if parameter.isDir():
                return self.sp_icon.folder
            if gettype(parameter.absoluteFilePath()) == 'aes':
                return self.sp_icon.lock
            if gettype(parameter.absoluteFilePath()) == 'aes_zip':
                return self.sp_icon.folder_lock
            if gettype(parameter.absoluteFilePath()) == 'image':
                return self.sp_icon.image
            if gettype(parameter.absoluteFilePath()) == 'video':
                return self.sp_icon.movie
            if gettype(parameter.absoluteFilePath()) == 'zip':
                return self.sp_icon.file_zip
        return super().icon(parameter)


class ProxyQFileSystemModel(QFileSystemModel):
    def __init__(self):
        super().__init__()
        self.column_name = 'Name'

    def headerData(self, section, orientation, role):
        if section == 0 and role == Qt.DisplayRole:
            return self.column_name
        else:
            return super(QFileSystemModel, self).headerData(section, orientation, role)

    def set_header_name(self, name):
        self.column_name = name


class TitleBarWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 15, 5, 0)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_Hover)

    def event(self, event):
        if event.type() == QEvent.HoverEnter:
            self.setCursor(Qt.SizeAllCursor)
        elif event.type() == QEvent.HoverLeave:
            self.setCursor(Qt.ArrowCursor)
        return super().event(event)


class FilesTree(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_model = ProxyQFileSystemModel()
        self.sp_icon = SPIcon()
        icon_provide = IconProvider()
        icon_provide.sp_icon = self.sp_icon
        self.file_model.setIconProvider(icon_provide)
        self.setModel(self.file_model)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.customContextMenuRequested.connect(self._open_files_tree_context)

    #     self.file_model.directoryLoaded.connect(self.on_directory_loaded)
    #
    # def on_directory_loaded(self, rootpath):
    #     idx = self.file_model.index(rootpath)
    #     self.selectionModel().clearSelection()
    #     if self.file_model.rowCount(idx) > 0:
    #         index = self.file_model.index(0, 0, idx)
    #         self.selectionModel().setCurrentIndex(index, self.selectionModel().SelectionFlag.Select)

    def change_root(self, rootpath):
        self.file_model.set_header_name(rootpath)
        self.file_model.setRootPath(rootpath)
        self.setRootIndex(self.file_model.index(rootpath))

        self.selectionModel()
        # self.selectionModel().currentChanged.emit(self.selectionModel().currentIndex()
        # self.selectionModel().currentIndex())
        # idx = self.selectionModel().currentIndex()
        # flag = self.selectionModel().SelectionFlag.Select
        # self.selectionModel().setCurrentIndex(idx, flag)

    def _open_files_tree_context(self, position):
        cur = self.selectionModel().currentIndex()
        idx = cur.siblingAtRow(cur.row())
        path = QFileSystemModel().filePath(idx)

        menu = QMenu()
        menu.addAction(self.sp_icon.filetree_menu_copy, "Copy fullpath")
        if gettype(path) != 'folder':
            menu.addAction(self.sp_icon.filetree_menu_copy, "Copy filename")
            menu.addSeparator()
            menu.addAction(self.sp_icon.filetree_menu_open, "Show in explorer")
            menu.addAction(self.sp_icon.filetree_menu_open, "Open in associated app")
        else:
            menu.addSeparator()
            menu.addAction(self.sp_icon.filetree_menu_open, "Show in explorer")
            menu.addAction(self.sp_icon.filetree_menu_open, "Open in explorer")

        action = menu.exec_(self.viewport().mapToGlobal(position))
        if action is None:
            return
        if action.text() == "Copy fullpath":
            cb = QApplication.clipboard()
            cb.setText(QFileSystemModel().filePath(idx), mode=cb.Clipboard)
        elif action.text() == "Copy filename":
            cb = QApplication.clipboard()
            cb.setText(os.path.basename(QFileSystemModel().filePath(idx)), mode=cb.Clipboard)
        elif action.text() == "Show in explorer":
            webbrowser.open(os.path.split(path)[0], new=2)
        elif action.text() == "Open in associated app":
            webbrowser.open(path, new=2)
        elif action.text() == "Open in explorer":
            webbrowser.open(path, new=2)
