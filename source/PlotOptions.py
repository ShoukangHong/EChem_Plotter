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

def kwDict(string):
    result = eval('{' + string+'}')
    if isinstance(result, dict):
        return result
    raise ValueError("'" + string + "'" + " is not a valid keyword dictionary string")
    
# ==========================
# help texts
# ==========================
styleHelp = '''Set marker, line and color with this parameter.
Format: '[marker][line][color]'  (Each of them is optional, '' is not needed)
Example: 'or' means circle+red, '+-b' means plus marker + solid line style + blue
Markers:
    '.' point marker
    'o' circle marker
    '^' triangle_up marker
    's' square marker
    '*' star marker
    '+' plus marker
    'x' x marker
    'D' diamond marker
Lines:
    '-' solid line style
    '--' dashed line style
    '-.' dash-dot line style
    ':' dotted line style
Colors:
    'b' blue
    'g' green
    'r' red
    'c' cyan
    'm' magenta
    'y' yellow
    'k' black
    'w' white
'''
scriptHelp = '''Directly write script to excecute.
can use these variables:
    plotter: Class(EchemPlotter),
    self: Class(PlotTabWidget)

Please refer to the source code for more information
'''

keyWordHelp = '''Advanced keyword arguments,
Please use this format:
    key1:value1, key2: value2, ...
    
Please refer to matplotlib documentation: '''

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
        'index': {'term': 'Data Manager Index', 'type': int, 'Text':QIntValidator(0,20), 'desc':'Set the data manager to get plot data from, count start from 0'}}, 
    'oParam':{}}

setActiveAx = { 'func': 'setActiveAx',
    'rParam':{
        'index': {'term': 'Axis Index', 'type': int, 'Text':QIntValidator(0,20), 'desc':'Set the axis, count start from 0'}}, 
    'oParam':{
        'twin': {'term': 'Twin', 'type': str, 'option': {'x': 'x', 'y':'y'}, 'desc':'Select the twin Axes that shares the chosen axis'}}}

addTwinX = { 'func': 'addTwinX',
    'rParam':{},
    'oParam':{}}

addTwinY = { 'func': 'addTwinX',
    'rParam':{},
    'oParam':{}}

setXAxLabel = { 'func': 'setXAxLabel',
    'rParam':{
        'label': {'term': 'Label', 'type': str, 'Text':True, 'desc':'Set the label of active x axis'}},
    'oParam':{'fontsize':{'term': 'Font size', 'type': int, 'Text':QIntValidator(1,999), 'desc':'Set font size'},
              'kwParams':{'term': 'Keyword parameters', 'type': kwDict, 'Text':True, 'desc': keyWordHelp + 'matplotlib.axes.Axes.set_xlabel'}}}

setYAxLabel = { 'func': 'setYAxLabel',
    'rParam':{
        'label': {'term': 'Label', 'type': str, 'Text':True, 'desc':'Set the label of active y axis'}},
    'oParam':{'fontsize':{'term': 'Font size', 'type': int, 'Text':QIntValidator(1,999), 'desc':'Set font size'},
              'kwParams':{'term': 'Keyword parameters', 'type': kwDict, 'Text':True, 'desc': keyWordHelp + 'matplotlib.axes.Axes.set_ylabel'}}}

setTitle = { 'func': 'setTitle',
    'rParam':{
        'title': {'term': 'Title', 'type': str, 'Text':True, 'desc':'Set the title of active figure'}},
    'oParam':{'fontsize':{'term': 'Font size', 'type': int, 'Text':QIntValidator(1,999), 'desc':'Set font size'},
        'kwParams':{'term': 'Keyword parameters', 'type': kwDict, 'Text':True, 'desc': keyWordHelp + 'matplotlib.axes.Axes.set_title'}}}

