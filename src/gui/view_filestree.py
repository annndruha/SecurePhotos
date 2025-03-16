import os
import webbrowser
from pathlib import Path

from PyQt5.QtCore import QEvent, QFileInfo, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QFileIconProvider, QFileSystemModel,
                             QMenu, QSizePolicy, QTreeView, QVBoxLayout,
                             QWidget)

from src.gui.icons import Icons

SUPPORTED_EXT = {'image': ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'ppm', 'xbm', 'xpm', 'svg'],
                 'aes': ['aes'],
                 'text': ['txt', 'md', 'doc', 'docx', 'pdf', 'rtf', 'odt'],
                 'audio': ['aac', 'wav', 'mp3', 'ac3', 'ogg', 'wma'],
                 'video': ['mkv', 'mp4', 'avi', 'mov', 'webm'],
                 'zip': ['rar', 'zip'],
                 'aes_zip': ['aes_zip']}
ROTATABLE_FORMATS = ['bmp', 'jpg', 'jpeg', 'png']


def is_rotatable(fullpath: str) -> bool:
    if not fullpath:
        return False
    try:
        ext = Path(fullpath).suffix.replace('.', '').lower()
    except (AttributeError, NotImplementedError):
        return False
    if ext in ROTATABLE_FORMATS:
        return True
    return False


def gettype(fullpath: str) -> str | None:
    # Return None for not existing paths
    if fullpath is None or not os.path.exists(fullpath):
        return None

    if os.path.isdir(fullpath):
        return 'folder'

    try:
        ext = Path(fullpath).suffix.replace('.', '').lower()
    except (AttributeError, NotImplementedError):
        return None

    # Return file-type
    for key, ext_list in SUPPORTED_EXT.items():
        if ext in ext_list:
            return key
    return 'file'


class IconProvider(QFileIconProvider):
    def icon(self, parameter) -> QIcon:
        if isinstance(parameter, QFileInfo):
            if parameter.isDir():
                return self.icons.folder
            if gettype(parameter.absoluteFilePath()) == 'aes':
                return self.icons.lock
            if gettype(parameter.absoluteFilePath()) == 'aes_zip':
                return self.icons.folder_lock
            if gettype(parameter.absoluteFilePath()) == 'image':
                return self.icons.image
            if gettype(parameter.absoluteFilePath()) == 'video':
                return self.icons.movie
            if gettype(parameter.absoluteFilePath()) == 'zip':
                return self.icons.file_zip
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
        self.icons = Icons()
        icon_provider = IconProvider()
        icon_provider.icons = self.icons
        self.file_model.setIconProvider(icon_provider)
        self.setModel(self.file_model)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.customContextMenuRequested.connect(self._open_files_tree_context)

    def change_root(self, rootpath):
        self.file_model.set_header_name(rootpath)
        self.file_model.setRootPath(rootpath)
        self.setRootIndex(self.file_model.index(rootpath))
        self.selectionModel()

    def _open_files_tree_context(self, position):
        cur = self.selectionModel().currentIndex()
        idx = cur.siblingAtRow(cur.row())
        path = QFileSystemModel().filePath(idx)

        menu = QMenu()
        menu.addAction(self.icons.copy, "Copy fullpath")
        if gettype(path) != 'folder':
            menu.addAction(self.icons.copy, "Copy filename")
            menu.addSeparator()
            menu.addAction(self.icons.open, "Show in explorer")
            menu.addAction(self.icons.open, "Open in associated app")
        else:
            menu.addSeparator()
            menu.addAction(self.icons.open, "Show in explorer")
            menu.addAction(self.icons.open, "Open in explorer")

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
