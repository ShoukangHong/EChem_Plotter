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

def kwDict(string):
    result = eval('{' + string+'}')
    if isinstance(result, dict):
        return result
    raise ValueError("'" + string + "'" + " is not a valid keyword dictionary string")

# ==========================
# help texts
# ==========================

# ==========================
# action parameters
# ==========================
empty = {'rParam':{}, 'oParam':{}}

newFigure = { 'func': 'newFigure',
    'rParam':{}, 
    'oParam':{
        'nrows':{'term':'Number of Rows', 'type': int, 'Text': QIntValidator(1,5), 'desc': 'Number of rows of the subplot grid.'},
        'ncols': {'term':'Number of Columns', 'type': int, 'Text': QIntValidator(1,5), 'desc': 'Number of columns of the subplot grid.'}}}

setActiveDataManager = { 'func': 'setActiveDataManager',
    'rParam':{
        'index': {'term': 'index', 'type': int, 'Text':QIntValidator(0,20), 'desc':'Set the manager to plot, start from 0'}}, 
    'oParam':{}}

setActiveAx = { 'func': 'setActiveAx',
    'rParam':{
        'index': {'term': 'index', 'type': int, 'Text':QIntValidator(0,20), 'desc':'Set the axis, start from 0'}}, 
    'oParam':{
        'twin': {'term': 'twin', 'type': str, 'option': {'x': 'x', 'y':'y'}, 'desc':'Set the twin axis'}}}

addTwinX = { 'func': 'addTwinX',
    'rParam':{},
    'oParam':{}}

addTwinY = { 'func': 'addTwinX',
    'rParam':{},
    'oParam':{}}

setXAxLabel = { 'func': 'setXAxLabel',
    'rParam':{
        'label': {'term': 'label', 'type': str, 'Text':True, 'desc':'Set the label of active x axis'}},
    'oParam':{'fontsize':{'term': 'Font size', 'type': int, 'Text':QIntValidator(1,999), 'desc':'Set font size'},
              'kwParams':{'term': 'keyword parameters', 'type': kwDict, 'Text':True, 'desc':'advanced keyword arguments'}}}

setYAxLabel = { 'func': 'setYAxLabel',
    'rParam':{
        'label': {'term': 'label', 'type': str, 'Text':True, 'desc':'Set the label of active y axis'}},
    'oParam':{'fontsize':{'term': 'Font size', 'type': int, 'Text':QIntValidator(1,999), 'desc':'Set font size'},
              'kwParams':{'term': 'keyword parameters', 'type': kwDict, 'Text':True, 'desc':'advanced keyword arguments'}}}

setTitle = { 'func': 'setTitle',
    'rParam':{
        'title': {'term': 'title', 'type': str, 'Text':True, 'desc':'Set the title of active figure'}},
    'oParam':{'fontsize':{'term': 'Font size', 'type': int, 'Text':QIntValidator(1,999), 'desc':'Set font size'},
        'kwParams':{'term': 'keyword parameters', 'type': kwDict, 'Text':True, 'desc':'advanced keyword arguments'}}}

plot = { 'func': 'plot',
    'rParam':{
        'xDataLabel':{'term': 'xDataLabel', 'type': str, 'Text':nameValidator, 'desc':'choose the x label to plot'},
        'yDataLabel':{'term': 'yDataLabel', 'type': str, 'Text':nameValidator, 'desc':'choose the y label to plot'}},
    'oParam':{
        'style':{'term':'style', 'type': str, 'Text': True, 'desc': 'set the style of plot.'},
        'xDataManagerIndex': {'term': 'xDataManagerIndex', 'type': int, 'Text':QIntValidator(0,20), 'desc':' Get x plotdata from data manager with this index. If not specified, use active data manager.'},
        'yDataManagerIndex': {'term': 'yDataManagerIndex', 'type': int, 'Text':QIntValidator(0,20), 'desc':' Get y plotdata from data manager with this index. If not specified, use active data manager.'},
        'label': {'term': 'legend Name', 'type': str, 'Text':True, 'desc':' the legend that will be desplayed'},
        'kwParams':{'term': 'keyword parameters', 'type': kwDict, 'Text':True, 'desc':'advanced keyword arguments'}}}

