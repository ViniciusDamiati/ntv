# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'details.ui'
#
# Created: Tue Sep 22 15:05:31 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(415, 565)
        Dialog.setMaximumSize(QtCore.QSize(415, 565))
        Dialog.setModal(False)
        self.radprof = MPL_Widget(Dialog)
        self.radprof.setGeometry(QtCore.QRect(10, 220, 401, 330))
        self.radprof.setMinimumSize(QtCore.QSize(300, 330))
        self.radprof.setMaximumSize(QtCore.QSize(16777215, 330))
        self.radprof.setObjectName("radprof")
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 401, 202))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.xval = QtGui.QLabel(self.layoutWidget)
        self.xval.setFrameShape(QtGui.QFrame.StyledPanel)
        self.xval.setFrameShadow(QtGui.QFrame.Sunken)
        self.xval.setObjectName("xval")
        self.gridLayout.addWidget(self.xval, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.counts = QtGui.QLabel(self.layoutWidget)
        self.counts.setFrameShape(QtGui.QFrame.StyledPanel)
        self.counts.setFrameShadow(QtGui.QFrame.Sunken)
        self.counts.setObjectName("counts")
        self.gridLayout.addWidget(self.counts, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.background = QtGui.QLabel(self.layoutWidget)
        self.background.setFrameShape(QtGui.QFrame.StyledPanel)
        self.background.setFrameShadow(QtGui.QFrame.Sunken)
        self.background.setObjectName("background")
        self.gridLayout.addWidget(self.background, 3, 1, 1, 1)
        self.yval = QtGui.QLabel(self.layoutWidget)
        self.yval.setFrameShape(QtGui.QFrame.StyledPanel)
        self.yval.setFrameShadow(QtGui.QFrame.Sunken)
        self.yval.setObjectName("yval")
        self.gridLayout.addWidget(self.yval, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.frame = QtGui.QFrame(self.layoutWidget)
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
