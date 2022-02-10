# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:33:54 2022

@author: shouk
"""
import os
import re
import pandas
import numpy
import matplotlib.pyplot as plt

class PlotData:
    def __init__(self, label, values, unit):
        self._values = values
        self._unit = unit
        self._label = label
    
    def unit(self):
        return self._unit
    
    def values(self):
        return self._values
    
    def setValues(self, values):
        self._values = values
        
    def getValue(self, index, default = None):
        if 0 <= index < len(self._values):
            return self._values[index]
        if default != None:
            return default
        return self._values[max(0, min(index, len(self._values) - 1))]
    
    def label(self):
        return self._label
    
    def __str__(self):
        return '\n'.join( [self._label] + [self._unit] + [str(val) for val in self._values])
    
class DataManager:
    def __init__(self, rawAddress, sheet = 0):
        self._docInfo = {}
        self._rawData = []
        self._header= []
        self._data = []
        self._variables = {}
        self._plotDataSet = {}
        self._starter = self._ender = self._spliter = None
        self._eventLog = []
        self.loadDocInfo(rawAddress)
        self.loadRawData(self.docInfo('address'), sheet)
        
    def loadDocInfo(self, rawAddress):
        '''given a document address, format it and store document info({address: , path: , name: , type: })'''
        self._docInfo['address'] = self.formatAddress(rawAddress)
        parts = self._docInfo['address'].split('/')
        lastPart = parts[-1].split('.')
        self._docInfo['path'] = '/'.join(parts[:-1]) + '/'
        self._docInfo['name'] = '.'.join(lastPart[:-1])
        self._docInfo['type'] = '.' + lastPart[-1]
    
    def formatAddress(self, rawAddress):
        '''convert \ to / and store'''
        address = ''
        for char in repr(rawAddress):
            if char == '\\':
                address += '/' if address[-1] != '/' else ''
            else:
                address += char
        return address[1:-1]
    
    def docInfo(self, key):
        '''given key, return corresponding document info.
        key can be 'address', 'path', 'name' and 'type'.'''
        return self._docInfo[key]
    
    def loadRawData(self, address,sheet = 0):
        '''given a doc address, return the data as a string'''
        try:
            doc = open(address, 'r')
            self._rawData = doc.readlines()
        except:
            try :
                doc = pandas.read_excel(address, sheet)
                self._rawData = doc.to_csv(index=False, sep='\t').split('\r\n')
            except:
                self.pushLog('document doesn\'t exist!')
                self.viewLog()
    
    def formatRawData(self, spliter = None, starter = None, ender = None, digits = None):
        '''given raw data, format it to meet certain criteria.'''
        self._digits = digits
        spliter = self.createSpliter() if not spliter else spliter
        starter = self.createStarter() if not starter else starter
        ender = self.createEnder() if not ender else ender
        i = 0
        while not starter(self._rawData[i]):
            i += 1
            
        self._header = spliter(self._rawData[i])
        i += 1
        
        while i < len(self._rawData) and not ender(self._rawData[i]):
            if self._rawData[i] != '':
                line = [string for string in spliter(self._rawData[i])]
                self._data.append(line)
            i += 1
            
        del self._rawData
      
    def getHead(self, key):
        index = self.getIndex(key)
        return self._header[index]
    
    def getCol(self, key):
        '''given regex or index, return the corresponding column data'''
        index = self.getIndex(key)
        try:
            if self._digits:
                return [round(float(line[index]), self._digits) for line in self._data]
            else:
                return [float(line[index]) for line in self._data]
        except:
            return [line[index] for line in self._data]
    
    def getIndex(self, key):
        '''given regex, return the header index that matches regex'''
        if isinstance(key, int):
            return key
        for i, label in enumerate(self._header):
            if re.match(key, label):
                return i

    def getData(self):
        return self._data

    def printData(self):
        print('\t'.join(self._header))
        print('\n'.join(['\t'.join([str(num) for num in line]) for line in self._data]))

    def createSpliter(self, regex = '\t'):
        def spliter(string):
            return string.split(regex)
        return spliter

    def createStarter(self, regex = None):
        if not regex:
            def starter(string):
                return True
        else:
            def starter(string):
                return re.search(regex, string)
        return starter

    def createEnder(self, regex = None):
        if not regex:
            def ender(string):
                return False
        else:
            def ender(string):
                return re.search(regex, string)
        return ender
    
    def modifyPlotDataValues(self, label, funcString):
        plotData = self.getPlotData(label)
        plotData.setValues(self.modifyValues(plotData.values(), funcString))
    
    def modifyValues(self, values, funcString):
        func = self.createDataHandler(funcString)
        return [func(i, val, self.variables(), self.plotDataSet()) for i, val in enumerate(values)]

    def createPlotData(self, key, funcString = None, unit = '', label = None):
        label = label if label else  self.getHead(key)
        values = [val for val in self.getCol(key)]
        self._plotDataSet[label] = PlotData(label, values, unit)
        if funcString:
            values = self.modifyValues(values, funcString)
            self._plotDataSet[label].setValues(values)

    def createDataHandler(self, string = None):
        if string == '' or not string:
            return None
        funcString = self.toFunctionString(string)
        exec(funcString, globals())
        return globals()['func']
    
    def toFunctionString(self, string):
        string = ' ' + string + ' '
        for key in self.plotDataSet():
            string = re.sub(r'(\W)('+ key + ')\(', r"\1plotDataSet['\2'].getValue(", string)
        #print(string)
        #string = re.sub(r'plotDataSet\[(.*?)\]', r'plotDataSet[\1].getValue', string)
        for key in self.variables():
            string = re.sub(r'(\W)('+ key + ')(\W)', r"\1variables['\2']\3", string)
        #print(string)
        return 'def func(i, val, variables, plotDataSet): \n\t return ' + string[1:-1]
    
    def createVariable(self, name, val):
        self._variables[name]= val
    
    def variables(self):
        return self._variables
    
    def getVariable(self, name):
        return self.variables().get(name, None)    
    
    def plotDataSet(self):
        return self._plotDataSet

    def getPlotData(self, label):
        return self._plotDataSet.get(label, None)
    
    def getPlotDataValues(self, label):
        if self.getVariable('startIndex') and self.getVariable('endIndex'):
            return self.getPlotData(label).values()[self.getVariable('startIndex'):self.getVariable('endIndex')]
        else:
            return self.getPlotData(label).values()
    
    def setPlotRange(self, start, end):
        self.createVariable('startIndex', start)
        self.createVariable('endIndex', end)
    
    def resetPlotRange(self):
        if self.getVariable('startIndex'):
            self.variables().pop('startIndex')
        if self.getVariable('endIndex'):
            self.variables().pop('endIndex')
    
    def setPlotRangeByTurn(self, label, turnhandlerString, turnStart = 1, turnEnd = 2):
        self.resetPlotRange()
        allValues = self.getPlotDataValues(label)
        turn = 1
        i = start = end = 0
        turnhandler = self.createDataHandler(turnhandlerString)
        while turn < turnStart and i < len(allValues):
            if turnhandler(i, allValues[i], self.variables(), self.plotDataSet()):
                turn += 1
            i += 1
        if i > 1 and i < len(allValues) and turn < turnEnd:
            start = i - 1
        while turn < turnEnd and i < len(allValues):
            if turnhandler(i, allValues[i], self.variables(), self.plotDataSet()):
                turn += 1
            i += 1
        end = i
        self.setPlotRange(start, end)
    
    def setPlotRangeByValue(self, label, startValue, endValue = float('inf')):
        self.resetPlotRange()
        allValues = self.getPlotDataValues(label)
        i = start = end = 0
        if startValue <= endValue:
            def compareFunc(a, b):
                return a < b
        elif startValue > endValue: 
            def compareFunc(a, b):
                return a > b
        
        while i < len(allValues) and compareFunc(allValues[i], startValue):
            i += 1
        start = i
        while i < len(allValues) and (compareFunc(allValues[i], endValue) or allValues[i] == endValue):
            i += 1
        end = i
        self.setPlotRange(start, end) 
    
    def pushLog(self, string):
        self._eventLog.append(string)
        print('event history: ')
        if len(self._eventLog) > 20:
            self._eventLog.pop(0)
        
    def viewLog(self):
        for string in self._eventLog[::-1]:
            print(string)
            
class EchemPlotter:
    def __init__(self):
        self._dataManagers = []
        self._pyplot = plt
        self._figureCount = 1
        self._activeDataManager = plt.figure(1)
        self._activeFigure = None
        self._activeAx = None
        self._ax = []
        self._twinX = []
        self._twinY = []
        
    def pyplot(self):
        return self._pyplot
    
    def openDoc(self, rawAddress):
        self.addDataManager(DataManager(rawAddress))
    
    def addDataManager(self, dataManager):
        self._activeDataManager = dataManager
        self._dataManagers.append(dataManager)
    
    def activeDataManager(self):
        return self._activeDataManager
    
    def getPlotData(self, key, manager = None):
        if not manager:
            manager = self.activeDataManager()
        return manager.getPlotData(key)
      
    def getPlotDataValues(self, key, manager = None):
        return self.getPlotData(key, manager).values()
    
    def plot(self, xData, yData, axIndex = None, legend = None, style = None):
        ax = self.indexToAx(axIndex)
        if style:
            ax.plot(xData, yData, style, label = legend)
        else:
            ax.plot(xData, yData, label = legend)
            
    def newFig(self):
        self._figureCount += 1
        self._activeFigure = plt.figure(self._figureCount)
        return self._activeFigure
        
    def setSubPlots(self, nrows=1, ncols=1):
        self._activeFigure, self._ax = plt.subplots(nrows, ncols, constrained_layout=True)
        if not isinstance(self._ax, numpy.ndarray):
            self._ax = [self._ax]
        self._activeAx = self.indexToAx(0)
        self._twinX = [None for _ in range(len(self._ax))]
        self._twinY = [None for _ in range(len(self._ax))]
    
    def setXAxLabel(self, label, axIndex = None):
        ax = self.indexToAx(axIndex)
        ax.set_xlabel(label)
        
    def setYAxLabel(self, label, axIndex = None):
        ax = self.indexToAx(axIndex)
        ax.set_ylabel(label)
        
    def setAxScale(self, xStart = None, xEnd = None, yStart = None, yEnd = None, axIndex = None):
        ax = self.indexToAx(axIndex)
        if xStart != None or xEnd != None:
            ax.set_xlim(left = xStart, right = xEnd)
        if yStart != None or yEnd != None:
            ax.set_ylim(bottom = yStart, top = yEnd)
    
    def addTwinX(self, axIndex = None):
        '''add twin x axis and set the twin axis to active'''
        if not axIndex:
            axIndex = self.activeAxIndex()
        ax = self.indexToAx(axIndex)
        self._twinX[axIndex] = ax.twinx()
        self.setActiveAx(axIndex, 'x')
    
    def addTwinY(self, axIndex = None):
        '''add twin y axis and set the twin axis to active'''
        if not axIndex:
            axIndex = self.activeAxIndex()
        ax = self.indexToAx(axIndex)
        self._twinY[axIndex] = ax.twiny()
        self.setActiveAx(axIndex, 'y')
    
    def setActiveAx(self, index, twin = None):
        self._activeAx = self.indexToAx(index, twin)
        plt.sca(self._activeAx)
    
    def activeAx(self):
        return self._activeAx
    
    def activeAxIndex(self):
        for i in range(len(self._ax)):
            if self._activeAx in [self._ax[i], self._twinX[i], self._twinY[i]]:
                return i
    
    def indexToAx(self, index, twin = None):
        if index == None:
            return self._activeAx
        if twin == 'x':
            return self._twinX[index]
        if twin == 'y':
            return self._twinY[index]
        return self._ax[index]
    
    def showLegend(self, axIndex = None, loc = 'best'):
        lines = []
        labels = []
        i = self.activeAxIndex()
        for ax in [self._ax[i], self._twinX[i], self._twinY[i]]:
            if ax:
                newLines, newLabels = ax.get_legend_handles_labels()
                lines += newLines
                labels += newLabels
        self._activeAx.legend(lines, labels, loc=loc)
        