setScale = { 'func': 'setAxScale',
    'rParam':{},
    'oParam':{'left':{'term': 'left', 'type': float, 'Text':QDoubleValidator(), 'desc':' the left position'},
              'right':{'term': 'right', 'type': float, 'Text':QDoubleValidator(), 'desc':' the right position'},
              'bottom':{'term': 'bottom', 'type': float, 'Text':QDoubleValidator(), 'desc':' the bottom position'},
              'top':{'term': 'top', 'type': float, 'Text':QDoubleValidator(), 'desc':' the top position'},
              'leftBlank':{'term': 'left blank', 'type': float, 'Text':QDoubleValidator(), 'desc':' the left blank ratio'},
              'rightBlank':{'term': 'right blank', 'type': float, 'Text':QDoubleValidator(), 'desc':' the right blank ratio'},
              'bottomBlank':{'term': 'bottom blank', 'type': float, 'Text':QDoubleValidator(), 'desc':' the bottom blank ratio'},
              'topBlank':{'term': 'top blank', 'type': float, 'Text':QDoubleValidator(), 'desc':' the top blank ratio'}}}

setTickInterval = { 'func': 'setTickInterval',
    'rParam':{'axisType':{'term': 'Axis Type', 'type': str, 'option': {'x':'x', 'y':'y'}, 'desc':' the axis to modify'}},
    'oParam':{'interval':{'term': 'Interval', 'type': float, 'Text':QDoubleValidator(), 'desc':'set interval value for each tick, cannot use with Tick Number'},
              'tickNum':{'term': 'Tick Number', 'type': int, 'Text':QIntValidator(0,999), 'desc':'Target number of ticks. Will determine interval based on this value. The final tick number may not be exactly the tickNumber, because tick increments needs to be 1, 2 or 5 *10^x.'},
              'minor':{'term': 'Minor Interval', 'type': int, 'Text':QIntValidator(0,10), 'desc':'minor tick number, default is disabled, set 0 will use auto minor tick, otherwise will have the (number - 1) of minor tick'},
              'realign':{'term': 'Realign', 'type': str, 'option': {'start':'s', 'end':'e', 'both':'se'}, 'desc':'realign start/end or start and end point after setting the interval'}}}

showLegends = { 'func': 'showLegends',
    'rParam':{},
    'oParam':{'loc':{'term': 'legend Location', 'type': str, 'option': {'ur':'upper right', 'ul':'upper left', 'll': 'lower left', 'lr':'lower right', 'r': 'right', 'l': 'center left'}, 'desc':' the legend position ulrl refers to up, low, right left'},
              'kwParams':{'term': 'keyword parameters', 'type': kwDict, 'Text':True, 'desc':'advanced keyword arguments'}}}

note = { 'func': 'note',
    'rParam':{'note': {'term': 'note', 'type': str, 'Text':True, 'desc':'Write some notes to explain things'}},
    'oParam':{}}

script = { 'func': 'script',
    'rParam':{'script': {'term': 'script', 'type': str, 'Text':True, 'desc':'Directly Write code to excecute'}},
    'oParam':{}}
# ==========================
# action Dictionary
# ==========================
PLOTACTIONDICT = {
    'Choose Action': empty,
    'Create New Figure':newFigure,
    'Set Active Data Manager':setActiveDataManager,
    'Set Active Axis':setActiveAx,
    'Add Twin X and set Active':addTwinX,
    'Add Twin Y and set Active':addTwinY,
    'Set X Axis Label': setXAxLabel,
    'Set Y Axis Label': setYAxLabel,
    'Set Title': setTitle,
    'Plot':plot,
    'Set Scale': setScale,
    'Set Tick Interval': setTickInterval,
    'Show Legends': showLegends,
    'Note' : note,
    'Script': script
}