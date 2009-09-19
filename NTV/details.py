# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'details.ui'
#
# Created: Mon Sep 14 11:41:22 2009
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 554)
        Dialog.setMaximumSize(QtCore.QSize(400, 560))
        self.radprof = MPL_Widget(Dialog)
        self.radprof.setGeometry(QtCore.QRect(0, 220, 400, 330))
        self.radprof.setMinimumSize(QtCore.QSize(400, 330))
        self.radprof.setMaximumSize(QtCore.QSize(16777215, 330))
        self.radprof.setObjectName("radprof")
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 10, 401, 202))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.xval = QtGui.QLabel(self.widget)
        self.xval.setFrameShape(QtGui.QFrame.StyledPanel)
        self.xval.setFrameShadow(QtGui.QFrame.Sunken)
        self.xval.setObjectName("xval")
        self.gridLayout.addWidget(self.xval, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.counts = QtGui.QLabel(self.widget)
        self.counts.setFrameShape(QtGui.QFrame.StyledPanel)
        self.counts.setFrameShadow(QtGui.QFrame.Sunken)
        self.counts.setObjectName("counts")
        self.gridLayout.addWidget(self.counts, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.background = QtGui.QLabel(self.widget)
        self.background.setFrameShape(QtGui.QFrame.StyledPanel)
        self.background.setFrameShadow(QtGui.QFrame.Sunken)
        self.background.setObjectName("background")
        self.gridLayout.addWidget(self.background, 3, 1, 1, 1)
        self.yval = QtGui.QLabel(self.widget)
        self.yval.setFrameShape(QtGui.QFrame.StyledPanel)
        self.yval.setFrameShadow(QtGui.QFrame.Sunken)
        self.yval.setObjectName("yval")
        self.gridLayout.addWidget(self.yval, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.frame = QtGui.QFrame(self.widget)
        self.frame.setMinimumSize(QtCore.QSize(200, 200))
        self.frame.setMaximumSize(QtCore.QSize(200, 200))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.vis = MPL_Widget1(self.frame)
        self.vis.setGeometry(QtCore.QRect(0, 0, 200, 200))
        self.vis.setMinimumSize(QtCore.QSize(200, 200))
        self.vis.setMaximumSize(QtCore.QSize(200, 200))
        self.vis.setObjectName("vis")
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "X Center", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Y Center", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Counts", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Background", None, QtGui.QApplication.UnicodeUTF8))

from mpl_pyqt4_widget import MPL_Widget
from mpl_pyqt4_widget_new import MPL_Widget1
