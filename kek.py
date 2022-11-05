import sys
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QFileIconProvider


class IconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QtGui.QIcon("images/icons/folder.svg")
        return QFileIconProvider.icon(self, fileInfo)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    file_model = QtWidgets.QFileSystemModel()
    file_model.setIconProvider(IconProvider())
    file_model.setRootPath(QtCore.QDir.currentPath())
    browse_tree = QtWidgets.QTreeView()
    browse_tree.setModel(file_model)
    browse_tree.show()
    sys.exit(app.exec_())
