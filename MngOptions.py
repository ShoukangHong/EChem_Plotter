# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:28:13 2022

@author: shouk
"""
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
import re

# ==========================
# Validators
# ==========================
nameValidator = QRegExpValidator(QRegExp(r'^[a-zA-Z_][a-zA-Z0-9_]*$'))
nameListValidator = QRegExpValidator(QRegExp(r'^[a-zA-Z][a-zA-Z0-9_, ]*$'))
def nameList(string):
    names = string.split(',')
    for i, name in enumerate(names):
        names[i] = name.strip()
        if names[i] == '' or not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', names[i]):
            raise ValueError("'" + names[i] + "'" + " is not a valid plot data name")
    return names

# ==========================
# help texts
# ==========================
formulaHelp = '''the expression will be applied to modify each value of the plot data.
Useable variables:
i: current index of the value, start from 0
val: ith value of the current index, equals to label(i), label here is the label name you set at required parameter.
variableName: will get the value of variable that has this name. Add the variable before this action otherwise it won't work.
plotDataName(index, default): will get the indexth value of plot data with this name. default is the default value if index out of range.
    if the plot data is not this one, add the plot data before this action otherwise it won't work.
Example: 
    variable: {a: 3, b:2}
    plot data: {x:[1,2,3,4,5], y:[2,4,6,8,10]}
    label: x
    funcString: 2 * val + y(i) * (a - b)
    calculation when i = 0: 2 * 1 + 2 * (3-2)
    final result: [4, 8, 12, 16, 20]
'''

turnFormulaHelp = '''the expression will be applied to modify each value of the plot data.
Useable variables:
i: current index of the value, start from 0
val: ith value of the current index, equals to label(i), label here is the label name you set at required parameter.
variableName: will get the value of variable that has this name. Add the variable before this action otherwise it won't work.
plotDataName(index, default): will get the indexth value of plot data with this name. default is the default value if index out of range.
    if the plot data is not this one, add the plot data before this action otherwise it won't work.
Example: 
    plot data: {x:[1,2,1,3,1,4]}
    label: x
    start Turn: 2
    end Turn: 2
    funcString: val < x(i-1, 0)
    calculation when i = 0: 1 < 0, return False, turn count = 1
                when i = 1: 2 < 1, return False, turn count = 1
                when i = 2: 1 < 2, return True, turn count = 2, truncate data with index < 2
                ...
    final result: [1, 3]
'''

# ==========================
# action parameters
# ==========================
empty = {'rParam':{}, 'oParam':{}}
formatRawData = { 'func': 'formatRawData',
    'rParam':{
        'spliter': {'term': 'Split Text', 'type': str, 'option': {'Tab': '\t', 'Comma':',', 'Text': True}, 'desc':'use this parameter to split each row of data'}}, 
    'oParam':{
        'starter': {'term': 'Start Text', 'type': str, 'Text': True, 'desc':'if a line contains this parameter, start data collection(inclusive)'},
        'ender': {'term': 'End Text', 'type': str, 'Text': True, 'desc':'if a line contains this parameter, end data collection(exclusive)'},
        'maxLine': {'term': 'Max line', 'type': int, 'Text': QIntValidator(), 'desc':'the max number of lines to import'}}}

addVariable = { 'func': 'createVariable',
    'rParam':{
        'name':{'term':'Variable Name', 'type': str, 'Text': nameValidator, 'desc':'set the name of your variable, it cannot contain space and cannot be a number'},
        'value':{'term':'Variable Value', 'type': float, 'Text': QDoubleValidator(), 'desc':'set the value of your variable, it must be a number'}},
    'oParam':{}}

createPlotData = { 'func': 'createPlotData',
    'rParam':{
        'key':{'term':'Title', 'type': str, 'Text': True, 'desc':'Get data from the corresponding title'},
        'label':{'term':'Name', 'type': str, 'Text': nameValidator, 'desc':'Set the name of this plot data.'}},
    'oParam':{
        'funcString':{'term':'function', 'type': str, 'Text': True, 'desc':formulaHelp},
        'sigfig':{'term':'Sigfig', 'type': int, 'Text': QIntValidator(1, 100), 'desc':'set sig fig of the plot data'}}}

modifyPlotData = { 'func': 'modifyPlotDataValues',
    'rParam':{
        'label':{'term':'Name', 'type': str, 'Text': nameValidator, 'desc':'the name of plot data to modify.'},
        'funcString':{'term':'function', 'type': str, 'Text': True, 'desc':formulaHelp}},
    'oParam':{}}

truncateByValue = { 'func': 'truncatePlotDataByValue',
    'rParam':{
        'label':{'term':'Plot Data Name', 'type': str, 'Text': nameValidator, 'desc': 'the name of plot data used to determine data range by value'},
        'inputLabels':{'term':'Input', 'type': nameList, 'Text':nameListValidator, 'desc': 'the name of input plot data that are about to truncate'}}, 
    'oParam':{
        'outputLabels':{'term':'Output', 'type': nameList, 'Text': nameListValidator, 'desc': 'a list of plot data name for truncate output, if disabled the data will overwrite the input plot data.'},
        'startValue': {'term':'Start Value', 'type':float, 'Text':QDoubleValidator(),'desc': 'truncate data before the start value.'},
        'endValue': {'term':'End Value', 'type':float, 'Text':QDoubleValidator(),'desc': 'truncate data after the end value.'}}}

truncateByTurn = { 'func': 'truncatePlotDataByTurn',
    'rParam':{
        'label':{'term':'Plot Data Name', 'type': str, 'Text': nameValidator, 'desc': 'the name of plot data used to determine data range by Turn'},
        'turnHandlerString':{'term':'function', 'type':str, 'Text': True, 'desc': turnFormulaHelp},
        'inputLabels':{'term':'Input', 'type': nameList, 'Text':nameListValidator, 'desc': 'the name of input plot data that are about to truncate'}}, 
    'oParam':{
        'outputLabels':{'term':'Output', 'type': nameList, 'Text': nameListValidator, 'desc': 'a list of plot data name for truncate output, if disabled the data will overwrite the input plot data.'},
        'startTurn': {'term':'Start Turn', 'type':int, 'Text':QIntValidator(),'desc': 'truncate data before the start turn, if disabled start at turn one.'},
        'endTurn': {'term':'End Turn', 'type':int, 'Text':QIntValidator(),'desc': 'truncate data after the end value, if disabled end after turn one.'}}}

filterByFunc = { 'func': 'filterPlotDataByFunc',
    'rParam':{
        'label':{'term':'Plot Data Name', 'type': str, 'Text': nameValidator, 'desc': 'the name of plot data used to determine data range by Turn'},
        'inputLabels':{'term':'Input', 'type': nameList, 'Text':nameListValidator, 'desc': 'the name of input plot data that are about to truncate'}, 
        'funcString':{'term':'function', 'type': str, 'Text':True, 'desc': 'the function to do filtering'}}, 
    'oParam':{
        'outputLabels':{'term':'Output', 'type': nameList, 'Text': nameListValidator, 'desc': 'a list of plot data name for truncate output, if disabled the data will overwrite the input plot data.'}}}

# ==========================
# action Dictionary
# ==========================
MNGACTIONDICT = {
    'Choose Action': empty ,
    'Format Raw Data':formatRawData,
    'Add Variable':addVariable,
    'Create Plot Data':createPlotData,
    'Modify Plot Data':modifyPlotData,
    'Truncate Plot Data By Value':truncateByValue,
    'Truncate Plot Data By Turn':truncateByTurn,
    'Fliter Plot Data By Function':filterByFunc
    }