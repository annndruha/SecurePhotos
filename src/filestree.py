import os
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileIconProvider

SUPPORTED_EXT = {'image': ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'ppm', 'xbm', 'xpm', 'svg'],
                 'aes': ['aes'],
                 'text': ['txt', 'md', 'doc', 'docx', 'pdf', 'rtf', 'odt'],
                 'audio': ['aac', 'wav', 'mp3', 'ac3', 'ogg', 'wma'],
                 'video': ['mkv', 'mp4', 'avi', 'mov'],
                 'zip': ['rar', 'zip']}


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


class FilesTree(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_model = QFileSystemModel()
        self.file_model.setIconProvider(QFileIconProvider())
        self.setModel(self.file_model)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def change_root(self, rootpath):
        self.file_model.setRootPath(rootpath)
        self.setRootIndex(self.file_model.index(rootpath))
