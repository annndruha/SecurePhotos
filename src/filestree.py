import os

from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileIconProvider

SUPPORTED_EXT = {'image': ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'ppm', 'xbm', 'xpm', 'svg'],
                 'aes': ['aes'],
                 'text': ['txt', 'md', 'doc', 'docx', 'pdf', 'rtf', 'odt'],
                 'audio': ['aac', 'wav', 'mp3', 'ac3', 'ogg', 'wma'],
                 'video': ['mkv', 'mp4', 'avi', 'mov'],
                 'zip': ['rar', 'zip'],
                 'aes_zip': ['aes_zip']}


def is_rotatable(fullpath):
    ext = os.path.splitext(os.path.basename(fullpath))[1].replace('.', '').lower()
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
                icon = QtGui.QIcon("images/icons/folder.svg")
                # noinspection PyUnresolvedReferences
                icon.addFile("images/icons/folder_open.svg", state=icon.On)
                return icon
            if gettype(parameter.absoluteFilePath()) == 'aes':
                return QtGui.QIcon("images/icons/lock.svg")
            if gettype(parameter.absoluteFilePath()) == 'aes_zip':
                return QtGui.QIcon("images/icons/folder_lock.svg")
            if gettype(parameter.absoluteFilePath()) == 'image':
                return QtGui.QIcon("images/icons/image.svg")
            if gettype(parameter.absoluteFilePath()) == 'video':
                return QtGui.QIcon("images/icons/movie.svg")
            if gettype(parameter.absoluteFilePath()) == 'zip':
                return QtGui.QIcon("images/icons/file_zip.svg")
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


class FilesTree(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_model = ProxyQFileSystemModel()
        self.file_model.setIconProvider(IconProvider())
        self.setModel(self.file_model)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.file_model.directoryLoaded.connect(self.on_directory_loaded)

    def on_directory_loaded(self, rootpath):
        idx = self.file_model.index(rootpath)
        self.selectionModel().clearSelection()
        if self.file_model.rowCount(idx) > 0:
            index = self.file_model.index(0, 0, idx)
            self.selectionModel().setCurrentIndex(index, self.selectionModel().SelectionFlag.Select)

    def change_root(self, rootpath):
        self.file_model.set_header_name(rootpath)
        self.file_model.setRootPath(rootpath)
        self.setRootIndex(self.file_model.index(rootpath))

        self.selectionModel()
        # self.selectionModel().currentChanged.emit(self.selectionModel().currentIndex()
        # self.selectionModel().currentIndex())
        # idx = self.selectionModel().currentIndex()
        # flag = self.selectionModel().SelectionFlag.Select
        # print(idx)
        # self.selectionModel().setCurrentIndex(idx, flag)
