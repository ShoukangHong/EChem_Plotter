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
from PlotterWidgets import MngTabWidget

PLOTTER = Plotter_Core.EchemPlotter()
BaseUI, Window = uic.loadUiType("UI/mainWindow.ui")
BaseMngTabUI, MngTab = uic.loadUiType("UI/mngTab.ui")
_oldFunc = BaseUI.retranslateUi

ROOT = INFOTABS = MNGTABS = PLTTABS = CANVAS = None

class Ui_MainWindow(BaseUI):
    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)
        mainWindow.ui = self
        self.connectEvents(mainWindow)
        self.setGlobals()
        
    def retranslateUi(self, mainWindow):
        self.canvas.deleteLater()
        fig, ax = PLOTTER.newFigure(1, 1, True)
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setObjectName("canvas")
        toolbar = NavigationToolbar2QT(self.canvas, mainWindow)
        self.verticalLayout_4.addWidget(toolbar)
        self.verticalLayout_4.addWidget(self.canvas)
        ax.plot([0,1,2,3,4], [10,1,20,3,40])
        self.addInitialWidgets(mainWindow)
        super().retranslateUi(mainWindow)
    
    def setGlobals(self):
        global ROOT, INFOTABS, MNGTABS, PLTTABS, CANVAS
        ROOT = self
        INFOTABS = self.infoTabs
        MNGTABS = self.mngTabs
        PLTTABS = self.pltTabs
        CANVAS = self.canvas
    
    def addInitialWidgets(self, mainWindow):
        newTab = MngTabWidget(self.mngTabs)
        self.mngTabs.addTab(newTab, "new Tab")
        newTab.setInfoWindows(self.rawDataInfoList,
                              self.dataInfoTable,
                              self.varInfoTable,
                              self.plotDataInfoTable)
    
    def connectEvents(self, mainWindow):
        pass
        
        
    
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