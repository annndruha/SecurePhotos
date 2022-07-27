import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

IMG_EXT = [str(ext, 'utf-8').lower() for ext in QtGui.QImageReader.supportedImageFormats()]
TEXT_EXT = ['txt', 'md', 'doc', 'docx', 'pdf', 'rtf', 'odt']
AUDIO_EXT = ['aac', 'wav', 'mp3', 'ac3', 'ogg', 'wma']
VIDEO_EXT = ['mkv', 'mp4', 'avi', 'mov']
ZIP_EXT = ['rar', 'zip']


def geticon(fullpath):  # Not for folders
    ext = os.path.splitext(os.path.basename(fullpath))[1].replace('.', '').lower()
    if ext == 'aes':
        return QtGui.QIcon('images/icons/lock.svg')
    elif ext in IMG_EXT:
        return QtGui.QIcon('images/icons/image.svg')
    elif ext in TEXT_EXT:
        return QtGui.QIcon('images/icons/file_text.svg')
    elif ext in AUDIO_EXT:
        return QtGui.QIcon('images/icons/file_audio.svg')
    elif ext in VIDEO_EXT:
        return QtGui.QIcon('images/icons/movie.svg')
    elif ext in ZIP_EXT:
        return QtGui.QIcon('images/icons/file_zip.svg')
    else:
        return QtGui.QIcon('images/icons/file.svg')


class FilesItem(QTreeWidgetItem):
    def __init__(self, parent, fullpath, basename):
        super().__init__(parent, [basename])
        self.parent = parent
        self.fullpath = fullpath
        self.basename = basename

    def __repr__(self):
        return str(self.basename)

    def load_subtree(self):
        self.clear()
        if not os.path.isdir(self.fullpath):
            return
        dirlist = [x for x in os.listdir(self.fullpath) if os.path.isdir(os.path.join(self.fullpath, x))]
        filelist = [x for x in os.listdir(self.fullpath) if not os.path.isdir(os.path.join(self.fullpath, x))]
        for element in dirlist + filelist:

            parent_itm = FilesItem(self, os.path.join(self.fullpath, element), os.path.basename(element))
            if os.path.isdir(parent_itm.fullpath):
                parent_itm.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                parent_itm.setIcon(0, QtGui.QIcon('images/icons/folder.svg'))
            else:
                parent_itm.setIcon(0, geticon(parent_itm.fullpath))

    def clear(self):
        while self.childCount() > 0:
            for i in range(self.childCount()):
                self.removeChild(self.child(i))


class FilesTree(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.root_elem = None
        self.itemExpanded.connect(self._item_expanded)
        self.itemCollapsed.connect(self._item_collapsed)
        self.setRootIsDecorated(False)

    def load_project_structure(self, path):
        self.root_elem = FilesItem(self, path, path)
        self.root_elem.load_subtree()
        self.root_elem.setExpanded(True)

    def _item_expanded(self, item):
        item.load_subtree()
        item.setIcon(0, QtGui.QIcon('images/icons/folder_open.svg'))

    def _item_collapsed(self, item):
        item.clear()
        item.setIcon(0, QtGui.QIcon('images/icons/folder.svg'))

    def get_path(self):
        return self.currentItem().fullpath

    def delete_item(self):
        item = self.currentItem()
        item.parent.removeChild(item)
