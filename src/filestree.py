import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class FilesItem(QTreeWidgetItem):
    def __init__(self, parent, basename):
        # print(type(parent))
        super().__init__(parent, basename)
        self.fullpath = None

    def addChilds(self):
        dirlist = [x for x in os.listdir(self.fullpath) if os.path.isdir(os.path.join(self.fullpath, x))]
        filelist = [x for x in os.listdir(self.fullpath) if not os.path.isdir(os.path.join(self.fullpath, x))]
        for element in dirlist + filelist:

            parent_itm = FilesItem(self, [os.path.basename(element)])

            # parent_itm = FilesItem(os.path.join(path, element))
            parent_itm.fullpath = os.path.join(self.fullpath, element)
            if os.path.isdir(parent_itm.fullpath):
                parent_itm.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                parent_itm.setIcon(0, QtGui.QIcon('images/icons/folder.svg'))
                parent_itm.addChilds()
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



class FilesTree(QTreeWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.itemSelectionChanged.connect(self.current_select)

    def load_project_structure(self, path):
        dirlist = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
        filelist = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))]
        for element in dirlist + filelist:

            parent_itm = FilesItem(self, [os.path.basename(element)])

            # parent_itm = FilesItem(os.path.join(path, element))
            parent_itm.fullpath = os.path.join(path, element)
            if os.path.isdir(parent_itm.fullpath):
                parent_itm.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                parent_itm.setIcon(0, QtGui.QIcon('images/icons/folder.svg'))
                parent_itm.addChilds()
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

    def current_select(self):
        print(self.currentItem().fullpath)
