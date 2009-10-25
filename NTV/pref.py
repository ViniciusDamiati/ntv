# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pref.ui'
#
# Created: Tue Oct 20 17:15:43 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_prefs(object):
    def setupUi(self, prefs):
        prefs.setObjectName("prefs")
        prefs.resize(400, 215)
        self.verticalLayout_2 = QtGui.QVBoxLayout(prefs)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(prefs)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(prefs)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(prefs)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(prefs)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.preview20 = QtGui.QRadioButton(prefs)
        self.preview20.setObjectName("preview20")
        self.gridLayout.addWidget(self.preview20, 0, 0, 1, 2)
        self.preview5 = QtGui.QRadioButton(prefs)
        self.preview5.setObjectName("preview5")
        self.gridLayout.addWidget(self.preview5, 0, 4, 1, 1)
        self.cutsizeset = QtGui.QLineEdit(prefs)
        self.cutsizeset.setMaximumSize(QtCore.QSize(50, 16777215))
        self.cutsizeset.setObjectName("cutsizeset")
        self.gridLayout.addWidget(self.cutsizeset, 1, 0, 1, 2)
        self.plotup = QtGui.QRadioButton(prefs)
        self.plotup.setObjectName("plotup")
        self.gridLayout.addWidget(self.plotup, 2, 0, 1, 2)
        self.plotdown = QtGui.QRadioButton(prefs)
        self.plotdown.setObjectName("plotdown")
        self.gridLayout.addWidget(self.plotdown, 2, 3, 1, 2)
        self.overplot = QtGui.QRadioButton(prefs)
        self.overplot.setObjectName("overplot")
        self.gridLayout.addWidget(self.overplot, 3, 0, 1, 3)
        self.multi = QtGui.QRadioButton(prefs)
        self.multi.setObjectName("multi")
        self.gridLayout.addWidget(self.multi, 3, 3, 1, 2)
        self.preview10 = QtGui.QRadioButton(prefs)
        self.preview10.setObjectName("preview10")
        self.gridLayout.addWidget(self.preview10, 0, 2, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.ok_sync = QtGui.QPushButton(prefs)
        self.ok_sync.setMaximumSize(QtCore.QSize(100, 16777215))
        self.ok_sync.setObjectName("ok_sync")
        self.verticalLayout_2.addWidget(self.ok_sync)

        self.retranslateUi(prefs)
        QtCore.QMetaObject.connectSlotsByName(prefs)

    def retranslateUi(self, prefs):
        prefs.setWindowTitle(QtGui.QApplication.translate("prefs", "Preference", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("prefs", "Preview Size", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("prefs", "Default cut size", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("prefs", "Plot Origin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("prefs", "Dialog Box Behaivor", None, QtGui.QApplication.UnicodeUTF8))
        self.preview20.setText(QtGui.QApplication.translate("prefs", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.preview5.setText(QtGui.QApplication.translate("prefs", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.cutsizeset.setText(QtGui.QApplication.translate("prefs", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.plotup.setText(QtGui.QApplication.translate("prefs", "Upper", None, QtGui.QApplication.UnicodeUTF8))
        self.plotdown.setText(QtGui.QApplication.translate("prefs", "Lower", None, QtGui.QApplication.UnicodeUTF8))
        self.overplot.setText(QtGui.QApplication.translate("prefs", "Overplot", None, QtGui.QApplication.UnicodeUTF8))
        self.multi.setText(QtGui.QApplication.translate("prefs", "Multi Windows", None, QtGui.QApplication.UnicodeUTF8))
        self.preview10.setText(QtGui.QApplication.translate("prefs", "10", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_sync.setText(QtGui.QApplication.translate("prefs", "Ok", None, QtGui.QApplication.UnicodeUTF8))

