# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './UI/DialogLoading.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgLoading(object):
    def setupUi(self, DlgLoading):
        DlgLoading.setObjectName("DlgLoading")
        DlgLoading.setWindowModality(QtCore.Qt.ApplicationModal)
        DlgLoading.resize(218, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DlgLoading.sizePolicy().hasHeightForWidth())
        DlgLoading.setSizePolicy(sizePolicy)
        DlgLoading.setMinimumSize(QtCore.QSize(200, 200))
        DlgLoading.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(DlgLoading)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(DlgLoading)
        self.frame.setStyleSheet("background-color:white;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 30)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_loading = QtWidgets.QLabel(self.frame)
        self.lbl_loading.setStyleSheet("")
        self.lbl_loading.setText("")
        self.lbl_loading.setPixmap(QtGui.QPixmap("../../IMG/loading.png"))
        self.lbl_loading.setObjectName("lbl_loading")
        self.verticalLayout_2.addWidget(self.lbl_loading)
        self.lbl_text = QtWidgets.QLabel(self.frame)
        self.lbl_text.setStyleSheet("")
        self.lbl_text.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_text.setObjectName("lbl_text")
        self.verticalLayout_2.addWidget(self.lbl_text)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(DlgLoading)
        QtCore.QMetaObject.connectSlotsByName(DlgLoading)

    def retranslateUi(self, DlgLoading):
        _translate = QtCore.QCoreApplication.translate
        DlgLoading.setWindowTitle(_translate("DlgLoading", "Loading"))
        self.lbl_text.setText(_translate("DlgLoading", "\n"
"사진을 분석중입니다.\n"
"잠시만 기다려 주세요"))
