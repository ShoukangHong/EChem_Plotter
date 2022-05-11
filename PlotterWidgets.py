# -*- coding: utf-8 -*-
"""
@author: shouk
"""
from PyQt5.QtWidgets import (QWidget, QListWidget, QMenu, QAction, QMessageBox, QFrame,
    QLabel, QHBoxLayout, QRadioButton, QTableWidgetItem, QCheckBox, QLineEdit, QFileDialog)
from PyQt5 import uic, QtCore
from MngOptions import MNGACTIONDICT
from PlotOptions import PLOTACTIONDICT
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QColor
from Plotter_Core import DataManager
MainUI, MainWindow = uic.loadUiType("UI/mainWindow.ui")
ActionDlgUI, ActionDlgWindow = uic.loadUiType("UI/actionDialog.ui")

CLIPBOARD = []

class MngDialogFrame(QFrame):
    '''data manager dialog frame Class,'''
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
            elif isinstance(child, QLineEdit):
                child.setText(setup[i]['value'])
                self.lineEditChanged(child)
        self.setCheck(True)
        self.setInput('value', value)
        self.setInput('valid', True)
    
    def isInputValid(self):
        return self.getInput('valid') or not self.isEnabled()

    def getInput(self, key):
        return self._inputInfo[key]
    
    def setInput(self, key, val):
        self._inputInfo[key] = val

    def setCheck(self, val):
        '''if the frame has an outer checkbox, set its check status, val(boolean)'''
        if self._checkBox:
            self._checkBox.setChecked(val)
            
    def setCheckBox(self, box):
        '''set the outer checkbox of this frame. box(QCheckBox)'''
        self._checkBox = box

# ==========================
# Dialog Class
# ==========================
FormatDlgUI, FormatDlgWindow = uic.loadUiType("UI/formatDialog.ui")
class FormatDialog(FormatDlgWindow):
    '''image format dialog class'''
    def __init__(self, parent, imageFormat):
        super().__init__(parent)
        self.ui = FormatDlgUI()
        self.ui.setupUi(self)
        self.setupvalidator()
        self.connectEvents()
        self.loadFormat(imageFormat)
    
    def setupvalidator(self):
        self.ui.heightLE.setValidator(QDoubleValidator(1, 100, 2))
        self.ui.widthLE.setValidator(QDoubleValidator(1, 100, 2))
        self.ui.resolutionLE.setValidator(QIntValidator(10, 9999))
    
    def connectEvents(self):
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        
    def accepted(self):
        self.saveFormat()
        super().accepted()

    def loadFormat(self, imageFormat):
        self.ui.formatCB.setCurrentText(imageFormat['format'])
        self.ui.compressionCB.setCurrentText(imageFormat['compression'])
        self.ui.resolutionLE.setText(str(imageFormat['resolution']))
        self.ui.heightLE.setText(str(imageFormat['height']))
        self.ui.widthLE.setText(str(imageFormat['width']))

    def saveFormat(self):
        imageFormat = {}
        imageFormat['format'] = self.ui.formatCB.currentText()
        imageFormat['compression'] = self.ui.compressionCB.currentText()
        imageFormat['resolution'] = int(self.ui.resolutionLE.text())
        imageFormat['height'] = float(self.ui.heightLE.text())
        imageFormat['width'] = float(self.ui.widthLE.text())
        self.parent().ui.setImageFormat(imageFormat)


SelectPageDlgUI, SelectPageDlgWindow = uic.loadUiType("UI/selectPageDialog.ui")
class SelectPageDialog(SelectPageDlgWindow):
    '''image format dialog class'''
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = SelectPageDlgUI()
        self.ui.setupUi(self)
        self.connectEvents()
    
    def connectEvents(self):
        self.ui.buttonBox.accepted.connect(self.accept)
        
    def accept(self):
        self.parent().sheetIndex = int(self.ui.pageSB.text())
        super().accept()

