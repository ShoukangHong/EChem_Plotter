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
from PlotterWidgets import MngTabWidget, PlotTabWidget

PLOTTER = Plotter_Core.EchemPlotter()
BaseUI, Window = uic.loadUiType("UI/mainWindow.ui")
BaseMngTabUI, MngTab = uic.loadUiType("UI/mngTab.ui")
_oldFunc = BaseUI.retranslateUi

ROOT = INFOTABS = MNGTABS = PLTLIST = CANVAS = None

class Ui_MainWindow(BaseUI):
    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        mainWindow.ui = self
        self.connectEvents(mainWindow)
        self.setGlobals()
        self.subjectWindow = mainWindow
        
    def retranslateUi(self, mainWindow):
        self.canvas.deleteLater()
        fig, ax = PLOTTER.newFigure(1, 1, True)
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setObjectName("canvas")
        self.toolbar = NavigationToolbar2QT(self.canvas, mainWindow)
        self.verticalLayout_4.addWidget(self.toolbar)
        self.verticalLayout_4.addWidget(self.canvas)
        ax.plot([0,1,2,3,4], [10,1,20,3,40])
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
        self.plotActionWidget.mngTabs = self.mngTabs
        self.plotActionWidget.canvas = self.canvas
        
    def addMngTabWidget(self, mainWindow):
        newTab = MngTabWidget(self.mngTabs)
        self.mngTabs.addTab(newTab, "new Tab")
        newTab.setInfoWindows(self.rawDataInfoList,
                              self.dataInfoTable,
                              self.varInfoTable,
                              self.plotDataInfoTable)
    
    def connectEvents(self, mainWindow):
        self.mngTabs.currentChanged.connect(self.onTabChanged)
        self.plotPB.clicked.connect(self.compileAndPlot)
        self.plotLoadPB.clicked.connect(self.openPlotMethod)
        self.plotSavePB.clicked.connect(self.savePlotMethod)
        self.menuSaveTemplate.triggered.connect(self.saveTemplate)
        self.menuLoadTemplate.triggered.connect(self.loadTemplate)
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
        newTab.setInfoWindows(self.rawDataInfoList,
                              self.dataInfoTable,
                              self.varInfoTable,
                              self.plotDataInfoTable)
        return newTab
    
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
        fileName, _ = QFileDialog.getOpenFileName(self.subjectWindow,"QFileDialog.getOpenFileName()", "","Method Files (*.txt);;All Files (*)", options=options)
        if fileName:
            try:
                text = open(fileName,'r').read()
                template = eval(text)
                print(template)
                for i, dataMethod in enumerate(template['DataMethods']):
                    if self.mngTabs.count() <= i+1:
                        newTab = self.createNewTab()
                        self.mngTabs.insertTab(self.mngTabs.count()-1, newTab, "new Manager")
                    self.mngTabs.widget(i).restoreActions(dataMethod)
                if template['plotMethod']:
                    self.plotActionWidget.restoreActions(template['plotMethod'])
            except Exception as e:
                print(e)
            
    def saveTemplate(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self.subjectWindow,"QFileDialog.getSaveFileName()", "template.txt","Template Files (*.txt);;All Files (*)", options=options)
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

    def compileAndPlot(self):
        PLOTTER.pyplot().clf()
        PLOTTER.pyplot().cla()
        self.canvas.deleteLater()
        self.toolbar.deleteLater()
        try:
            self.plotActionWidget.compileActions()
        except Exception as e:
            print(e)
            PLOTTER.newFigure(1, 1, True)
            
        self.canvas = FigureCanvasQTAgg(PLOTTER.figure())
        self.canvas.setObjectName("canvas")
        self.toolbar = NavigationToolbar2QT(self.canvas, self.subjectWindow)
        self.verticalLayout_4.addWidget(self.toolbar)
        self.verticalLayout_4.addWidget(self.canvas)
        self.canvas.draw()
        
    def saveImage(self):
        options = QFileDialog.Options()
        direct = ''
        if isinstance(self.mngTabs.currentWidget(), MngTabWidget) and self.mngTabs.currentWidget().dataManager():
            direct = self.mngTabs.currentWidget().dataManager().docInfo('path') + self.mngTabs.currentWidget().dataManager().docInfo('name') + '.tif'   
        fileName, _ = QFileDialog.getSaveFileName(self.subjectWindow,"QFileDialog.getSaveFileName()", direct,"Images (*.tif *.png *.jpg);;All Files (*)", options=options)
        if fileName:
            PLOTTER.pyplot().savefig(fileName, dpi=300, bbox_inches="tight")
# setattr(BaseUI, 'retranslateUi', retranslateUi)

class PlotterGUI:
    def __init__(self, root):
        self._root = root
        self._mainMenu = None
        self._dataNB = None
        self._infoNB = None
        self._plotterFrm = None
        self._canvas= None
        self._terms = {
            "defaultNBLabel" : "New Method"
            }

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