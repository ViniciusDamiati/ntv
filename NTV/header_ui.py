# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'header.ui'
#
# Created: Mon Sep 28 13:46:11 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_header(object):
    def setupUi(self, header):
        header.setObjectName("header")
        header.resize(503, 599)
        header.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(header)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cardlist = QtGui.QListWidget(header)
        self.cardlist.setObjectName("cardlist")
        self.verticalLayout.addWidget(self.cardlist)

        self.retranslateUi(header)
        QtCore.QMetaObject.connectSlotsByName(header)

    def retranslateUi(self, header):
        header.setWindowTitle(QtGui.QApplication.translate("header", "Header", None, QtGui.QApplication.UnicodeUTF8))

