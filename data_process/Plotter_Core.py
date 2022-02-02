# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:33:54 2022

@author: shouk
"""
import os

class DataManager:
    def __init__(self, rawAddress):
        self._docInfo = {}
        self._rawData = []
        self._eventLog = []
        self.loadDocInfo(rawAddress)
        self.loadRawData(self.docInfo('address'))
        
    def loadDocInfo(self, rawAddress):
        '''given a document address, format it and store document info({address: , path: , name: , type: })'''
        self.formatAddress(rawAddress)
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
        self._docInfo['address'] = address[1:-1]
    
    def docInfo(self, key):
        '''given key, return corresponding document info.
        key can be 'address', 'path', 'name' and 'type'.'''
        return self._docInfo[key]
    
    def loadRawData(self, address):
        '''given a doc address, return the data as a string'''
        try:
            doc = open(address, 'r')
            self._rawData = doc.readlines()
        except:
            self.pushLog('document doesn\'t exist!')
            self.viewLog()
    
    def formatRawData(self, rawData):
        '''given raw data, format it to meet certain criteria.'''
        pass
    
    def pushLog(self, string):
        self._eventLog.append(string)
        print('event history: ')
        if len(self._eventLog) > 20:
            self._eventLog.pop(0)
        
    def viewLog(self):
        for string in self._eventLog[::-1]:
            print(string)
        
    def setDataTable(self, body, regex):
        '''given the data and regular expression, seperate the data into a 2D table.'''
        pass

    def setDataRange(self, startCondition, endCondition):
        pass

    def setHeaderAndBody(self, dataTable, regex):
        '''given the data table and regular expression, identify header row and body row, return header row and body row'''
        pass

    def addDataOfInterest(self, regex):
        pass

    def processDataOfInterest(self, expression):
        pass
    
    def setXCol(self, regex):
        pass

    def setYCol(self, regex):
        pass
    
    def setXLabel(self, name):
        pass

    def setYLabel(self, name):
        pass

    def setXName(self, name):
        pass

    def setYName(self, name):
        pass