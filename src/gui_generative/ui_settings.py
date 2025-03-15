# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer\settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(539, 401)
        font = QtGui.QFont()
        font.setPointSize(10)
        SettingsDialog.setFont(font)
        SettingsDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SettingsDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkRotateLeft = QtWidgets.QCheckBox(self.tab_1)
        self.checkRotateLeft.setChecked(True)
        self.checkRotateLeft.setObjectName("checkRotateLeft")
        self.verticalLayout_3.addWidget(self.checkRotateLeft)
        self.checkRotateRight = QtWidgets.QCheckBox(self.tab_1)
        self.checkRotateRight.setChecked(True)
        self.checkRotateRight.setObjectName("checkRotateRight")
        self.verticalLayout_3.addWidget(self.checkRotateRight)
        self.checkDelete = QtWidgets.QCheckBox(self.tab_1)
        self.checkDelete.setChecked(True)
        self.checkDelete.setObjectName("checkDelete")
        self.verticalLayout_3.addWidget(self.checkDelete)
        self.checkFitView = QtWidgets.QCheckBox(self.tab_1)
        self.checkFitView.setChecked(True)
        self.checkFitView.setObjectName("checkFitView")
        self.verticalLayout_3.addWidget(self.checkFitView)
        self.checkFullscreen = QtWidgets.QCheckBox(self.tab_1)
        self.checkFullscreen.setChecked(True)
        self.checkFullscreen.setObjectName("checkFullscreen")
        self.verticalLayout_3.addWidget(self.checkFullscreen)
        self.checkEncrypt = QtWidgets.QCheckBox(self.tab_1)
        self.checkEncrypt.setChecked(True)
        self.checkEncrypt.setObjectName("checkEncrypt")
        self.verticalLayout_3.addWidget(self.checkEncrypt)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.enableCopyToTarget = QtWidgets.QCheckBox(self.tab_2)
        self.enableCopyToTarget.setObjectName("enableCopyToTarget")
        self.gridLayout.addWidget(self.enableCopyToTarget, 0, 2, 1, 1)
        self.labelTarget = QtWidgets.QLabel(self.tab_2)
        self.labelTarget.setObjectName("labelTarget")
        self.gridLayout.addWidget(self.labelTarget, 1, 2, 1, 1)
        self.selectCopyFolder = QtWidgets.QPushButton(self.tab_2)
        self.selectCopyFolder.setObjectName("selectCopyFolder")
        self.gridLayout.addWidget(self.selectCopyFolder, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout1 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout1.setObjectName("verticalLayout1")
        self.label_about = QtWidgets.QLabel(self.tab_3)
        self.label_about.setObjectName("label_about")
        self.verticalLayout1.addWidget(self.label_about)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout1.addItem(spacerItem2)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_apply = QtWidgets.QPushButton(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_apply.setFont(font)
        self.pushButton_apply.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.gridLayout_2.addWidget(self.pushButton_apply, 0, 2, 1, 1)
        self.pushButton_cancel = QtWidgets.QPushButton(SettingsDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout_2.addWidget(self.pushButton_cancel, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.retranslateUi(SettingsDialog)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.checkRotateLeft.setText(_translate("SettingsDialog", "Show action \"Rotate Left\""))
        self.checkRotateRight.setText(_translate("SettingsDialog", "Show action \"Rotate Right\""))
        self.checkDelete.setText(_translate("SettingsDialog", "Show action \"Delete\""))
        self.checkFitView.setText(_translate("SettingsDialog", "Show action \"Fit view\""))
        self.checkFullscreen.setText(_translate("SettingsDialog", "Show action \"Fullscreen\""))
        self.checkEncrypt.setText(_translate("SettingsDialog", "Show Encrypt/Decrypt actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("SettingsDialog", "Settings"))
        self.enableCopyToTarget.setText(_translate("SettingsDialog", "Enable copy to target button"))
        self.labelTarget.setText(_translate("SettingsDialog", "Copy target path"))
        self.selectCopyFolder.setText(_translate("SettingsDialog", "Select target"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("SettingsDialog", "Additional"))
        self.label_about.setText(_translate("SettingsDialog", "SecurePhotos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("SettingsDialog", "About"))
        self.pushButton_apply.setText(_translate("SettingsDialog", "Apply"))
        self.pushButton_cancel.setText(_translate("SettingsDialog", "Cancel"))
