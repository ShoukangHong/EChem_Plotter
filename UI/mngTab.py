# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mngTab.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mngTab(object):
    def setupUi(self, mngTab):
        mngTab.setObjectName("mngTab")
        mngTab.resize(345, 306)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mngTab.sizePolicy().hasHeightForWidth())
        mngTab.setSizePolicy(sizePolicy)
        mngTab.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout = QtWidgets.QVBoxLayout(mngTab)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.eventList = EventListWidget(mngTab)
        self.eventList.setAutoFillBackground(True)
        self.eventList.setDragEnabled(True)
        self.eventList.setDragDropOverwriteMode(False)
        self.eventList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.eventList.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.eventList.setAlternatingRowColors(True)
        self.eventList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.eventList.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.eventList.setSelectionRectVisible(False)
        self.eventList.setObjectName("eventList")
        item = QtWidgets.QListWidgetItem()
        self.eventList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.eventList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.eventList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.eventList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.eventList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.eventList.addItem(item)
        self.verticalLayout.addWidget(self.eventList)
        self.frame = QtWidgets.QFrame(mngTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 25))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.resetBtn = QtWidgets.QPushButton(self.frame)
        self.resetBtn.setObjectName("resetBtn")
        self.horizontalLayout.addWidget(self.resetBtn)
        self.compileBtn = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.compileBtn.sizePolicy().hasHeightForWidth())
        self.compileBtn.setSizePolicy(sizePolicy)
        self.compileBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.compileBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.compileBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.compileBtn.setObjectName("compileBtn")
        self.horizontalLayout.addWidget(self.compileBtn)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(mngTab)
        QtCore.QMetaObject.connectSlotsByName(mngTab)

    def retranslateUi(self, mngTab):
        _translate = QtCore.QCoreApplication.translate
        mngTab.setWindowTitle(_translate("mngTab", "Form"))
        __sortingEnabled = self.eventList.isSortingEnabled()
        self.eventList.setSortingEnabled(False)
        self.eventList.setSortingEnabled(__sortingEnabled)
        self.resetBtn.setText(_translate("mngTab", "Reset"))
        self.compileBtn.setText(_translate("mngTab", "Compile"))

from PlotterWidgets import EventListWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mngTab = QtWidgets.QWidget()
    ui = Ui_mngTab()
    ui.setupUi(mngTab)
    mngTab.show()
    sys.exit(app.exec_())