class BaseDialogWidget(ActionDlgWindow):
    '''Base class of plotter/dataManager Dialog Widgets'''
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
        
    def selectAction(self, idx):
        '''handler that deals with selected action of action combo box
        idx(int): the index of selected action'''
        text = self.ui.actionCB.itemText(idx)
        self.clearParams()
        
        for key, param in self.actionDict[text]['rParam'].items():
            self.addRequiredParam(key, param)
            
        for key, param in self.actionDict[text]['oParam'].items():
            self.addOptionalParam(key, param)
            
    def accept(self):
        if self.checkInputValid():
            self.parent().setNextAction(self.outPut)
            super().accept()
            
    # ==========================
    # Input Validity Check
    # ==========================
    def checkInputValid(self):
        '''check the validity of input and store the out put if valid'''
        if self.ui.actionCB.currentIndex() == 0:
            self.clearResultAndShowError("Please choose an action!")
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
        
        return True
    
    def readInput(self, widget, paramDict):
        '''Convert the input of a dialog frame to value and store in paramDict.
        widget(MngDialogFrame), paramDict(Dict)'''
        try:
            typeFunc = widget.getInput('type')
            paramDict[widget.getInput('key')] = typeFunc(widget.getInput('value'))
            return True
        except Exception as e:
            text = 'Cannot convert ' + str(widget.getInput('value')) + ' to ' + typeFunc.__name__
            self.clearResultAndShowError(text + '\n' + str(e))
            return False
        
    # ==========================
    # set up MngDialogFrame
    # ==========================
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
            lineEdit.setStyleSheet("font-weight: normal")
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

    # ========================
    # Other functions
    # ========================
    def clearParams(self):
        '''delect MngDialogFrames and clear self.rParamWidgets and self.oParamWidgets'''
        for widget in self.rParamWidgets.values():
            widget.deleteLater()
        for widget in self.oParamWidgets.values():
            widget.parent().deleteLater()
        self.rParamWidgets = {}
        self.oParamWidgets = {}

    def clearResultAndShowError(self, text):
        self.outPut = {'action': '', 'rParam': {}, 'oParam':{}}
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



class MngDialogWidget(BaseDialogWidget):
    '''DataManager Dialog Widget Class'''
    def __init__(self, parent):
        super().__init__(parent)
        self.actionDict = MNGACTIONDICT
        self.ui.actionCB.addItems(self.actionDict.keys())



class PlotDialogWidget(BaseDialogWidget):
    '''Plotter Dialog Widget Class'''
    def __init__(self, parent):
        super().__init__(parent)
        self.actionDict = PLOTACTIONDICT
        self.ui.actionCB.addItems(self.actionDict.keys())

# ==========================
# List Widget Class
# ==========================
class BaseListWidget(QListWidget):
    '''Base class of plotter/dataManagers list Widget'''
    def __init__(self, parent):
        super().__init__(parent)
        self.DialogWidget = None
        self._nextAction = None
        self._clipboard = []
        self.connectEvents()
        
    def connectEvents(self):
        self.itemDoubleClicked.connect(self.doubleClickItem)
        
    # ==========================
    # Signal Handlers
    # ==========================
    def keyPressEvent(self, ev):
        i = self.currentRow()
        item = self.currentItem()
        if ev.key() == QtCore.Qt.Key_Delete:
            if item.text() != '':
                self.takeItem(i)
        elif ev.modifiers() and QtCore.Qt.ControlModifier and ev.key() == QtCore.Qt.Key_C:
            if item.statusTip():
                self.copyEvent(item)
        elif ev.modifiers() and QtCore.Qt.ControlModifier and ev.key() == QtCore.Qt.Key_V:
            if len(self._clipboard)>0:
                self.pasteEvent(item)
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
            copyAct = QAction("copy")
            copyAct.triggered.connect(lambda: self.copyEvent(self.currentItem()))
            pasteAct = QAction("paste")
            pasteAct.triggered.connect(lambda: self.pasteEvent(self.currentItem()))
            deleteAct = QAction("delete")
            deleteAct.triggered.connect(lambda: self.deleteExistingEvent(self.currentItem()))
            
            if target:
                self.setCurrentItem(target)
            if not target or not target.statusTip():
                editAct.setDisabled(True)
                copyAct.setDisabled(True)
                deleteAct.setDisabled(True)
            if len(self._clipboard)<=0:
                pasteAct.setDisabled(True)
            
            menu.addAction(insertAct)
            menu.addAction(editAct)
            menu.addAction(copyAct)
            menu.addAction(pasteAct)
            menu.addAction(deleteAct)
            menu.exec_(ev.globalPos())
        else:
            super().mousePressEvent(ev)
    
    def doubleClickItem(self):
        if len(self.currentItem().statusTip()) > 0:
            self.editExistingEvent(self.currentItem())
        else:
            self.insertNewEvent(self.currentItem())
    
    def editExistingEvent(self, target):
        dlg = self.DialogWidget(self)
        dlg.setWindowTitle("Setup New Action")
        actionString = target.statusTip()
        dlg.restoreDialog(eval(actionString))
        button = dlg.exec()
        if button:
            self.setActionText(target, self.nextAction())
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
            self.setActionText(self.item(idx), self.nextAction())
            #item.dataDialog = dlg
            self.setNextAction(None)

    def copyEvent(self, target):
        if len(self._clipboard) > 0:
            self._clipboard[0] = target.statusTip()
        else:
            self._clipboard.append(target.statusTip())
        
    def pasteEvent(self, target):
        if len(self._clipboard) <= 0:
            return
        idx = self.row(target)
        while idx > 0 and self.item(idx - 1).text() == '':
            idx-= 1
        self.insertItem(idx, '')
        self.setActionText(self.item(idx), eval(self._clipboard[0]))

    def deleteExistingEvent(self, target):
        self.takeItem(self.row(target))
        
    # ==========================
    # Action Methods
    # ==========================
    def setActionText(self, target, action):
        text = self.actionToText(action)
        target.setStatusTip(repr(action))
        if action['action'] == 'Note':
            target.setForeground(QColor('#0000cc'))
            target.setText(text[8:])
        else:
            target.setForeground(QColor('#000000'))
            target.setText(text)
            if action['action'] in ['Add Variable', 'Set Title']:
                target.setForeground(QColor('#cc0000'))
    
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
    '''DataManagers list Widget class'''
    def __init__(self, parent):
        super().__init__(parent)
        self._clipboard = CLIPBOARD
        self.DialogWidget = MngDialogWidget



