import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


SUPPORTED_EXT = QtGui.QImageReader.supportedImageFormats()


def geticon(fullpath):
    ext = os.path.splitext(os.path.basename(fullpath))[1].replace('.', '')
    print(ext)
    if os.path.isdir(fullpath):
        return QtGui.QIcon('images/icons/folder.svg')
    if ext in [str(ext, 'utf-8') for ext in SUPPORTED_EXT]:
        return QtGui.QIcon('images/icons/image.svg')
    elif ext == 'aes':
        return QtGui.QIcon('images/icons/lock.svg')
    else:
        return QtGui.QIcon('images/icons/file.svg')


class FilesItem(QTreeWidgetItem):
    def __init__(self, parent, fullpath, basename):
        self.parent = parent
        self.fullpath = fullpath
        self.basename = basename
        super().__init__(parent, [basename])

    def load_subtree(self):
        if not os.path.isdir(self.fullpath):
            return
        dirlist = [x for x in os.listdir(self.fullpath) if os.path.isdir(os.path.join(self.fullpath, x))]
        filelist = [x for x in os.listdir(self.fullpath) if not os.path.isdir(os.path.join(self.fullpath, x))]
        for element in dirlist + filelist:

            parent_itm = FilesItem(self, os.path.join(self.fullpath, element), os.path.basename(element))

            # parent_itm = FilesItem(os.path.join(path, element))
            # parent_itm.fullpath = os.path.join(self.fullpath, element)
            if os.path.isdir(parent_itm.fullpath):
                parent_itm.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            parent_itm.setIcon(0, geticon(parent_itm.fullpath))


    def clear(self):
        # super().clear()
        # self.__init__(self.parent, self.fullpath, self.basename)
        # print('before', self.childCount())
        for i in range(self.childCount()):
            self.removeChild(self.child(i))
        # print('after', self.childCount())




class FilesTree(QTreeWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.itemSelectionChanged.connect(self.preload_subtree)

    def load_project_structure(self, path):
        self.root_elem = FilesItem(self, path, os.path.basename(path))
        self.root_elem.load_subtree()
        self.root_elem.setExpanded(True)

    def preload_subtree(self):
        super().currentItem().clear()
        super().currentItem().load_subtree()

    def getPath(self):
        return super().currentItem().fullpath

    def clear(self):
        super().clear()
