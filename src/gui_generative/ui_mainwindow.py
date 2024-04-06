# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(840, 500))
        palette = QtGui.QPalette()
        MainWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = GraphicsView(self.widget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.widget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockFilesTree = QtWidgets.QDockWidget(MainWindow)
        self.dockFilesTree.setObjectName("dockFilesTree")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setBaseSize(QtCore.QSize(350, 0))
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.filesTree = FilesTree(self.dockWidgetContents)
        self.filesTree.setObjectName("filesTree")
        self.gridLayout.addWidget(self.filesTree, 0, 0, 1, 1)
        self.dockFilesTree.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockFilesTree)
        self.actionEnterKey = QtWidgets.QAction(MainWindow)
        self.actionEnterKey.setObjectName("actionEnterKey")
        self.actionEncrypt = QtWidgets.QAction(MainWindow)
        self.actionEncrypt.setObjectName("actionEncrypt")
        self.actionOpenFolder = QtWidgets.QAction(MainWindow)
        self.actionOpenFolder.setObjectName("actionOpenFolder")
        self.actionRotateLeft = QtWidgets.QAction(MainWindow)
        self.actionRotateLeft.setObjectName("actionRotateLeft")
        self.actionRotateRight = QtWidgets.QAction(MainWindow)
        self.actionRotateRight.setObjectName("actionRotateRight")
        self.actionFullscreen = QtWidgets.QAction(MainWindow)
        self.actionFullscreen.setObjectName("actionFullscreen")
        self.actionChangeFit = QtWidgets.QAction(MainWindow)
        self.actionChangeFit.setEnabled(False)
        self.actionChangeFit.setObjectName("actionChangeFit")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionFoldeDecrypt = QtWidgets.QAction(MainWindow)
        self.actionFoldeDecrypt.setObjectName("actionFoldeDecrypt")
        self.toolBar.addAction(self.actionOpenFolder)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRotateLeft)
        self.toolBar.addAction(self.actionRotateRight)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionChangeFit)
        self.toolBar.addAction(self.actionFullscreen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEnterKey)
        self.toolBar.addAction(self.actionEncrypt)
        self.toolBar.addAction(self.actionFoldeDecrypt)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SecurePhotos"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Tool Bar"))
        self.dockFilesTree.setWindowTitle(_translate("MainWindow", "Files Tree"))
        self.actionEnterKey.setText(_translate("MainWindow", "Enter Key"))
        self.actionEncrypt.setText(_translate("MainWindow", "Encrypt"))
        self.actionOpenFolder.setText(_translate("MainWindow", "Open Folder"))
        self.actionRotateLeft.setText(_translate("MainWindow", "Rotate Left"))
        self.actionRotateRight.setText(_translate("MainWindow", "Rotate Right"))
        self.actionFullscreen.setText(_translate("MainWindow", "Fullscreen"))
        self.actionChangeFit.setText(_translate("MainWindow", "Can\'t fit"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionFoldeDecrypt.setText(_translate("MainWindow", "Decrypt Folder"))
from src.gui.view_filestree import FilesTree
from src.gui.window_graphicsview import GraphicsView
