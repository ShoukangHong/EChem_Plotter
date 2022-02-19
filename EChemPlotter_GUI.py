# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 11:11:56 2022

@author: shouk
"""
from data_process import Plotter_Core
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog

def addWidgetAttr():
    def setCommandId(self, id):
        self._commandId = id
    
    def commandId(self):
        return self._commandId
    
    setattr(tk.Widget, '_commandId', None)
    setattr(tk.Widget, 'commandId', commandId)
    setattr(tk.Widget, 'setCommandId', setCommandId)
    
    def commandId(self):
        return self._commandId
    
    setattr(tk.Frame, 'getChild', None)


PLOTTER = Plotter_Core.EchemPlotter()

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
        self.initMainMenu(root)
        self.initConfig(root)
        self.initDataNB(root, 0, 0)
        self.initInfoNB(root)
        self.initPlotterFrm(root)
        self.initCanvas(root)
        # self.initPlotterFrm(root, 1, 0)
    # ========================================
    # GUI init
    # ========================================
    def initMainMenu(self, root):
        mainMenu = tk.Menu(root)
        root.config(menu=mainMenu)
        self.initFileMenu(mainMenu)
        self.initRunMenu(mainMenu)
        return mainMenu
    
    def initFileMenu(self, root):
        fileMenu = tk.Menu(root, tearoff=0)
        root.add_cascade(menu=fileMenu, label="File")
        fileMenu.add_command(label="Open", command=self.openFile)
        fileMenu.add_command(label="Save", command=self.doNothing)
        fileMenu.add_command(label="Save as...", command=self.doNothing)
        fileMenu.add_separator()
        fileMenu.add_command(label="Close", command=self.doNothing)
        
    def initRunMenu(self, root):
        runMenu = tk.Menu(root, tearoff=0)
        root.add_cascade(menu=runMenu, label="Run")
        runMenu.add_command(label="Run", command=self.doNothing)
    
    def initConfig(self, root):
        root.rowconfigure([0, 1], minsize=400, weight=1)
        root.columnconfigure([0, 1], minsize=400, weight=1)
    
    def initDataNB(self, root, row = 0, col = 0):
        dataManagerLbl = tk.Label(master = root, text = 'Data Manager')
        dataManagerLbl.grid(row = row, column = col)
        dataNB = ttk.Notebook(root)
        dataNB.grid_propagate(0)
        manager = tk.Frame(dataNB)
        manager.pack(fill='both', expand=True)
        dataNB.add(manager, text=self.term("defaultNBLabel"))
        dataNB.grid(row = row, column = col, sticky = 'news',padx = 5, pady = 5)
        self._dataNB = dataNB
        # manager = tk.Frame(root, relief = 'groove', borderwidth = 1)
        # dataManagerLbl = tk.Label(master = root, text="Data Manager")
        # dataManagerLbl.grid(row = row, column = col)
        # manager.grid(row = row, column = col, sticky = 'news',padx = 5, pady = 5)

    def initInfoNB(self, root, row = 0, col = 1):
        infoNB = ttk.Notebook(root)
        infoNB.grid_propagate(0)
        
        logFrm = ttk.Frame(infoNB)
        logFrm.pack(fill='both', expand=True)
        infoNB.add(logFrm, text='Event Log')
        rawDataFrm = ttk.Frame(infoNB)
        rawDataFrm.pack(fill='both', expand=True)
        infoNB.add(rawDataFrm, text='Raw Data')

        dataFrm = ttk.Frame(infoNB)
        dataFrm.pack(fill='both', expand=True)
        infoNB.add(dataFrm, text='Data')

        variableFrm = ttk.Frame(infoNB)
        variableFrm.pack(fill='both', expand=True)
        infoNB.add(variableFrm, text='Variables')

        plotDataFrm = ttk.Frame(infoNB)
        plotDataFrm.pack(fill='both', expand=True)
        infoNB.add(plotDataFrm, text='Plot Data')

        infoNB.grid(row = row, column = col, sticky = 'news',padx = 5, pady = 5)
        self._infoNB = infoNB
        
    def initPlotterFrm(self, root, row = 1, col = 0):
        plotterFrm = tk.Frame(root, relief = 'groove', borderwidth = 1)
        plotterFrm.grid(row = row, column = col, sticky = 'news',padx = 5, pady = 5)
        plotterLbl = tk.Label(master = plotterFrm, text = "plot data", anchor="w")
        plotterLbl.pack(fill = 'x')
        self._plotterFrm = plotterFrm
        
    def initCanvas(self, root, row = 1, col = 1):
        canvas = tk.Canvas(root, bg="white")
        canvas.create_arc((10, 10, 300, 300), start=0, extent=150, fill="red")
        canvas.grid(row = row, column = col, sticky = 'news',padx = 5, pady = 5)
        self._canvas = canvas
    # ========================================
    # unit Frame
    # ========================================
    
    
    # ========================================
    # GUI handlers
    # ========================================
    
    def openFile(self):
        """Open a file for editing."""
        filepath = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*")]
        )
        print(filepath)
        if not filepath:
            return
        PLOTTER.openDoc(filepath)
        print(self.dataNB().winfo_children())
        manager = tk.Frame(self.dataNB())
        manager.pack(fill='both', expand=True)
        text = PLOTTER.activeDataManager().docInfo('name') + PLOTTER.activeDataManager().docInfo('type')
        self.dataNB().insert(0, manager, text = text)
        # if self.dataNB().tab(0)['text'] == self.term("defaultNBLabel"):
        #     self.dataNB().tab(0)['text'] = PLOTTER.activeDataManager().docInfo('address')
        
    def doNothing(self):
        filewin = tk.Toplevel(self._root)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()
    
    # ========================================
    # Getters
    # ========================================
    def plotter(self):
        return self._plotter
    
    def dataNB(self):
        return self._dataNB
    
    def term(self, term):
        return self._terms[term]
    
if (__name__ == '__main__'):
    addWidgetAttr()
    window = tk.Tk()
    PlotterGUI(window)
    window.mainloop()