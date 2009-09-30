# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'threeD.ui'
#
# Created: Mon Sep 28 23:10:54 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_threeD(object):
    def setupUi(self, threeD):
        threeD.setObjectName("threeD")
        threeD.resize(426, 83)
        self.verticalLayout = QtGui.QVBoxLayout(threeD)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fnumbar = QtGui.QSlider(threeD)
        self.fnumbar.setOrientation(QtCore.Qt.Horizontal)
        self.fnumbar.setTickPosition(QtGui.QSlider.TicksBelow)
        self.fnumbar.setObjectName("fnumbar")
        self.verticalLayout.addWidget(self.fnumbar)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(threeD)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.fnumber = QtGui.QLabel(threeD)
        self.fnumber.setMinimumSize(QtCore.QSize(50, 0))
        self.fnumber.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fnumber.setFrameShadow(QtGui.QFrame.Sunken)
        self.fnumber.setObjectName("fnumber")
        self.horizontalLayout.addWidget(self.fnumber)
        self.play = QtGui.QCommandLinkButton(threeD)
        self.play.setMinimumSize(QtCore.QSize(0, 41))
        self.play.setMaximumSize(QtCore.QSize(85, 16777215))
        self.play.setObjectName("play")
        self.horizontalLayout.addWidget(self.play)
        self.label_3 = QtGui.QLabel(threeD)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.delay = QtGui.QLineEdit(threeD)
        self.delay.setMinimumSize(QtCore.QSize(40, 0))
        self.delay.setObjectName("delay")
        self.horizontalLayout.addWidget(self.delay)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(threeD)
        QtCore.QMetaObject.connectSlotsByName(threeD)

    def retranslateUi(self, threeD):
        threeD.setWindowTitle(QtGui.QApplication.translate("threeD", "3D Navigator", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("threeD", "Frame Number", None, QtGui.QApplication.UnicodeUTF8))
        self.play.setText(QtGui.QApplication.translate("threeD", "play", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("threeD", "Time Delay", None, QtGui.QApplication.UnicodeUTF8))
        self.delay.setText(QtGui.QApplication.translate("threeD", "0.5", None, QtGui.QApplication.UnicodeUTF8))