class PlotListWidget(BaseListWidget):
    '''Plotter list Widget class'''
    def __init__(self, parent):
        super().__init__(parent)
        self.DialogWidget = PlotDialogWidget
        
# ==========================
# Tab Widget Class
# ==========================
class BaseTabWidget(QWidget):
    '''Base class of plotter/dataManager tab widgets'''
    def __init__(self, parent):
        super().__init__(parent)
        self._methodType = ''
        self._actionDict = ''
        
    def actList(self):
        return self.ui.actionList
    
    def openMethod(self, fileName = None):
        if not fileName:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"Open Method", "",
                "Method Files (*" + self._methodType + ");;All Files (*)", options=options)    
        if fileName:
            try:
                text = open(fileName,'r').read()
                actions = eval(text)
                self.restoreActions(actions)
            except Exception as e:
                self.showError('can not open method: \n' + str(e))

    def saveMethod(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save Method",
            "method" + self._methodType,"Method Files (*" + self._methodType + ")", options=options)
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
    
    def runActions(self):
        pass
    
    def excecuteAction(self):
        pass
    
    def restoreActions(self, actions):
        self.actList().resetActions()
        for i, action in enumerate(actions):
            self.actList().insertItem(i, '')
            self.actList().setActionText(self.actList().item(i), action)
            
    def showError(self, text):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