plot = { 'func': 'plot',
    'rParam':{
        'xDataLabel':{'term': 'X Axis Label', 'type': str, 'Text':nameValidator, 'desc':'choose the x label to plot'},
        'yDataLabel':{'term': 'Y Axis Label', 'type': str, 'Text':nameValidator, 'desc':'choose the y label to plot'}},
    'oParam':{
        'style':{'term':'style', 'type': str, 'Text': True, 'desc': styleHelp},
        'xDataManagerIndex': {'term': 'X Data Manager Index', 'type': int, 'Text':QIntValidator(0,20), 'desc':' Get x plotdata from data manager with this index. If not specified, use active data manager.'},
        'yDataManagerIndex': {'term': 'Y Data Manager Index', 'type': int, 'Text':QIntValidator(0,20), 'desc':' Get y plotdata from data manager with this index. If not specified, use active data manager.'},
        'label': {'term': 'Legend', 'type': str, 'Text':True, 'desc':' the legend that will be desplayed'},
        'kwParams':{'term': 'Keyword parameters', 'type': kwDict, 'Text':True, 'desc': keyWordHelp + 'matplotlib.axes.Axes.plot'}}}

setScale = { 'func': 'setAxScale',
    'rParam':{},
    'oParam':{'left':{'term': 'Left', 'type': float, 'Text':QDoubleValidator(), 'desc':' the left position'},
              'right':{'term': 'Right', 'type': float, 'Text':QDoubleValidator(), 'desc':' the right position'},
              'bottom':{'term': 'Bottom', 'type': float, 'Text':QDoubleValidator(), 'desc':' the bottom position'},
              'top':{'term': 'Top', 'type': float, 'Text':QDoubleValidator(), 'desc':' the top position'},
              'leftBlank':{'term': 'Left Blank Ratio', 'type': float, 'Text':QDoubleValidator(), 'desc':' the left blank ratio'},
              'rightBlank':{'term': 'Right Blank Ratio', 'type': float, 'Text':QDoubleValidator(), 'desc':' the right blank ratio'},
              'bottomBlank':{'term': 'Bottom blank Ratio', 'type': float, 'Text':QDoubleValidator(), 'desc':' the bottom blank ratio'},
              'topBlank':{'term': 'Top Blank Ratio', 'type': float, 'Text':QDoubleValidator(), 'desc':' the top blank ratio'}}}

setTickInterval = { 'func': 'setTickInterval',
    'rParam':{'axisType':{'term': 'Axis Type', 'type': str, 'option': {'x':'x', 'y':'y'}, 'desc':' the axis to modify'}},
    'oParam':{'interval':{'term': 'Interval', 'type': float, 'Text':QDoubleValidator(), 'desc':'set interval value for each tick, cannot use with Tick Number'},
              'tickNum':{'term': 'Tick Number', 'type': int, 'Text':QIntValidator(0,999), 'desc':'Target number of ticks. Will determine interval based on this value. The final tick number may not be exactly the tickNumber, because tick increments needs to be 1, 2 or 5 *10^x.'},
              'minor':{'term': 'Minor Interval', 'type': int, 'Text':QIntValidator(0,10), 'desc':'minor tick number, default is disabled, set 0 will use auto minor tick, otherwise will have the (number - 1) of minor tick'},
              'realign':{'term': 'Realign', 'type': str, 'option': {'start':'s', 'end':'e', 'both':'se'}, 'desc':'realign start/end or start and end point after setting the interval'}}}

showLegends = { 'func': 'showLegends',
    'rParam':{},
    'oParam':{'loc':{'term': 'Legend Location', 'type': str, 'option': {'ur':'upper right', 'ul':'upper left', 'll': 'lower left', 'lr':'lower right', 'r': 'right', 'l': 'center left'}, 'desc':' the legend position ulrl refers to up, low, right left'},
              'kwParams':{'term': 'Keyword parameters', 'type': kwDict, 'Text':True, 'desc': keyWordHelp + 'matplotlib.axes.Axes.legend'}}}

note = { 'func': 'note',
    'rParam':{'note': {'term': 'Note', 'type': str, 'Text':True, 'desc':'Write some notes to explain things'}},
    'oParam':{}}

script = { 'func': 'script',
    'rParam':{'script': {'term': 'Script', 'type': str, 'Text':True, 'desc':scriptHelp}},
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