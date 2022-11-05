# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.filesTree = FilesTree(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filesTree.sizePolicy().hasHeightForWidth())
        self.filesTree.setSizePolicy(sizePolicy)
        self.filesTree.setMinimumSize(QtCore.QSize(400, 0))
        self.filesTree.setMaximumSize(QtCore.QSize(400, 16777215))
        self.filesTree.setObjectName("filesTree")
        self.filesTree.header().setVisible(False)
        self.gridLayout.addWidget(self.filesTree, 0, 0, 1, 1)
        self.imageView = QtWidgets.QLabel(self.widget)
        self.imageView.setAlignment(QtCore.Qt.AlignCenter)
        self.imageView.setObjectName("imageView")
        self.gridLayout.addWidget(self.imageView, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.widget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionEnterKey = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../images/icons/key.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionEnterKey.setIcon(icon1)
        self.actionEnterKey.setObjectName("actionEnterKey")
        self.actionEncrypt = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../images/icons/lock.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionEncrypt.setIcon(icon2)
        self.actionEncrypt.setObjectName("actionEncrypt")
        self.actionOpenFolder = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../images/icons/folder_open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionOpenFolder.setIcon(icon3)
        self.actionOpenFolder.setObjectName("actionOpenFolder")
        self.actionRotateLeft = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../images/icons/rotate_left.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRotateLeft.setIcon(icon4)
        self.actionRotateLeft.setObjectName("actionRotateLeft")
        self.actionRotateRight = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../images/icons/rotate_right.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRotateRight.setIcon(icon5)
        self.actionRotateRight.setObjectName("actionRotateRight")
        self.actionFullscreen = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../images/icons/open_full.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFullscreen.setIcon(icon6)
        self.actionFullscreen.setObjectName("actionFullscreen")
        self.actionTreeView = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../images/icons/tree.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionTreeView.setIcon(icon7)
        self.actionTreeView.setObjectName("actionTreeView")
        self.actionActualSize = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../images/icons/zoom_in.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionActualSize.setIcon(icon8)
        self.actionActualSize.setObjectName("actionActualSize")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../images/icons/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionDelete.setIcon(icon9)
        self.actionDelete.setObjectName("actionDelete")
        self.actionFitSize = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("../images/icons/zoom_out.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionFitSize.setIcon(icon10)
        self.actionFitSize.setObjectName("actionFitSize")
        self.toolBar.addAction(self.actionOpenFolder)
        self.toolBar.addAction(self.actionTreeView)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRotateLeft)
        self.toolBar.addAction(self.actionRotateRight)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionActualSize)
        self.toolBar.addAction(self.actionFitSize)
        self.toolBar.addAction(self.actionFullscreen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEnterKey)
        self.toolBar.addAction(self.actionEncrypt)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SecurePhotos"))
        self.imageView.setText(_translate("MainWindow", "Image not selected"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionEnterKey.setText(_translate("MainWindow", "Enter Key"))
        self.actionEncrypt.setText(_translate("MainWindow", "Encrypt"))
        self.actionOpenFolder.setText(_translate("MainWindow", "Open Folder"))
        self.actionRotateLeft.setText(_translate("MainWindow", "Rotate Left"))
        self.actionRotateRight.setText(_translate("MainWindow", "Rotate Right"))
        self.actionFullscreen.setText(_translate("MainWindow", "Fullscreen"))
        self.actionTreeView.setText(_translate("MainWindow", "Tree View"))
        self.actionActualSize.setText(_translate("MainWindow", "Actual Size"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionFitSize.setText(_translate("MainWindow", "Fit Size"))
from src.filestree import FilesTree
