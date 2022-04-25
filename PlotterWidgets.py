# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mngTab.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import (QListWidget, QMenu, QAction, QMessageBox, QDialog,
                             QFrame, QLabel, QHBoxLayout, QRadioButton, QListWidgetItem, QTableWidgetItem,
                             QCheckBox, QLineEdit, QFileDialog)
from PyQt5 import uic, QtCore
from MngOptions import MNGACTIONDICT
from PlotOptions import PLOTACTIONDICT
from PyQt5.QtGui import QIcon
from Plotter_Core import DataManager, EchemPlotter
import json
MainUI, MainWindow = uic.loadUiType("UI/mainWindow.ui")
ActionDlgUI, ActionDlgWindow = uic.loadUiType("UI/actionDialog.ui")

class MngDialogFrame(QFrame):
    def __init__(self, parent, key , param):
        super().__init__(parent)
        self._checkBox = None
        self._inputInfo = {
            'valid': False,
            'key': None,
            'term': None,
            'type': None,
            'value': None}
        self.setInput('key', key)
        self.setInput('term', param['term'])
        self.setInput('type', param['type'])
        
    # ==========================
    # Signal Handlers
    # ==========================
    def buttonToggle(self, isChecked, value):
        '''reaction when a button is switched on or off'''
        if (isChecked):
            self.setInput('valid', True)
            self.setInput('value', value)
    
    def lineEditButtonToggle(self, isChecked, lineEdit):
        '''reaction when a line edit button is switched on or off'''
        lineEdit.setDisabled(not isChecked)
        if (isChecked):
            text = lineEdit.text()
            self.lineEditChanged(lineEdit)
            self.setInput('value', text)
    
    def lineEditChanged(self, lineEdit):
        '''reaction when a line edit widget changes content'''
        text = lineEdit.displayText()
        if text != '':
            self.setInput('value', text)
            self.setInput('valid', True)    
        else:
            self.setInput('valid', False)
            
    # ==========================
    # Input Management
    # ==========================
    def getInputSetup(self):
        '''get the setup and value for input restore
        returns {} or {'setup':..., 'value':...}'''
        result = []
        if self._checkBox and not self._checkBox.isChecked():
            return {}
        for child in self.children():
            result.append({})
            if isinstance(child, QRadioButton):
                result[-1]['value'] = child.isChecked()
            # elif isinstance(child, QComboBox):
            #     result.append({})
            #     result[-1]['value'] = obj.currentIndex()
            elif isinstance(child, QLineEdit):
                result[-1]['value'] = child.text()
        
        return {'setup':result, 'value': self.getInput('value')}
    
    def restoreInputSetup(self, info):
        '''restore the setup and value for input restore
        info(dict): {} or {'setup':..., 'value':...}'''
        if not info:
            return
        setup = info['setup']
        value = info['value']
        self.setCheck(True)
        for i, child in enumerate(self.children()):
            if isinstance(child, QRadioButton) and setup[i]['value']:
                child.setChecked(setup[i]['value'])
            # elif isinstance(child, QComboBox):
            #     child.setCurrentIndex(setup[i]['value'])
            elif isinstance(child, QLineEdit):
                child.setText(setup[i]['value'])
                self.lineEditChanged(child)
        self.setCheck(True)
        self.setInput('value', value)
        self.setInput('valid', True)
    
    def isInputValid(self):
        return self.getInput('valid') or not self.isEnabled()
    
    # ==========================
    # Getter and Setter
    # ==========================
    def setCheck(self, val):
        '''if the frame has an outer checkbox, set its check status, val(boolean)'''
        if self._checkBox:
            self._checkBox.setChecked(val)
            
    def setCheckBox(self, box):
        '''set the outer checkbox of this frame. box(QCheckBox)'''
        self._checkBox = box
            
    def getInput(self, key):
        return self._inputInfo[key]
    
    def setInput(self, key, val):
        self._inputInfo[key] = val
    
