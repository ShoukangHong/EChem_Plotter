# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mngTab.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import (QListWidget, QMenu, QAction, QMessageBox, QDialog, QFrame, QLabel, QHBoxLayout, QRadioButton,
                             QCheckBox, QLineEdit)
from PyQt5 import uic, QtCore

MainUI, MainWindow = uic.loadUiType("UI/mainWindow.ui")
MngDlgUI, MngDlgWindow = uic.loadUiType("UI/mngDialog.ui")

EMPTY = {'rParam':{}, 'oParam':{}}
FORMATRAWDATA = {'rParam':{
                    'spliter': {'term': 'split text', 'type': str, 'option': {'tab': '\n', 'comma':',', 'text': True}}}, 
                'oParam':{
                    'starter': {'term': 'start text', 'type': str, 'text': True, 'option': {'tab': '\n', 'comma':',', 'text': True}},
                    'ender': {'term': 'end text', 'type': str, 'text': True, 'option': {'tab': '\n', 'comma':',', 'text': True}}}}

TRUNCATEDATA = {'rParam':{}, 
                'oParam':{
                    'step':{'term': 'step', 'type':int, 'text':True},
                    'start':{'term': 'start index', 'type':int, 'text':True},
                    'end':{'term': 'end index', 'type':int, 'text':True}}}


ACTIONDICT = {
    'Choose Action': EMPTY,
    'Format Raw Data':FORMATRAWDATA,
    'Truncate Data':TRUNCATEDATA,
    'Set Variable':{'rParam':{}, 'oParam':{}},
    'Add Plot Data':{'rParam':{}, 'oParam':{}},
    'Modify Plot Data':{'rParam':{}, 'oParam':{}},
    'Set Plot Data Range By Value':{'rParam':{}, 'oParam':{}},
    'Set Plot Data Range By Turn':{'rParam':{}, 'oParam':{}}
    }

class MngDialogWidget(MngDlgWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = MngDlgUI()
        self.ui.setupUi(self)
        self.connectEvents()
        self.paramWidgets = []
        
    def connectEvents(self):
        actionCB = self.ui.actionCB
        actionCB.activated.connect(self.selectAction)
    
    def selectAction(self, idx):
        text = self.ui.actionCB.itemText(idx)
        print(text)
        self.clearParams()
        
        for param in ACTIONDICT[text]['rParam'].values():
            self.addrequiredParam(param)
            
        for param in ACTIONDICT[text]['oParam'].values():
            self.addOptionalParam(param)
        
    def addrequiredParam(self, param):
        box = self.ui.rParamBox
        frame = QFrame(box)
        QHBoxLayout(frame)
        label = QLabel(frame)
        frame.layout().addWidget(label)
        label.setText(param['term'])
        self.addOptions(frame, param.get('option', {}))
        box.layout().addWidget(frame)
        self.paramWidgets.append(frame)
    
    def addOptionalParam(self, param):
        box = self.ui.oParamBox
        frame = QFrame(box)
        innerFrm = QFrame(frame)
        QHBoxLayout(frame)
        QHBoxLayout(innerFrm)
        checkBox = QCheckBox(frame)
        frame.layout().addWidget(checkBox)
        frame.layout().addWidget(innerFrm)
        checkBox.setText(param['term'])
        innerFrm.setDisabled(True)
        checkBox.stateChanged.connect(lambda: innerFrm.setDisabled(not checkBox.isChecked()))
        self.addOptions(innerFrm, param.get('option', {}))
        box.layout().addWidget(frame)
        self.paramWidgets.append(frame)
    
    def clearParams(self):
        for widget in self.paramWidgets:
            widget.deleteLater()
        self.paramWidgets = []

    def addOptions(self, frame, options):
        buttons = []
        for key, val in options.items():
            button = QRadioButton(frame)
            frame.layout().addWidget(button)
            button.setText(key)
            buttons.append(button)
            if key == 'text':
                lineEdit = QLineEdit(button)
                frame.layout().addWidget(lineEdit)
                lineEdit.setDisabled(True)
                button.toggled.connect(lambda isChecked: lineEdit.setDisabled(not isChecked))
                
        

class MngListWidget(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.itemDoubleClicked.connect(self.newActionWindow)
    
    def newActionWindow(self, ev):
            print('pop up window')
    
    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Delete:
            i = self.currentRow()
            item = self.currentItem()
            if item.text() != '':
                self.takeItem(i)
        else:
            super().keyPressEvent(ev)
            
    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            target = self.itemAt(ev.pos())
            idx = self.row(target)
            menu = QMenu()
            insertAct = QAction("insert")
            insertAct.triggered.connect(lambda: self.insertNewEvent(idx))
            editAct = QAction("edit")
            editAct.triggered.connect(lambda: self.setText('sb'))
            cancelAct = QAction("cancel")
            
            if target:
                self.setCurrentItem(target)
            if not target or target.text() == '':
                editAct.setDisabled(True)
            
            menu.addAction(insertAct)
            menu.addAction(editAct)
            menu.addAction(cancelAct)
            menu.exec_(ev.globalPos())
        else:
            super().mousePressEvent(ev)
    
    def insertNewEvent(self, idx):
        dlg = MngDialogWidget(self)
        dlg.setWindowTitle("Setup New Action")
        button = dlg.exec()
        print(button)
        while idx > 0 and self.item(idx - 1).text() == '':
            idx-= 1
        self.insertItem(idx, 'new Item')
    
    def setText(self, string):
        self.currentItem().setText(string)
    
    def compileActions(self):
        print('compile actions')
    
    def resetActions(self):
        for row in range(self.count()-1, -1, -1):
            if self.item(row).text() != '':
                self.takeItem(row)
        print('popUpWindow')

MngTabUI, MngTabWindow = uic.loadUiType("UI/mngTab.ui")
class MngTabWidget(MngTabWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = MngTabUI()
        self.ui.setupUi(self)
        self.connectEvents()
    
    def actList(self):
        return self.ui.actionList
    
    def connectEvents(self):
        self.ui.compileBtn.clicked.connect(self.actList().compileActions)
        self.ui.resetBtn.clicked.connect(self.actList().resetActions)