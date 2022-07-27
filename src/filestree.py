import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class FilesItem(QTreeWidgetItem):
    def __init__(self, parent, fullpath, basename):
        # print(type(parent))
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
                parent_itm.setIcon(0, QtGui.QIcon('images/icons/folder.svg'))
                # parent_itm.addChilds()
                # self.load_project_structure(parent, parent_itm.fullpath)
            else:
                ext = os.path.splitext(parent_itm.fullpath)[1].replace('.', '')
                supported_ext = QtGui.QImageReader.supportedImageFormats()
                if ext in [str(ext, 'utf-8') for ext in supported_ext]:
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/image.svg'))
                elif ext == 'aes':
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/lock.svg'))
                else:
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/file.svg'))

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
        dirlist = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
        filelist = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))]
        for element in dirlist + filelist:

            parent_itm = FilesItem(self, os.path.join(path, element), os.path.basename(element))

            # parent_itm = FilesItem(os.path.join(path, element))
            # parent_itm.fullpath = os.path.join(path, element)
            if os.path.isdir(parent_itm.fullpath):
                parent_itm.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                parent_itm.setIcon(0, QtGui.QIcon('images/icons/folder.svg'))
                # parent_itm.addChilds()
                # self.load_project_structure(parent, parent_itm.fullpath)
            else:
                ext = os.path.splitext(parent_itm.fullpath)[1].replace('.', '')
                supported_ext = QtGui.QImageReader.supportedImageFormats()
                if ext in [str(ext, 'utf-8') for ext in supported_ext]:
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/image.svg'))
                elif ext == 'aes':
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/lock.svg'))
                else:
                    parent_itm.setIcon(0, QtGui.QIcon('images/icons/file.svg'))
            # self.insertChild()

    def preload_subtree(self):
        super().currentItem().clear()
        super().currentItem().load_subtree()

    def getPath(self):
        return super().currentItem().fullpath

    def clear(self):
        super().clear()
