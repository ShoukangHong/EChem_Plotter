# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:33:54 2022

@author: shouk
"""
import os
import re
import pandas
import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

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
    def __init__(self, rawAddress, sheets = None):
        self._docInfo = {}
        self._rawData = []
        self._header= []
        self._data = []
        self._variables = {}
        self._plotDataSet = {}
        self._starter = self._ender = self._spliter = None
        self._eventLog = []
        self.loadRawData(rawAddress, sheets)
    
    # =======================================
    # Load and format file
    # =======================================
    def loadRawData(self, rawAddress,sheets = None):
        '''given a doc address, return the data as a string'''
        address = self.loadDocInfo(rawAddress)
        try:
            doc = open(address, 'r')
            self._rawData.append(doc.readlines())
        except:
            try:
                sheets = sheets if sheets else (0,)
                for sheet in sheets:
                    dataFrame = pandas.read_excel(address, sheet)
                    self._rawData.append(dataFrame.to_csv(index=False, sep='\t').split('\r\n'))
            except:
                self.__pushLog('document doesn\'t exist!')
                self.viewLog()
                
    def loadDocInfo(self, rawAddress):
        '''given a document address, format it and store document info({address: , path: , name: , type: })'''
        self._docInfo['address'] = self.formatAddress(rawAddress)
        parts = self._docInfo['address'].split('/')
        lastPart = parts[-1].split('.')
        self._docInfo['path'] = '/'.join(parts[:-1]) + '/'
        self._docInfo['name'] = '.'.join(lastPart[:-1])
        self._docInfo['type'] = '.' + lastPart[-1]
        return self._docInfo['address']
    
    def formatAddress(self, rawAddress):
        '''convert \ to / and store'''
        address = ''
        for char in repr(rawAddress):
            if char == '\\':
                address += '/' if address[-1] != '/' else ''
            else:
                address += char
        return address[1:-1]
    
    def formatRawData(self, spliter = None, starter = None, ender = None, digits = None):
        '''given raw data, format it to meet certain criteria.
        spliter, starter, ender, (str): determines the way to deal with raw data
        '''
        self._digits = digits
        spliter = self.createSpliter() if not spliter else spliter
        starter = self.createStarter() if not starter else starter
        ender = self.createEnder() if not ender else ender
        for rawData in self._rawData:
            i = 0
            while not starter(rawData[i]):
                i += 1
                
            self._header = spliter(rawData[i].strip())
            i += 1
            
            while i < len(rawData) and not ender(rawData[i]):
                if rawData[i] != '':
                    line = [string for string in spliter(rawData[i].strip())]
                    self._data.append(line)
                i += 1
            
        del self._rawData
    
    def truncateData(self, step = 1, start = 0, end = None):
        if end == None:
            end = len(self._data)
        self._data = self._data[start:end:step]
    
    def createPlotData(self, key, funcString = None, unit = '', label = None):
        '''create and store plot data for further calculation and plotting'''
        label = label if label else  self.getHead(key)
        values = [val for val in self.getCol(key)]
        self._plotDataSet[label] = PlotData(label, values, unit)
        if funcString:
            values = self.modifyValues(values, funcString)
            self._plotDataSet[label].setValues(values)
    
    def modifyPlotDataValues(self, label, funcString):
        plotData = self.getPlotData(label)
        plotData.setValues(self.modifyValues(plotData.values(), funcString))
    
    def modifyValues(self, values, funcString):
        func = self.createDataHandler(funcString)
        return [func(i, val, self.variables(), self.plotDataSet()) for i, val in enumerate(values)]
    
    # =======================================
    # Save
    # =======================================
    def saveData(self, address = None, step = 1):
        if step > 1:
            self.truncateData(step)
        dataFrame = pandas.DataFrame(self._data, columns = self._header, dtype = str)
        if not address:
            address = self._docInfo['path'] + self._docInfo['name'] + '.txt'
        address = self.__autoAddress(address)
        dataFrame.to_csv(address, header = True, index=False, sep='\t')
        
    def savePlotData(self, address = None, labels = None, step = 1):
        if not labels:
            labels = [label for label in self._plotDataSet]
        array = numpy.array([self.getPlotDataValues(label)[::step] for label in labels]).transpose()
        dataFrame = pandas.DataFrame(array, columns = labels, dtype = str)
        if not address:
            address = self._docInfo['path'] + self._docInfo['name'] + '.txt'
        address = self.__autoAddress(address)
        dataFrame.to_csv(address, header = True, index=False, sep='\t')
    
    def __autoAddress(self, address):
        count = 0
        parts = address.split('.')
        addressWOType = '.'.join(parts[:-1])
        saveType = '.' + parts[-1]
        while os.path.exists(address) and count < 100:
            count += 1
            address = addressWOType + '(' + str(count) + ')'+ saveType
        return address
    
    # =======================================
    # Methods to set plot range
    # =======================================
    def setPlotRangeByTurn(self, label, turnhandlerString, startTurn = 1, endTurn = 2):
        '''set plot range by turn handler, only collect plot data from startTurn to endTurn(inclusive) counting turn from 1
        label(str):label of the plot data used to determin turn
        turnhandlerString(str): an expression to determine turn, if result is true, plus 1 turn
        startTurn(int): the turn to start plot data collection.
        endTurn(int): turn to end data plot collecting.
        '''
        self.resetPlotRange()
        allValues = self.getPlotDataValues(label)
        turn = 1
        i = start = end = 0
        turnhandler = self.createDataHandler(turnhandlerString)
        while turn < startTurn and i < len(allValues):
            if turnhandler(i, allValues[i], self.variables(), self.plotDataSet()):
                turn += 1
            i += 1
        if i > 1 and i < len(allValues) and turn < endTurn:
            start = i - 1
        while turn < endTurn and i < len(allValues):
            if turnhandler(i, allValues[i], self.variables(), self.plotDataSet()):
                turn += 1
            i += 1
        end = i
        self.setPlotRange(start, end)
    
    def setPlotRangeByValue(self, label, startValue, endValue = float('inf')):
        '''set plot range by turn handler, only collect plot data from startValue to endValue(inclusive)
        label(str):label of the plot data used to determin turn
        startValue(int): the value to start plot data collection.
        endValue(int): value to end plot data collecting.
        '''
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
    
    def setPlotRange(self, start = 0, end = None):
        '''set plot range by index, collect data from start to end, excluding end
        start(int): start index, default is 0
        end(int): end index, default is length of the plot data.
        '''
        if not end:
            end = len(self._data)
        self.createVariable('startIndex', start)
        self.createVariable('endIndex', end)
    
    def resetPlotRange(self):
        if self.getVariable('startIndex'):
            self.variables().pop('startIndex')
        if self.getVariable('endIndex'):
            self.variables().pop('endIndex')
            
    # =======================================
    # function and variable creaters
    # =======================================
    def createVariable(self, name, val):
        self._variables[name]= val
        
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

    def createDataHandler(self, string = None):
        if string == '' or not string:
            return None
        funcString = self.toFunctionString(string)
        exec(funcString, globals())
        return globals()['func']
    
    def toFunctionString(self, string):
        string = ' ' + string + ' '
        for key in self.plotDataSet():
            string = re.sub(r'(\W)('+ key + r')\(', r"\1plotDataSet['\2'].getValue(", string)
            string = re.sub(r"([^'\w])("+ key + r")([^'\w])", r"\1plotDataSet['\2']\3", string)
        #print(string)
        #string = re.sub(r'plotDataSet\[(.*?)\]', r'plotDataSet[\1].getValue', string)
        for key in self.variables():
            string = re.sub(r'(\W)('+ key + r')(\W)', r"\1variables['\2']\3", string)
        #print(string)
        return 'def func(i, val, variables, plotDataSet): \n\t return ' + string[1:-1]
    
    # =======================================
    # log info
    # =======================================
    def __pushLog(self, string):
        self._eventLog.append(string)
        print('event history: ')
        if len(self._eventLog) > 20:
            self._eventLog.pop(0)

    def viewLog(self):
        for string in self._eventLog[::-1]:
            print(string)
            
    def __str__(self):
        print('\t'.join(self._header))
        print('\n'.join(['\t'.join([str(num) for num in line]) for line in self._data]))
        
    # =======================================
    # Getters
    # =======================================
    def docInfo(self, key):
        '''given key, return corresponding document info.
        key can be 'address', 'path', 'name' and 'type'.'''
        return self._docInfo[key]
    
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
    
    def plotDataSet(self):
        return self._plotDataSet

    def getPlotData(self, label):
        return self._plotDataSet.get(label, None)
    
    def getPlotDataValues(self, label):
        if self.getVariable('startIndex') and self.getVariable('endIndex'):
            return self.getPlotData(label).values()[self.getVariable('startIndex'):self.getVariable('endIndex')]
        else:
            return self.getPlotData(label).values()
    
    def variables(self):
        return self._variables
    
    def getVariable(self, name):
        return self.variables().get(name, None)


# =======================================
# EchemPlotter Highest class of this project
# =======================================
class EchemPlotter:
    def __init__(self):
        self._dataManagers = []
        self._pyplot = plt
        self._figureCount = 1
        self._activeDataManager = None
        self._figure = plt.figure(1)
        self._activeAx = None
        self._axes = []
        self._twinXs = []
        self._twinYs = []
    
    def openDoc(self, rawAddress):
        self.addDataManager(DataManager(rawAddress))
        
    def resetFig(self, clear = False):
        self._figureCount += 1
        self._axes = []
        self._twinXs = []
        self._twinYs = []
        plt.figure(self._figureCount)
        if clear:
            self.figure().clear()
            plt.close(self.figure())
    
    # =======================================
    # Plotting Methods
    # =======================================
    def plot(self, xDataLabel, yDataLabel, style = None, xDataManagerIndex = None, yDataManagerIndex = None, setXYLabel = True, **kwargs):
        '''plot y vs y data.
        xDataLabel(str): Label of plotdata you want for x values
        yDataLabel(str): Label of plotdata you want for y values
        xDataManagerIndex(int):  Get x plotdata from data manager with this index. If not specified, use active data manager.
        yDataManagerIndex(int): Get y plotdata from data manager with this index. If not specified, use active data manager.
        setXYLabel(bool): set X and Y axis Label as x DataLabel name and yDataLabel name.
        **kwargs: Arbitrary keyword arguments.
            label(str): Set a label that will be displayed in the legend.
            loc : int or {'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right',  ...}
            fontsize: int or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
        '''
        xData = self.getPlotDataValues(xDataLabel, xDataManagerIndex)
        yData = self.getPlotDataValues(yDataLabel, yDataManagerIndex)
        args = [xData, yData]
        if style:
            args.append(style)
            
        if setXYLabel:
            self.setXAxLabel(xDataLabel)
            self.setYAxLabel(yDataLabel)
        
        self.activeAx().plot(*args, **kwargs)
        
    def newFigure(self, nrows=1, ncols=1, clear = False):
        '''Create a new figure with a set of subplots.
        nrows, ncos(int): Number of rows/columns of the subplot grid.
        '''
        self.resetFig(clear)
        self._figure, self._axes = plt.subplots(nrows, ncols, constrained_layout=True)
        if not isinstance(self._axes, numpy.ndarray):
            self._axes = [self._axes]
        self._activeAx = self.indexToAx(0)
        self._twinXs = [None for _ in range(len(self._axes))]
        self._twinYs = [None for _ in range(len(self._axes))]
        return self._figure, self._activeAx
    
    def setXAxLabel(self, label):
        '''label(str): Set a label that will be displayed on active x axis.'''
        self.activeAx().set_xlabel(label)
        
    def setYAxLabel(self, label):
        '''label(str): Set a label that will be displayed on active y axis.'''
        self.activeAx().set_ylabel(label)
    
    def addTwinX(self):
        '''add twin x axis and set the twin axis to active'''
        axIndex = self.activeAxIndex()
        ax = self.indexToAx(axIndex)
        self._twinXs[axIndex] = ax.twinx()
        self.setActiveAx(axIndex, 'x')
    
    def addTwinY(self):
        '''add twin y axis and set the twin axis to active'''
        axIndex = self.activeAxIndex()
        ax = self.indexToAx(axIndex)
        self._twinYs[axIndex] = ax.twiny()
        self.setActiveAx(axIndex, 'y')
    
    def showLegends(self, **kwargs):
        '''Show legends of all axis in the subplot of activeAx.
        **kwargs: Arbitrary keyword arguments.
            loc : int or {'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right',  ...}
            fontsize: int or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
        '''
        lines = []
        labels = []
        i = self.activeAxIndex()
        for ax in [self._axes[i], self._twinXs[i], self._twinYs[i]]:
            if ax:
                newLines, newLabels = ax.get_legend_handles_labels()
                lines += newLines
                labels += newLabels
        self._activeAx.legend(lines, labels, **kwargs)

    # =======================================
    # Scale and tick
    # =======================================
    def setAxScale(self, left = None, right = None, bottom = None, top = None,
                   leftBlank = 0, rightBlank = 0, bottomBlank = 0, topBlank = 0):
        '''set the scale of active axis.
        left, right, bottom, top (float): set the value of corresponding stops.
        leftBlank,  rightBlank, bottomBlank, topBlank (float): set the Blank rate of corresponding stops.
            For example, yEndBlank = 0.5 will auto scale such that it makes top 50% of figure axis blank.
            You cannot set things like both left and leftBlank.
        '''
        ax = self.activeAx()
        if left != None or right != None:
            ax.set_xlim(left = left, right = right)
        if bottom != None or top != None:
            bottom, top = ax.set_ylim(bottom = bottom, top = top)
        if leftBlank > 0 or rightBlank > 0:
            left, right = ax.get_xlim()
            left, right = self.__autoScale(left, right, leftBlank, rightBlank)
            ax.set_xlim(left = left, right = right)
        if bottomBlank > 0 or topBlank > 0:
            bottom, top = ax.get_ylim()
            bottom, top = self.__autoScale(bottom, top, bottomBlank, topBlank)
            ax.set_ylim(bottom = bottom, top = top)  
        
    def __autoScale(self, start, end, startBlank, endBlank):
        '''set the scale of active axis
        return new start and end value based on given args.
        '''
        assert 0 < startBlank + endBlank < 0.95, 'blank ratio exceeds 95% or below 0%!'
        dif = end - start
        blankRatio = startBlank + endBlank
        addition = dif/(1-blankRatio) - dif
        start = start - addition * startBlank / blankRatio
        end = end + addition * endBlank / blankRatio
        return start, end

    def setTickInterval(self, axisType, interval = None, tickNum = None, minor = None, realign = None):
        '''set the tick Intervals
        axisType(str): {'x','y'}, the axis to modify.
        interval(int): set interval value for each tick.
        tickNum(int): Target number of ticks. Will determine interval based on this value. The final tick
            number may not be exactly the tickNumber, because tick increments needs to be 1, 2 or 5 *10^x.
        minor(int, bool): minor tick number, set True will use auto minor tick, set as number will have the
            (number - 1) of minor tick.
        realign(str): {'s', 'e', 'se'}:realign start/end or start and end point after setting the interval
            's' refers to start and 'e' refers to end.
        '''
        if axisType == 'x':
            start, end = self.activeAx().get_xlim()
            axis = self.activeAx().xaxis
        elif axisType == 'y':
            start, end = self.activeAx().get_ylim()
            axis = self.activeAx().yaxis
        else:
            raise Exception("axis must be 'x' or 'y'!")
            
        if interval:
            locator = plticker.MultipleLocator(base=abs(interval))
            axis.set_major_locator(locator)
        elif tickNum:
            interval = self.__getInterval(end - start, tickNum)
            locator = plticker.MultipleLocator(base=abs(interval))
            axis.set_major_locator(locator)
        if minor == True:
            axis.set_minor_locator(plticker.AutoMinorLocator())
        elif isinstance(minor, int):
            axis.set_minor_locator(plticker.AutoMinorLocator(minor))
        
        #print(interval)
        if not interval or not realign:
            return
        
        if axisType == 'x':
            left, right = self.activeAx().get_xlim()
            if 's' in realign:
                left = left - left % interval
            if 'e' in realign:
                right = right + interval - right % interval
            self.activeAx().set_xlim(left = left, right = right)
                
        if axisType == 'y':
            bottom, top = self.activeAx().get_ylim()
            #print(bottom, top)
            if 's' in realign:
                bottom = bottom - bottom % interval
            if 'e' in realign:
                top = top + interval - top % interval
            #print(bottom, top)
            self.activeAx().set_ylim(bottom = bottom, top = top)
    
    def __getInterval(self, difference, tickNum):
        '''return the ideal interval based on difference of end and start value and target tick number'''
        difference = self.__roundToNSigFigs(difference, 2)
        interval = self.__roundToNSigFigs(difference/tickNum, 1)
        digits = self.__dgits(interval)
        interval = int(interval * 10 ** (-digits))
        if interval > 7:
            interval = 10
        elif interval >= 3:
            interval = 5
        return interval * 10 ** digits
    
    def __roundToNSigFigs(self, val, n):
        '''given a value val, round to n sig figs and return'''
        return round(val, n-self.__dgits(val)-1)
    
    def __dgits(self, val):
        '''given a value, return its digits, 1234+> 3, 0.001=> -3'''
        return int(math.floor(math.log10(abs(val))))
    
    # =======================================
    # Getters
    # =======================================
    def pyplot(self):
        return self._pyplot
    
    def addDataManager(self, dataManager):
        self._dataManagers.append(dataManager)
        self.setActiveDataManager(-1)
    
    def figure(self):
        return self._figure
    
    def setActiveDataManager(self, index):
        self._activeDataManager = self._dataManagers[index]
    
    def activeDataManager(self):
        return self._activeDataManager
    
    def setActiveAx(self, index, twin = None):
        '''set the axis you are going to work on.
        index (int): subplot index of the activeAx.
        twin (Optional[str]): {'x' => twinX axis, 'y' => twinY axis}, default is the original axis
        '''
        self._activeAx = self.indexToAx(index, twin)
        plt.sca(self._activeAx)
    
    def activeAx(self):
        return self._activeAx
    
    def indexToAx(self, index, twin = None):
        if index == None:
            return self._activeAx
        if twin == 'x':
            return self._twinXs[index]
        if twin == 'y':
            return self._twinYs[index]
        return self._axes[index]

    def activeAxIndex(self):
        for i in range(len(self._axes)):
            if self._activeAx in [self._axes[i], self._twinXs[i], self._twinYs[i]]:
                return i

    def getPlotData(self, key, index = None):
        dataManager = self.activeDataManager() if index == None else self._dataManagers[index]
        return dataManager.getPlotData(key)
    
    def getPlotDataValues(self, label, index = None):
        '''get plot data values form dataManager
        label(str): label of the plotData
        index(int): index of data manager to get data from. If not specified, get data from active data manager.
        '''
        dataManager = self.activeDataManager() if index == None else self._dataManagers[index]
        return dataManager.getPlotDataValues(label)