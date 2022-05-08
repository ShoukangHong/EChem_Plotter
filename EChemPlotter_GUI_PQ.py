# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 09:27:30 2022

@author: shouk
"""
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
# from qgis.gui import QgsMapCanvas
import Plotter_Core
from PyQt5 import uic, QtCore
from PlotterWidgets import MngTabWidget, PlotTabWidget, FormatDialog

PLOTTER = Plotter_Core.EchemPlotter()
BaseUI, Window = uic.loadUiType("UI/mainWindow.ui")
BaseMngTabUI, MngTab = uic.loadUiType("UI/mngTab.ui")
_oldFunc = BaseUI.retranslateUi

ROOT = INFOTABS = MNGTABS = PLTLIST = CANVAS = None
CONFIG = {'imageFormatDir': 'ImageFormat.txt', 'imageFormat':None, 'canvasMH':400, 'canvasMW':600}
DEFALTIMAGEFORMAT={
    'format': '.tif',
    'compression':'LZW',
    'resolution': 600,
    'height':6,
    'width': 8}

class Ui_MainWindow(BaseUI):
    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        mainWindow.ui = self
        self.connectEvents(mainWindow)
        self.setGlobals()
        
    def retranslateUi(self, mainWindow):
        self.subjectWindow = mainWindow
        self.canvas.deleteLater()
        fig, ax = PLOTTER.newFigure(1, 1, True)
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setObjectName("canvas")
        self.toolbar = NavigationToolbar2QT(self.canvas, mainWindow)
        self.verticalLayout_4.addWidget(self.toolbar)
        self.verticalLayout_4.addWidget(self.canvas)
        self.plotLogo()
        self.loadImageFormat()
        self.addInitialWidgets(mainWindow)
        super().retranslateUi(mainWindow)


    def setGlobals(self):
        global ROOT, INFOTABS, MNGTABS, PLTLIST, CANVAS
        ROOT = self
        INFOTABS = self.infoTabs
        MNGTABS = self.mngTabs
        PLTLIST = self.plotActionWidget
        CANVAS = self.canvas
    
    def addInitialWidgets(self, mainWindow):
        commandTab = QWidget()
        self.mngTabs.addTab(commandTab, "+")
        self.mngTabs.tabBarDoubleClicked.connect(self.onTabDoubleClick)
        self.onTabDoubleClick()
        self.plotActionWidget = PlotTabWidget(self.pltTabs)
        self.pltTabs.insertTab(0, self.plotActionWidget, 'Plot Method')
        self.plotActionWidget.plotter = PLOTTER
        self.plotActionWidget.ui.plotBtn.clicked.connect(self.plot)
        self.plotActionWidget.mngTabs = self.mngTabs
        self.plotActionWidget.canvas = self.canvas
        
    # def addMngTabWidget(self, mainWindow):
    #     newTab = MngTabWidget(self.mngTabs)
    #     self.mngTabs.addTab(newTab, "new Tab")
    #     newTab.setInfoWindows(self.rawDataInfoList,
    #                           self.dataInfoTable,
    #                           self.varInfoTable,
    #                           self.plotDataInfoTable)
    
    def connectEvents(self, mainWindow):
        self.mngTabs.currentChanged.connect(self.onTabChanged)
        self.runAndPlotPB.clicked.connect(self.runAndPlot)
        self.plotLoadPB.clicked.connect(self.openPlotMethod)
        self.plotSavePB.clicked.connect(self.savePlotMethod)
        self.menuSaveTemplate.triggered.connect(self.saveTemplate)
        self.menuLoadTemplate.triggered.connect(self.loadTemplate)
        self.menuLoadDataMethod.triggered.connect(self.loadDataMethodToAll)
        self.meunBatchProcess.triggered.connect(self.batchProcess)
        self.menuImageFormat.triggered.connect(self.imageFormatDialog)
        self.saveImagePB.clicked.connect(self.saveImage)
    
    def onTabChanged(self):
        if self.mngTabs.count()-1 == self.mngTabs.currentIndex():
            pass
        elif self.mngTabs.currentWidget()._dataManager:
            self.mngTabs.currentWidget().updataInfoWindows()
            
    def onTabDoubleClick(self):
        if self.mngTabs.count()-1 == self.mngTabs.currentIndex():
            newTab = self.createNewTab()
            self.mngTabs.insertTab(self.mngTabs.count()-1, newTab, "new Manager")
            self.mngTabs.setCurrentWidget(newTab)
        else:
            self.mngTabs.removeTab(self.mngTabs.currentIndex())
    
    def createNewTab(self):
        newTab = MngTabWidget(self.mngTabs)
        newTab.setInfoWindows(self.rawDataInfoList, self.dataInfoTable,
                              self.varInfoTable, self.plotDataInfoTable)
        return newTab
    
    def batchProcess(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self.subjectWindow,"QFileDialog.getOpenFileName()", "",
                                                  "Data Files (*.txt *.csv *.mpt *.xlsx *.xlsm *.xls);;All Files (*)", options=options)
        if fileNames:
            for fileName in fileNames:
                self.mngTabs.currentWidget().selectDataFile(fileName = fileName)
                self.runAndPlot()
                dataManager = self.mngTabs.currentWidget().dataManager()
                direct = dataManager.docInfo('path') + dataManager.docInfo('name') + CONFIG['imageFormat']['format']
                PLOTTER.figure().set_size_inches(CONFIG['imageFormat']['width'], CONFIG['imageFormat']['height'])
                PLOTTER.pyplot().savefig(direct, dpi=CONFIG['imageFormat']['resolution'])
                
                    
    def loadDataMethodToAll(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.subjectWindow,"QFileDialog.getOpenFileName()", "","Method Files (*.txt);;All Files (*)", options=options) 
        for mngTab in [self.mngTabs.widget(count) for count in range(self.mngTabs.count())]:
            if isinstance(mngTab, MngTabWidget):
                mngTab.openMethod(fileName = fileName)
            
    def openDataMethod(self):
        if isinstance(self.mngTabs.currentWidget(), MngTabWidget):
            self.mngTabs.currentWidget().openMethod()
            
    def saveDataMethod(self):
        if isinstance(self.mngTabs.currentWidget(), MngTabWidget):
            self.mngTabs.currentWidget().saveMethod()

    def openPlotMethod(self):
        if isinstance(self.mngTabs.currentWidget(), MngTabWidget):
            self.plotActionWidget.openMethod()
            
    def savePlotMethod(self):
        if isinstance(self.mngTabs.currentWidget(), MngTabWidget):
            self.plotActionWidget.saveMethod()

    def loadTemplate(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.subjectWindow,"QFileDialog.getOpenFileName()", "","Method Files (*.tmp);;All Files (*)", options=options)
        if fileName:
            try:
                text = open(fileName,'r').read()
                template = eval(text)
                for i, dataMethod in enumerate(template['DataMethods']):
                    if self.mngTabs.count() <= i+1:
                        newTab = self.createNewTab()
                        self.mngTabs.insertTab(self.mngTabs.count()-1, newTab, "new Manager")
                    self.mngTabs.widget(i).restoreActions(dataMethod)
                if template['plotMethod']:
                    self.plotActionWidget.restoreActions(template['plotMethod'])
            except Exception as e:
                text = 'Failed to Load Template: \n' + str(e)
                self.showError(text)
                
    def saveTemplate(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.subjectWindow,"QFileDialog.getSaveFileName()", "template.tmp","Template Files (*.tmp)", options=options)
        if fileName:
            template = "{'DataMethods':["
            for mngTab in [self.mngTabs.widget(count) for count in range(self.mngTabs.count())]:
                if isinstance(mngTab, MngTabWidget):
                    action = mngTab.methodToString()
                    if action:
                        template += action + ',\n'
            if template == "{'DataMethods':[":
                template += '],\n'
            else:
                template = template[:-2] + '],\n'
            template += "'plotMethod':"
            
            if self.plotActionWidget.methodToString():
                template += self.plotActionWidget.methodToString() + '}'
            else:
                template += 'False' + '}'
            file = open(fileName,'w')
            file.write(template)
            file.close()       

    def runAndPlot(self):
        try:
            self.plotActionWidget.runDataManagers()
            self.plotActionWidget.runActions()
        except Exception as e:
            text = 'Failed to Plot: \n' + str(e)
            self.showError(text)
            PLOTTER.newFigure(1, 1, True)
            self.plotLogo()
        self.refreshCanvas()
         
    def plot(self):
        try:
            self.plotActionWidget.runActions()
        except Exception as e:
            text = 'Failed to Plot: \n' + str(e)
            self.showError(text)
            PLOTTER.newFigure(1, 1, True)
            self.plotLogo()
        self.refreshCanvas()
    
    def refreshCanvas(self):
        self.canvas.deleteLater()
        self.toolbar.deleteLater()
        self.canvas = FigureCanvasQTAgg(PLOTTER.figure())
        self.canvas.setObjectName("canvas")
        self.toolbar = NavigationToolbar2QT(self.canvas, self.subjectWindow)
        self.verticalLayout_4.addWidget(self.toolbar)
        self.verticalLayout_4.addWidget(self.canvas)
        self.resizeCanvas()
        self.canvas.draw()
    
    def saveImage(self, fileName = None):
        if not fileName:
            direct = ''
            options = QFileDialog.Options()
            if isinstance(self.mngTabs.currentWidget(), MngTabWidget) and self.mngTabs.currentWidget().dataManager():
                direct = self.mngTabs.currentWidget().dataManager().docInfo('path') + self.mngTabs.currentWidget().dataManager().docInfo('name') + CONFIG['imageFormat']['format']
            fileName, _ = QFileDialog.getSaveFileName(self.subjectWindow,"QFileDialog.getSaveFileName()", direct,
                                                      "Images (*.tif *.tiff *.png *.jpg);;All Files (*)", options=options)
        if fileName:
            PLOTTER.figure().set_size_inches(CONFIG['imageFormat']['width'], CONFIG['imageFormat']['height'])
            PLOTTER.pyplot().savefig(fileName, dpi=CONFIG['imageFormat']['resolution'])
# setattr(BaseUI, 'retranslateUi', retranslateUi)
    def imageFormatDialog(self):
        dlg = FormatDialog(self.subjectWindow, CONFIG['imageFormat'])
        dlg.setWindowTitle("Image Format")
        button = dlg.exec()
        if button:
            dlg.saveFormat()

    def loadImageFormat(self):
        text = open(CONFIG['imageFormatDir'],'r').read()
        try:
            CONFIG['imageFormat'] = eval(text)
            if not isinstance(CONFIG['imageFormat'], dict):
               self.resetImageFormat()
            else:
                self.refreshCanvas()
        except Exception as e:
            text = 'Failed to Load image format, image format reset to default: \n' + str(e)
            self.showError(text)
            self.resetImageFormat()
    
    def resetImageFormat(self):
        CONFIG['imageFormat'] = DEFALTIMAGEFORMAT
        self.resizeCanvas()
    
    def setImageFormat(self, imageFormat):
        CONFIG['imageFormat'] = imageFormat
        file = open(CONFIG['imageFormatDir'],'w')
        file.write(str(imageFormat))
        file.close()
        self.resizeCanvas()
    
    def resizeCanvas(self):
        height = self.pltTabs.height()
        width = self.infoTabs.width()
        if height < 40 or width<60:
            height = 364
            width = 556
        currentRatio = self.canvas.height()/self.canvas.width()
        requiredRatio = CONFIG['imageFormat']['height']/CONFIG['imageFormat']['width']
        if requiredRatio>currentRatio:
            self.canvas.setFixedSize(int(height/requiredRatio), height)
        elif requiredRatio<currentRatio:
            self.canvas.setFixedSize(width, int(width*requiredRatio))

    def showError(self, text):
        msg = QMessageBox(self.subjectWindow)
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def plotLogo(self):
        plt = PLOTTER.pyplot()
        echem = {'E':[[6,6,6,6,6,7,8,7,8,7,8],[13,12,11,10,9,13,13,11,11,9,9]],
              'C':[[10,10,10,10,10,11,12,11,12],[13,12,11,10,9,13,13,9,9]],
              'H':[[14,14,14,14,14,15,16,16,16,16,16],[13,12,11,10,9,11,13,12,11,10,9]],
              'E2':[[18,18,18,18,18,19,20,19,20,19,20],[13,12,11,10,9,13,13,11,11,9,9]],
              'M':[[22,22,22,22,22,22.33,22.67,23,23.33,23.67,24,24,24,24,24],[13,12,11,10,9,12,11,10,11,12,13,12,11,10,9]]}
        
        plotter = {'P':[[2,2,2,2,2,3,4,4,4,3], [6,5,4,3,2,6,6,5,4,4]],
              'L': [[6,6,6,6,6,7,8],[6,5,4,3,2,2,2]],
              'O': [[10,10,10,10,10,11,12,12,12,12,12,11],[6,5,4,3,2,2,2,3,4,5,6,6]],
              'T': [[14,15,16,15,15,15,15],[6,6,6,5,4,3,2]],
              'T2': [[18,19,20,19,19,19,19],[6,6,6,5,4,3,2]],
              'E3': [[22,22,22,22,22,23,24,23,24,23,24],[6,5,4,3,2,6,6,4,4,2,2]],
              'R': [[26,26,26,26,26,27,28,28,28,27,27,28],[6,5,4,3,2,6,6,5,4,4,3,2]]}
        echemX =[]
        echemY = []
        for val in echem.values():
            echemX += val[0]
        for val in echem.values():
            echemY += val[1]
        plotterX =[]
        plotterY = []
        for val in plotter.values():
            plotterX += val[0]
        for val in plotter.values():
            plotterY += val[1]
        plt.plot([7.5 + val for val in echemX], [7.5 + val for val in echemY], 'b*', markersize=7)
        plt.plot([7.5 + val for val in plotterX], [7.5 + val for val in plotterY], 'rD')
        plt.xlim([0, 45])
        plt.ylim([0, 30])
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("{}")
    mwindow = Window()
    ui = Ui_MainWindow()
    ui.setupUi(mwindow)
    mwindow.show()
    app.exec_()
# print(1)
# [print(key+ ': ' + str(val)) for key, val in ui.__dict__.items()]
# print(2)
# [print(key+ ': ' + str(val)) for key, val in ui.infoGB.__dict__.items()]
        # if CONFIG['imageFormat']['format'] == '.tif' or CONFIG['imageFormat']['format'] == '.tiff':
        #     if CONFIG['imageFormat']['compression'] == 'LZW':
        #         compression = CONFIG['imageFormat']['format'][1:] + '_' + 'lzw'
        #         compression_kwargs={"compression": compression}
        #         print(compression)
        #     elif CONFIG['imageFormat']['compression'] == 'ZIP':
        #         compression = CONFIG['imageFormat']['format'][1:] + '_' + 'zip'
        #         compression_kwargs={"compression": compression}