MngTabUI, MngTabWindow = uic.loadUiType("UI/mngTab.ui")
class MngTabWidget(BaseTabWidget):
    '''DataManager tab widget class'''
    def __init__(self, parent):
        super().__init__(parent)
        self._methodType = '.dmtd'
        self._dataManager = None
        self._infoData = {'raw': [],
                'data': [],
                'variables' : {},
                'plotData' : {}}
        self.sheetIndex = None
        self._infoWindows = {}
        self.ui = MngTabUI()
        self.ui.setupUi(self)
        self.connectEvents()

    def connectEvents(self):
        self.ui.runBtn.clicked.connect(self.runActions)
        self.ui.resetBtn.clicked.connect(self.actList().resetActions)
        self.ui.dataFileBtn.clicked.connect(self.selectDataFile)
        self.ui.loadBtn.clicked.connect(self.openMethod)
        self.ui.saveBtn.clicked.connect(self.saveMethod)
        
    def runActions(self):
        if not self._dataManager:
            return
        self._dataManager.clearData()
        for x in range(self.actList().count()-1):
            action = self.actList().item(x).statusTip()
            if not action:
                continue
            self.actList().setCurrentRow(x)
            try:
                self.excecuteAction(eval(action))
            except Exception as e:
                self.showError(action + '...failed!\n' + str(e))
                self.updataInfoWindows()
                return
        self.updataInfoWindows()
    
    def excecuteAction(self,action):
        dataManager = self._dataManager
        func = MNGACTIONDICT[action['action']]['func']
        if func == 'note':
            return
        elif func == 'script':
            eval(action['rParam']['script'])
        else:
            rparam = action['rParam'].values()
            oparam = action['oParam']
            method = getattr(self._dataManager, func)
            method(*rparam, **oparam)
        if (func in ['truncatePlotDataByTurn', 'truncatePlotDataByValue', 'filterPlotDataByFunc',
                       'modifyPlotDataValues', 'createPlotData', 'formatRawData']):
            print(func + ' complete!')
            
    def dataManager(self):
        return self._dataManager
        
    def selectDataFile(self, fileName = None):
        try:
            self.sheetIndex = None
            if not fileName:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                fileName, _ = QFileDialog.getOpenFileName(self,"Select Data File", "",
                                                          "Data Files (*.txt *.csv *.mpt *.xlsx *.xlsm *.xls);;All Files (*)", options=options)
            if fileName:
                fileType = '.'+fileName.split('.')[-1]
                if fileType in ['.xlsx', '.xlsm', '.xls']:
                    dlg = SelectPageDialog(self)
                    dlg.setWindowTitle("Select Excel Page")
                    button = dlg.exec()
                    if not button:
                        return
                mngTabs = self.parent().parent()
                if not self._dataManager:
                    self._dataManager = DataManager(fileName, sheet = 0 if not self.sheetIndex else self.sheetIndex)
                else:
                    self._dataManager.loadRawData(fileName, sheet = 0 if not self.sheetIndex else self.sheetIndex)
                name = self._dataManager.docInfo('name')
                if len(self._dataManager.docInfo('name'))>25:
                    name = self._dataManager.docInfo('name')[:22] + '...'
                mngTabs.setTabText(mngTabs.currentIndex(), name)
                self.updataInfoWindows()
        except Exception as e:
            self.showError('can not open data file! \n' + str(e))
            
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
        if len(self._infoData['data'])>0:
            dataWindow.setColumnCount(len(self._infoData['data'][0]))
            dataWindow.setHorizontalHeaderLabels(self._infoData['data'][0])
            for y in range(1, len(self._infoData['data'])):
                if dataWindow.rowCount() <= y:
                    dataWindow.insertRow(dataWindow.rowCount())
                for x in range(len(self._infoData['data'][0])):
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



PlotTabUI, PlotTabWindow = uic.loadUiType("UI/plotTab.ui")
class PlotTabWidget(BaseTabWidget):
    '''Plotter tab widget class'''
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = PlotTabUI()
        self.ui.setupUi(self)
        self.connectEvents()
        self._methodType = '.pmtd'
        self.plotter = None
        self.mngTabs = None
        self.canvas = None
    
    def connectEvents(self):
        self.ui.resetBtn.clicked.connect(self.actList().resetActions)
        
    def runActions(self):
        if self.actList().count() <= 0 or len(self.actList().item(0).statusTip()) <= 0:
            return
        self.plotter.resetFig(True)
        for x in range(self.actList().count()-1):
            action = self.actList().item(x).statusTip()
            if not action:
                continue
            self.actList().setCurrentRow(x)
            try:
                self.excecuteAction(eval(action))
            except Exception as e:
                self.showError(action[:50] + '... failed!\n' + str(e))
                return

    def excecuteAction(self,action):
        func = PLOTACTIONDICT[action['action']]['func']
        plotter = self.plotter
        if func == 'note':
            return
        elif func == 'script':
            eval(action['rParam']['script'])
        else:
            rparam = action['rParam'].values()
            oparam = {}
            for key, val in action['oParam'].items():
                if key == 'kwParams' and isinstance(val, dict):
                    oparam.update(val)
                else:
                    oparam[key] = val
            method = getattr(self.plotter, func)
            method(*rparam, **oparam)
        if (func in ['plot']):
            print(func + ' complete!')

    def runDataManagers(self):
        dataManagers = []
        for mngTab in [self.mngTabs.widget(count) for count in range(self.mngTabs.count())]:
            if isinstance(mngTab, MngTabWidget):
                mngTab.runActions()
                dataManagers.append(mngTab.dataManager())
            else:
                dataManagers.append(None)
        self.plotter.setDataManager(dataManagers)
    