#Supper class of Dialog Widget
class BaseDialogWidget(ActionDlgWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.actionDict = {}
        self.ui = ActionDlgUI()
        self.ui.setupUi(self)
        self.connectEvents()
        self.rParamWidgets = {}
        self.oParamWidgets = {}
        self.outPut = {'action': '', 'rParam': {}, 'oParam':{}}
        
    def connectEvents(self):
        actionCB = self.ui.actionCB
        actionCB.activated.connect(self.selectAction)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        
    # ==========================
    # Signal Handlers
    # ==========================
    def accept(self):
        if self.checkInputValid():
            self.parent().setNextAction(self.outPut)
            super().accept()
        else:
            pass
        
    def selectAction(self, idx):
        '''handler that deals with selected action of action combo box
        idx(int): the index of selected action'''
        text = self.ui.actionCB.itemText(idx)
        self.clearParams()
        
        for key, param in self.actionDict[text]['rParam'].items():
            self.addRequiredParam(key, param)
            
        for key, param in self.actionDict[text]['oParam'].items():
            self.addOptionalParam(key, param)
            
    # ==========================
    # Validity
    # ==========================
    def checkInputValid(self):
        '''check the validity of input and store the out put if valid'''
        if self.ui.actionCB.currentIndex() == 0:
            self.clearResultAndShowError("You haven't choose an action!")
            return False
        actionText = self.ui.actionCB.currentText()
        rParams = self.actionDict[actionText]['rParam'].keys()
        rParamDict = {}
        rWidgetSetups = {}
        for key in rParams:
            widget = self.rParamWidgets[key]
            if not widget.isInputValid():
                self.clearResultAndShowError('Missing input for ' + widget.getInput('term'))
                return False
            if not self.readInput(widget, rParamDict):
                return False
            rWidgetSetups[key] = widget.getInputSetup()
            
        oParamDict = {}
        oWidgetSetups = {}
        oParams = self.actionDict[actionText]['oParam'].keys()
        for key in oParams:
            widget = self.oParamWidgets[key]
            if not widget.isInputValid():
                self.clearResultAndShowError('Missing input for ' + widget.getInput('term'))
                return False
            if widget.isEnabled() and not self.readInput(widget, oParamDict):
                return False
            oWidgetSetups[key] = widget.getInputSetup()
            
        self.outPut['action'] = actionText
        self.outPut['rParam'] = rParamDict   
        self.outPut['oParam'] = oParamDict
        self.outPut['rWidgetSetups'] = rWidgetSetups
        self.outPut['oWidgetSetups'] = oWidgetSetups
        
        for key, val in self.outPut.items():
            print(key + ': ', val)
        return True
    
    def readInput(self, widget, paramDict):
        '''Convert the input of a dialog frame to value and store in paramDict.
        widget(MngDialogFrame), paramDict(Dict)'''
        try:
            typeFunc = widget.getInput('type')
            paramDict[widget.getInput('key')] = typeFunc(widget.getInput('value'))
            return True
        except:
            text = 'Cannot convert ' + str(widget.getInput('value')) + ' to ' + typeFunc.__name__
            self.clearResultAndShowError(text)
            return False
    
    def clearResultAndShowError(self, text):
        self.outPut = {'action': '', 'rParam': {}, 'oParam':{}}
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    # ==========================
    # MngDialogFrame Methods
    # ==========================
    def clearParams(self):
        '''delect MngDialogFrames and clear self.rParamWidgets and self.oParamWidgets'''
        for widget in self.rParamWidgets.values():
            widget.deleteLater()
        for widget in self.oParamWidgets.values():
            widget.parent().deleteLater()
        self.rParamWidgets = {}
        self.oParamWidgets = {}
        
    def restoreDialog(self, action):
        '''given the action details, restore dialog.
        action(Dict): this must be a valid output created by self.checkInputValid'''
        choiceIdx = list(self.actionDict.keys()).index(action["action"])
        self.ui.actionCB.setCurrentIndex(choiceIdx)
        self.selectAction(choiceIdx)
        for key, info in action['rWidgetSetups'].items():
            self.rParamWidgets[key].restoreInputSetup(info)
            
        for key, info in action['oWidgetSetups'].items():
            self.oParamWidgets[key].restoreInputSetup(info)
            
    def addRequiredParam(self, key, param):
        '''key(str), param(dict)'''
        box = self.ui.rParamBox
        
        frame = MngDialogFrame(box, key, param)
        frame.setToolTip(param['desc'])
        QHBoxLayout(frame)
        box.layout().addWidget(frame)
        self.rParamWidgets[key] = frame
        
        label = QLabel(frame)
        label.setStyleSheet("font-weight: bold")
        label.setText(param['term']+ ': ')
        frame.layout().addWidget(label)

        self.addLineEditWidget(frame, param.get('Text'))
        self.addOptions(frame, param.get('option', {}))
    
    def addOptionalParam(self, key, param):
        '''key(str), param(dict)'''
        box = self.ui.oParamBox
        frame = QFrame(box)
        frame.setToolTip(param['desc'])
        QHBoxLayout(frame)
        box.layout().addWidget(frame)
        
        checkBox = QCheckBox(frame)
        checkBox.setStyleSheet("font-weight: bold")
        checkBox.setText(param['term'] + ': ')
        frame.layout().addWidget(checkBox)
        
        innerFrm = MngDialogFrame(frame, key, param)
        innerFrm.setCheckBox(checkBox)
        QHBoxLayout(innerFrm)
        innerFrm.layout().setContentsMargins(0, 0, 0, 0)
        self.oParamWidgets[key] = innerFrm
        frame.layout().addWidget(innerFrm)
        
        self.addLineEditWidget(innerFrm, param.get('Text'))
        self.addOptions(innerFrm, param.get('option', {}))
        
        checkBox.stateChanged.connect(lambda: innerFrm.setDisabled(not checkBox.isChecked()))        
        innerFrm.setDisabled(True)

    def addLineEditWidget(self, frame, validator):
        '''frame(MngDialogFrame), validator(QValidator)'''
        if validator:
            lineEdit = QLineEdit(frame)
            frame.layout().addWidget(lineEdit)
            lineEdit.textEdited.connect(lambda: frame.lineEditChanged(lineEdit))
            if validator != True:
                lineEdit.setValidator(validator)
            return lineEdit

    def addOptions(self, frame, options):
        '''frame(MngDialogFrame), options(Dict)'''
        buttons = []
        for key, val in options.items():
            button = QRadioButton(frame)
            frame.layout().addWidget(button)
            button.setText(key)
            buttons.append(button)
            if key == 'Text':
                lineEdit = self.addLineEditWidget(frame, val)
                button.toggled.connect(lambda isChecked, wgt = lineEdit: frame.lineEditButtonToggle(isChecked, wgt))
                lineEdit.setDisabled(True)
            else:
                button.toggled.connect(lambda isChecked, val = val: frame.buttonToggle(isChecked, val))

class MngDialogWidget(BaseDialogWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.actionDict = MNGACTIONDICT
        self.ui.actionCB.addItems(self.actionDict.keys())

class PlotDialogWidget(BaseDialogWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.actionDict = PLOTACTIONDICT
        self.ui.actionCB.addItems(self.actionDict.keys())

class BaseListWidget(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.DialogWidget = None
        self._nextAction = None
        self.connectEvents()
        
    def connectEvents(self):
        self.itemDoubleClicked.connect(self.newActionWindow)
        
    # ==========================
    # Signal Handlers
    # ==========================
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
            menu = QMenu()
            insertAct = QAction("insert")
            insertAct.triggered.connect(lambda: self.insertNewEvent(target))
            editAct = QAction("edit")
            editAct.triggered.connect(lambda: self.editExistingEvent(self.currentItem()))
            deleteAct = QAction("delete")
            deleteAct.triggered.connect(lambda: self.deleteExistingEvent(self.currentItem()))
            cancelAct = QAction("cancel")
            
            if target:
                self.setCurrentItem(target)
            if not target or not target.statusTip():
                editAct.setDisabled(True)
                deleteAct.setDisabled(True)
            
            menu.addAction(insertAct)
            menu.addAction(editAct)
            menu.addAction(editAct)
            menu.addAction(deleteAct)
            menu.exec_(ev.globalPos())
        else:
            super().mousePressEvent(ev)
            
    def newActionWindow(self, ev):
        '''create a new action window newActionWindow'''
        print('pop up window')
    
    def editExistingEvent(self, target):
        dlg = self.DialogWidget(self)
        dlg.setWindowTitle("Setup New Action")
        actionString = target.statusTip()
        dlg.restoreDialog(eval(actionString))
        button = dlg.exec()
        if button:
            text = self.actionToText(self.nextAction())
            target.setText(text)
            target.setStatusTip(repr(self.nextAction()))
            self.setNextAction(None)
            
    def insertNewEvent(self, target):
        idx = self.row(target)
        dlg = self.DialogWidget(self)
        dlg.setWindowTitle("Setup New Action")
        button = dlg.exec()
        if button:
            while idx > 0 and self.item(idx - 1).text() == '':
                idx-= 1
            self.insertItem(idx, '')
            item = self.item(idx)
            text = self.actionToText(self.nextAction())
            item.setText(text)
            item.setStatusTip(repr(self.nextAction()))
            #item.dataDialog = dlg
            self.setNextAction(None)

    def deleteExistingEvent(self, target):
        self.takeItem(self.row(target))
    # ==========================
    # Action Methods
    # ==========================
    def actionToText(self, action):
        text = action['action']
        if action['rParam']:
            text += ' || ' + str(action['rParam'])[1:-1]
        if action['oParam']:
            text += ' || ' +str(action['oParam'])[1:-1]
        text = text.replace("'", "")
        return text
    
    def resetActions(self):
        for row in range(self.count()-1, -1, -1):
            if self.item(row).text() != '':
                self.takeItem(row)

    def nextAction(self):
        return self._nextAction
    
    def setNextAction(self, action):
        self._nextAction = action

class MngListWidget(BaseListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.DialogWidget = MngDialogWidget

class PlotListWidget(BaseListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.DialogWidget = PlotDialogWidget
        
MngTabUI, MngTabWindow = uic.loadUiType("UI/mngTab.ui")
class MngTabWidget(MngTabWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self._dataManager = None
        self._infoData = {'raw': [],
                'data': [],
                'variables' : {},
                'plotData' : {}}
        self._infoWindows = {}
        self.ui = MngTabUI()
        self.ui.setupUi(self)
        self.connectEvents()
    
    def actList(self):
        return self.ui.actionList
    
    def dataManager(self):
        return self._dataManager
    
    def connectEvents(self):
        self.ui.compileBtn.clicked.connect(self.compileActions)
        self.ui.resetBtn.clicked.connect(self.actList().resetActions)
        self.ui.dataFileBtn.clicked.connect(self.selectDataFile)
        self.ui.loadBtn.clicked.connect(self.openMethod)
        self.ui.saveBtn.clicked.connect(self.saveMethod)
        
    def selectDataFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            mngTabs = self.parent().parent()
            self._dataManager = DataManager(fileName)
            mngTabs.setTabText(mngTabs.currentIndex(), self._dataManager.docInfo('name'))
            self.updataInfoWindows()
            for key, val in self._infoData.items():
                print(key, val)
            
    def setInfoWindows(self, rawDataInfoList, dataInfoTable, varInfoTable, plotDataInfoTable):
        self._infoWindows['raw'] = rawDataInfoList
        self._infoWindows['data'] = dataInfoTable
        self._infoWindows['variables'] = varInfoTable
        self._infoWindows['plotData'] = plotDataInfoTable
        
    def updataInfoWindows(self):
        self._infoData = self._dataManager.createInfoData()
        rawDataWindow = self._infoWindows['raw']
        dataWindow = self._infoWindows['data']
        variableWindow = self._infoWindows['variables']
        plotDataWindow = self._infoWindows['plotData']
        for window in self._infoWindows.values():
            window.clear()
        if self._infoData['raw']:
            rawDataWindow.addItems(self._infoData['raw'])
            rawDataWindow.scrollToItem(rawDataWindow.item(0))
        if self._infoData['data']:
            dataWindow.setColumnCount(len(self._infoData['data'][0]))
            dataWindow.setHorizontalHeaderLabels(self._infoData['data'][0])
            for y in range(1, len(self._infoData['data'])):
                if dataWindow.rowCount() <= y:
                    dataWindow.insertRow(dataWindow.rowCount())
                for x in range(len(self._infoData['data'][0])):
                    print(self._infoData['data'][y][x])
                    item = QTableWidgetItem(str(self._infoData['data'][y][x]))   # create a new Item
                    dataWindow.setItem(y-1, x, item)
        if self._infoData['variables']:
            i = 0
            variableWindow.setHorizontalHeaderLabels(['key', 'value'])
            for key, val in self._infoData['variables'].items():
                if variableWindow.rowCount() <= i:
                    variableWindow.insertRow(variableWindow.rowCount())
                variableWindow.setItem(i, 0, QTableWidgetItem(key))
                variableWindow.setItem(i, 1, QTableWidgetItem(str(val)))
                i+=1
        if self._infoData['plotData']:
            plotDataWindow.setColumnCount(len(self._infoData['plotData'].keys()))
            plotDataWindow.setHorizontalHeaderLabels(list(self._infoData['plotData'].keys()))
            for x, data in enumerate(self._infoData['plotData'].values()):
                for y, val in enumerate(data):
                    if plotDataWindow.rowCount() <= y:
                        plotDataWindow.insertRow(plotDataWindow.rowCount())
                    plotDataWindow.setItem(y, x, QTableWidgetItem(str(val)))
                
    def compileActions(self):
        if not self._dataManager:
            return
        for x in range(self.actList().count()-1):
            action = self.actList().item(x).statusTip()
            if not action:
                continue
            self.excecuteAction(eval(action))
        self.updataInfoWindows()
    
    def excecuteAction(self,action):
        func = MNGACTIONDICT[action['action']]['func']
        print(action)
        rparam = action['rParam'].values()
        oparam = action['oParam']
        method = getattr(self._dataManager, func)
        method(*rparam, **oparam)
    
    def saveMethod(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "method.txt","Method Files (*.txt);;All Files (*)", options=options)
        if fileName:
            actions = self.methodToString()
            if not actions:
                return
            file = open(fileName,'w')
            file.write(actions)
            file.close()
            
    def methodToString(self):
        actions = '['
        for x in range(self.actList().count()-1):
            action = self.actList().item(x).statusTip()
            if not action:
                continue
            actions += action + ',\n'
        if actions == '[':
            return False
        return actions[:-2] + ']'
            
    def openMethod(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Method Files (*.txt);;All Files (*)", options=options)
        if fileName:
            try:
                text = open(fileName,'r').read()
                actions = eval(text)
                self.restoreActions(actions)
            except:
                print('error')
                return
            
    def restoreActions(self, actions):
        self.actList().resetActions()
        for i, action in enumerate(actions):
            self.actList().insertItem(i, self.actList().actionToText(action))
            item = self.actList().item(i)
            item.setStatusTip(repr(action))

PlotTabUI, PlotTabWindow = uic.loadUiType("UI/plotTab.ui")
class PlotTabWidget(PlotTabWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = PlotTabUI()
        self.ui.setupUi(self)
        self.connectEvents()
        self.plotter = None
        self.mngTabs = None
        self.canvas = None
    
    def actList(self):
        return self.ui.actionList
    
    def connectEvents(self):
        self.ui.resetBtn.clicked.connect(self.actList().resetActions)
                
    def compileActions(self):
        self.plotter.resetFig(True)
        self.initDataManagers()
        for x in range(self.actList().count()-1):
            action = self.actList().item(x).statusTip()
            if not action:
                continue
            self.excecuteAction(eval(action))
    
    def initDataManagers(self):
        dataManagers = []
        for mngTab in [self.mngTabs.widget(count) for count in range(self.mngTabs.count())]:
            if isinstance(mngTab, MngTabWidget):
                mngTab.compileActions()
                dataManagers.append(mngTab.dataManager())
            else:
                dataManagers.append(None)
        self.plotter.setDataManager(dataManagers)
    
    def excecuteAction(self,action):
        func = PLOTACTIONDICT[action['action']]['func']
        rparam = action['rParam'].values()
        oparam = action['oParam']
        method = getattr(self.plotter, func)
        method(*rparam, **oparam)
    
    def saveMethod(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "method.txt","Method Files (*.txt);;All Files (*)", options=options)
        if fileName:
            actions = self.methodToString()
            if not actions:
                return
            file = open(fileName,'w')
            file.write(actions)
            file.close()
            
    def methodToString(self):
        actions = '['
        for x in range(self.actList().count()-1):
            action = self.actList().item(x).statusTip()
            if not action:
                continue
            actions += action + ',\n'
        if actions == '[':
            return False
        return actions[:-2] + ']'
        
    def openMethod(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Method Files (*.txt);;All Files (*)", options=options)
        if fileName:
            try:
                text = open(fileName,'r').read()
                actions = eval(text)
                self.restoreActions(actions)
            except:
                print('error')
                return
            
    def restoreActions(self, actions):
        self.actList().resetActions()
        for i, action in enumerate(actions):
            self.actList().insertItem(i, self.actList().actionToText(action))
            item = self.actList().item(i)
            item.setStatusTip(repr(action))