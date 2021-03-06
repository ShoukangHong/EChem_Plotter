# -*- coding: utf-8 -*-
"""
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
i: the current index of the list during iteration, count start from 0.
val: ith value of the current plot data label, equals to label(i), label here is the label name you set at required parameter.
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
i: the current index of the list during iteration, count start from 0.
val: ith value of the current plot data label, equals to label(i), label here is the label name you set at required parameter.
variableName: will get the value of variable that has this name. Add the variable before this action otherwise it won't work.
plotDataLabel(index, default): will get the indexth value of plot data with this name. default is the default value if index out of range.
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

filterFormulaHelp = '''the expression will be applied to filter data.
Useable variables:
i: the current index of the list during iteration, count start from 0.
val: ith value of the current plot data label, equals to label(i), label here is the label name you set at required parameter.
variableName: will get the value of variable that has this name. Add the variable before this action otherwise it won't work.
plotDataLabel(index, default): will get the indexth value of plot data with this name. default is the default value if index out of range.
    if the plot data is not this one, add the plot data before this action otherwise it won't work.
Example: 
    plot data: {x:[1,2,1,3,1,4]}
    label: x
    funcString: val < 3
    result: [1, 2, 1, 1]
'''

scriptHelp = '''Directly write script to excecute.
can use these variables:
    dataManager: Class(DataManager),
    self: Class(MngTabWidget)

Please refer to the source code for more information
'''

nameListHelp = '''
Format: label1, label2, label3, ...'''
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
        'key':{'term':'Keyword', 'type': str, 'Text': True, 'desc':'Get data from the corresponding title'},
        'label':{'term':'Label', 'type': str, 'Text': nameValidator, 'desc':'Set the name of this plot data.'}},
    'oParam':{
        'funcString':{'term':'Function', 'type': str, 'Text': True, 'desc':formulaHelp},
        'sigfig':{'term':'Sigfig', 'type': int, 'Text': QIntValidator(1, 100), 'desc':'set sig fig of the plot data'}}}

modifyPlotData = { 'func': 'modifyPlotDataValues',
    'rParam':{
        'label':{'term':'Label', 'type': str, 'Text': nameValidator, 'desc':'the name of plot data to modify.'},
        'funcString':{'term':'Function', 'type': str, 'Text': True, 'desc':formulaHelp}},
    'oParam':{}}

truncateByValue = { 'func': 'truncatePlotDataByValue',
    'rParam':{
        'label':{'term':'Plot Data Label', 'type': str, 'Text': nameValidator, 'desc': 'the name of plot data used to determine data range by value'},
        'inputLabels':{'term':'Input Labels', 'type': nameList, 'Text':nameListValidator, 'desc': 'the name of input plot data that are about to truncate. ' + nameListHelp}}, 
    'oParam':{
        'outputLabels':{'term':'Output Labels', 'type': nameList, 'Text': nameListValidator, 'desc': 'a list of plot data name for truncate output, if disabled the data will overwrite the input plot data. ' + nameListHelp},
        'startValue': {'term':'Start Value', 'type':float, 'Text':QDoubleValidator(),'desc': 'truncate data before the start value.'},
        'endValue': {'term':'End Value', 'type':float, 'Text':QDoubleValidator(),'desc': 'truncate data after the end value.'}}}

truncateByTurn = { 'func': 'truncatePlotDataByTurn',
    'rParam':{
        'label':{'term':'Plot Data Label', 'type': str, 'Text': nameValidator, 'desc': 'the name of plot data used to determine data range by Turn'},
        'turnHandlerString':{'term':'Function', 'type':str, 'Text': True, 'desc': turnFormulaHelp},
        'inputLabels':{'term':'Input Labels', 'type': nameList, 'Text':nameListValidator, 'desc': 'the name of input plot data that are about to truncate. ' + nameListHelp}}, 
    'oParam':{
        'outputLabels':{'term':'Output Labels', 'type': nameList, 'Text': nameListValidator, 'desc': 'a list of plot data name for truncate output, if disabled the data will overwrite the input plot data. ' + nameListHelp},
        'startTurn': {'term':'Start Turn', 'type':int, 'Text':QIntValidator(),'desc': 'truncate data before the start turn, if disabled start at turn one.'},
        'endTurn': {'term':'End Turn', 'type':int, 'Text':QIntValidator(),'desc': 'truncate data after the end value, if disabled end after turn one.'}}}

filterByFunc = { 'func': 'filterPlotDataByFunc',
    'rParam':{
        'label':{'term':'Plot Data Label', 'type': str, 'Text': nameValidator, 'desc': 'the name of plot data used to determine data range by Turn'},
        'inputLabels':{'term':'Input Labels', 'type': nameList, 'Text':nameListValidator, 'desc': 'the name of input plot data that are about to truncate. ' + nameListHelp}, 
        'funcString':{'term':'Function', 'type': str, 'Text':True, 'desc': filterFormulaHelp}}, 
    'oParam':{
        'outputLabels':{'term':'Output Labels', 'type': nameList, 'Text': nameListValidator, 'desc': 'a list of plot data name for truncate output, if disabled the data will overwrite the input plot data. ' + nameListHelp}}}

savePlotData = { 'func': 'savePlotData',
    'rParam':{}, 
    'oParam':{
        'labels':{'term':'Lables', 'type': nameList, 'Text':nameListValidator, 'desc': 'the name of plot data that are about to export, default is all plot data. ' + nameListHelp},
        'name': {'term':'Save Name', 'type':str, 'Text':nameValidator,'desc': 'the out put file name.'},
        'step': {'term':'Step', 'type':int, 'Text':QIntValidator(1,1000),'desc': 'step of each data saved, defult is 1, which means no data will be skipped. Set high to reduce file size(but will lose some data)'}}}

note = { 'func': 'note',
    'rParam':{'note': {'term': 'Note', 'type': str, 'Text':True, 'desc':'Write some notes to explain things'}},
    'oParam':{}}

script = { 'func': 'script',
    'rParam':{'script': {'term': 'Script', 'type': str, 'Text':True, 'desc': scriptHelp}},
    'oParam':{}}

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
    'Fliter Plot Data By Function':filterByFunc,
    'Save Plot Data': savePlotData,
    'Note' : note,
    'Script': script
    }