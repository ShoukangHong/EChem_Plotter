# -*- coding: utf-8 -*-
"""
@author: shouk
"""
import os, pandas, numpy, math, re
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

class PlotData:
    def __init__(self, label, values, unit = ''):
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
        self.loadRawData(rawAddress, sheet)
    
    # =======================================
    # Load and format file
    # =======================================
    def loadRawData(self, rawAddress,sheet = 0):
        '''given a doc address, return the data as a string'''
        self.clearData()
        self._docInfo = {}
        address = self.loadDocInfo(rawAddress)
        docType = self.docInfo('type') 
        try:
            if docType in ['.xlsx', '.xlsm', '.xls']:
                dataFrame = pandas.read_excel(address, sheet)
                self._rawData=dataFrame.to_csv(index=False, sep='\t').split('\r\n')
            elif docType == '.mpt':
                doc = open(address, 'r', encoding='utf-8',errors = 'ignore')
                self._rawData = doc.readlines()
                doc.close()
            else:
                doc = open(address, 'r', errors = 'ignore')
                self._rawData = doc.readlines()
                doc.close()
        except Exception as e:
            print(e)
            raise e
            
            
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
    
    def formatRawData(self, spliter = '\t', starter = None, ender = None, maxLine = 99999999):
        '''given raw data, format it to meet certain criteria.
        spliter, starter, ender, (str): determines the way to deal with raw data
        '''
        spString = spliter
        spliter = self.createSpliter(spliter)
        starter = self.createStarter(starter)
        ender = self.createEnder(ender)
        i = 0
        while not starter(self._rawData[i]):
            i += 1
        self._header = spliter(self._rawData[i].strip())
        i += 1
        self._data = pandas.DataFrame([], columns = self._header)
        temp = []
        while i < len(self._rawData) and i < maxLine and not ender(self._rawData[i]):
            if self._rawData[i] == '':
                i+=1
            elif len(temp)<500000:
                temp.append(spliter(self._rawData[i].strip()))
                i += 1
            else:
                temp = pandas.DataFrame(temp, columns = self._header)
                self._data = pandas.concat([self._data, temp], ignore_index=True)
                temp = []
                print('Formating data...' + str(i) + '/' + str(len(self._rawData)))
        if len(temp) > 0:
            temp = pandas.DataFrame(temp, columns= self._header)
            self._data = pandas.concat([self._data, temp], ignore_index=True)
    
    def createPlotData(self, key, label = None, funcString = None, sigfig = None):
        '''create and store plot data for further calculation and plotting
        key(str/int): the text/index used to get data from column with corresponding index/title
        label(str): the name assigned to the plotData
        funcString(str): the expression will be applied to each value of the plot data.
            i: current index of the iteration
            val: ith value of the column, equals to label(i)
            variables: use the variable name
            plotDatas: plotDataName(index, optional:default) default is the default value if index out of range
            Example: variable: {'a': 3, 'b':2}
                plot data: {'x':[1,2,3,4,5], y:[2,4,6,8,10]}
                label: x
                funcString: 2 * val + y(i) * (a - b)
                calculation when i = 0: 2 * 1 + 2 * (3-2)
                final result: [4, 8, 12, 16, 20]
        '''
        label = label if label else self.getHead(key)
        values = numpy.array(self.getCol(key, sigfig), dtype=numpy.float32)
        self.plotDataSet()[label] = PlotData(label, values)
        if funcString:
            values = self.modifyValues(values, funcString)
            self.getPlotData(label).setValues(values)
    
    def modifyPlotDataValues(self, label, funcString):
        plotData = self.getPlotData(label)
        plotData.setValues(self.modifyValues(plotData.values(), funcString))
    
    def modifyValues(self, values, funcString):
        func = self.createDataHandler(funcString)
        return numpy.array([func(i, val, self.variables(), self.plotDataSet()) for i, val in enumerate(values)], dtype=numpy.float32)
    
    def clearData(self):
        self._header= []
        self._data = []
        self._variables = {}
        self._plotDataSet = {}
    
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
        
    def savePlotData(self, labels = None, address = None, name = None, step = 1):
        if not labels:
            labels = [label for label in self._plotDataSet]
        array = numpy.array([self.getPlotDataValues(label)[::step] for label in labels]).transpose()
        dataFrame = pandas.DataFrame(array, columns = labels, dtype = str)
        name = name if name else self._docInfo['name']
        address = address if address else self._docInfo['path'] + name + '.txt'
        if address == self._docInfo['address']:
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
    def truncatePlotDataByTurn(self, label, turnhandlerString, inputLabels, outputLabels = None, startTurn = 1, endTurn = 1, step = 1):
        '''set plot range by turn handler, only collect plot data from startTurn to endTurn(inclusive) counting turn from 1
        label(str):label of the plot data used to determin turn
        turnhandlerString(str): an expression to determine turn, if result is true, plus 1 turn
        startTurn(int): the turn to start plot data collection.
        endTurn(int): turn to end data plot collecting.
        '''
        allValues = self.getPlotDataValues(label)
        turn = 1
        i = start = end = 0
        turnhandler = self.createDataHandler(turnhandlerString)
        while turn < startTurn and i < len(allValues):
            if turnhandler(i, allValues[i], self.variables(), self.plotDataSet()):
                turn += 1
            i += 1
            assert i < len(allValues), 'Cannot find start turn ' + str(startTurn) + ' with function string: ' + turnhandlerString
        if i > 1 and i < len(allValues) and turn <= endTurn:
            start = i - 1
        while turn <= endTurn and i < len(allValues):
            if turnhandler(i, allValues[i], self.variables(), self.plotDataSet()):
                turn += 1
            i += 1
        end = max(start, i - 1)
        
        for i, targetLabel in enumerate(inputLabels):
            plotData = self.getPlotData(targetLabel)
            values = plotData.values()
            if outputLabels:
                self.plotDataSet()[outputLabels[i]] = PlotData(outputLabels[i], values[start:end:step])
            else:
                plotData.setValues(values[start:end:step])
    
    def truncatePlotDataByValue(self, label, inputLabels, outputLabels = None, startValue = 0, endValue = float('inf'), step = 1):
        '''set plot range by turn handler, only collect plot data from startValue to endValue(inclusive)
        label(str):label of the plot data used to determin turn
        startValue(int): the value to start plot data collection.
        endValue(int): value to end plot data collecting.
        '''
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
        
        for i, targetLabel in enumerate(inputLabels):
            plotData = self.getPlotData(targetLabel)
            values = plotData.values()
            if outputLabels:
                self.plotDataSet()[outputLabels[i]] = PlotData(outputLabels[i], values[start:end:step])
            else:
                plotData.setValues(values[start:end:step])

    def filterPlotDataByFunc(self, label, inputLabels, funcString = '', outputLabels = None):
        '''filter plot data by funcString, only collect plot data that returns true,
        label(str):label of the plot data used to determin turn
        '''
        values = self.getPlotDataValues(label)
        func = self.createDataHandler(funcString)
        filterList = [func(i, val, self.variables(), self.plotDataSet()) for i, val in enumerate(values)]
        # def filterByList(inputValues):
        #     outPut = []
        #     for i, val in enumerate(inputValues):
        #         if filterList[i]:
        #             outPut.append(val)
        #     return numpy.array(outPut)
        for i, targetLabel in enumerate(inputLabels):
            plotData = self.getPlotData(targetLabel)
            filteredValues = plotData.values()[filterList]
            if outputLabels:
                self.plotDataSet()[outputLabels[i]] = PlotData(outputLabels[i], filteredValues)
            else:
                plotData.setValues(filteredValues)
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
        wordSet = set(['val', 'i', 'self', 'funcString'])
        nameSet = set(self.plotDataSet().keys()).union(set(self.variables().keys()))
        nameIntersect = set(self.plotDataSet().keys()).intersection(self.variables().keys())
        assert len(nameIntersect) == 0, "variable/plotData name: " + str(nameIntersect) + ' duplicates!'
        assert len(wordSet.intersection(nameSet)) == 0, "variable/plotData name: " + str(wordSet.intersection(nameSet)) + ' not allowed!'
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
        for key in self.variables():
            string = re.sub(r'(\W)('+ key + r')(\W)', r"\1variables['\2']\3", string)
        return 'def func(i, val, variables, plotDataSet): \n\t return ' + string[1:-1]
    
    def createInfoData(self):
        '''return a dict'''
        info = {'raw': self.getShortList(self._rawData),
                'data': self.getShortList(self._data),
                'variables' : self._variables.copy(),
                'plotData' : {key:self.getShortList(data.values()) for key, data in self._plotDataSet.items()}
                }
        return info
    
    def getShortList(self, data):
        if isinstance(data, pandas.DataFrame):
            if data.shape[0] < 400:
                return numpy.concatenate(([self._header[:]], data.to_numpy()))
            else:
                return numpy.concatenate(([self._header[:]], data[:100].to_numpy(),
                                    data[data.shape[0]//2-50:data.shape[0]//2+50].to_numpy(),
                                    data[-100:].to_numpy()))
        elif not isinstance(data, numpy.ndarray) and not data or len(data)<0:
            return []
        elif len(data) < 400:
            return list(data)
        else:
            if isinstance(data[0], list):
                placeHolder = [['...' for i in range(len(data[0]))]]
            else:
                placeHolder = ['...']
            return list(data[:100])+placeHolder+list(data[len(data)//2-50:len(data)//2+50])+placeHolder +list(data[-100:])
        
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
    
    def getCol(self, key, sigfig = None):
        '''given regex or index, return the corresponding column data'''
        head = self.getHead(key)
        try:
            return self._data[head].apply().astype(numpy.float32)
        except:
            return self._data[head]
    
    def getIndex(self, key):
        '''given regex, return the header index that matches regex'''
        if isinstance(key, int):
            return key
        for i, label in enumerate(self._header):
            if key==label:
                return i
        for i, label in enumerate(self._header):
            if re.match(key, label):
                return i
        raise NameError('key not found! Key: ' + key + ', Header: ' + str(self._header))

    def getData(self):
        return self._data
    
    def plotDataSet(self):
        return self._plotDataSet

    def getPlotData(self, label):
        return self._plotDataSet.get(label, None)
    
    def getPlotDataValues(self, label):
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
        if clear:
            self.figure().clear()
            plt.clf()
            plt.cla()
            plt.close()
        plt.figure(self._figureCount)
    
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
        
    def newFigure(self, nrows=1, ncols=1, clear = True):
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
    
    def setXAxLabel(self, label, **kwargs):
        '''label(str): Set a label that will be displayed on active x axis.'''
        self.activeAx().set_xlabel(label, **kwargs)
        
    def setYAxLabel(self, label, **kwargs):
        '''label(str): Set a label that will be displayed on active y axis.'''
        self.activeAx().set_ylabel(label, **kwargs)
    
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
    
    def setTitle(self, title = '', **kwargs):
        '''label(str): Set the title of active ax.'''
        self.activeAx().set_title(title, **kwargs)
    
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
        interval(float): set interval value for each tick.
        tickNum(int): Target number of ticks. Will determine interval based on this value. The final tick
            number may not be exactly the tickNumber, because tick increments needs to be 1, 2 or 5 *10^x.
        minor(int, bool): minor tick number, set 0 will use auto minor tick, set as number will have the
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
        if minor == 0:
            axis.set_minor_locator(plticker.AutoMinorLocator())
        elif isinstance(minor, int):
            axis.set_minor_locator(plticker.AutoMinorLocator(minor))
        
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
            if 's' in realign:
                bottom = bottom - bottom % interval
            if 'e' in realign:
                top = top + interval - top % interval
            self.activeAx().set_ylim(bottom = bottom, top = top)
    
    def __getInterval(self, difference, tickNum):
        '''return the ideal interval based on difference of end and start value and target tick number'''
        difference = self.__roundToNSigFigs(difference, 2)
        interval = self.__roundToNSigFigs(difference/tickNum, 1)
        digits = self.__digits(interval)
        interval = int(interval * 10 ** (-digits))
        if interval > 7:
            interval = 10
        elif interval >= 3:
            interval = 5
        return interval * 10 ** digits
    
    def __roundToNSigFigs(self, val, n):
        '''given a value val, round to n sig figs and return'''
        return round(val, n-self.__digits(val)-1)
    
    def __digits(self, val):
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

    def setDataManager(self, dataManagers):
        self._dataManagers = dataManagers

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