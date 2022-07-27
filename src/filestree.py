import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

SUPPORTED_EXT = QtGui.QImageReader.supportedImageFormats()


def geticon(fullpath):
    ext = os.path.splitext(os.path.basename(fullpath))[1].replace('.', '')
    if ext in [str(ext, 'utf-8') for ext in SUPPORTED_EXT]:
        return QtGui.QIcon('images/icons/image.svg')
    elif ext == 'aes':
        return QtGui.QIcon('images/icons/lock.svg')
    else:
        return QtGui.QIcon('images/icons/file.svg')


class FilesItem(QTreeWidgetItem):
    def __init__(self, parent, fullpath, basename):
        super().__init__(parent, [basename])
        self.parent = parent
        self.fullpath = fullpath
        self.basename = basename
        # self.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)

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

    def getPath(self):
        return self.currentItem().fullpath

    def deleteItem(self):
        item = self.currentItem()
        print(item)
        idx = item.parent.indexOfChild(item)
        item.parent.load_subtree()
        new_item = item.parent.child(idx)
        item.parent.setSelected(False)
        new_item.setSelected(True)
