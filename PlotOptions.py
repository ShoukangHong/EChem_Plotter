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
    'oParam':{}}

setYAxLabel = { 'func': 'setYAxLabel',
    'rParam':{
        'label': {'term': 'label', 'type': str, 'Text':True, 'desc':'Set the label of active y axis'}},
    'oParam':{}}

setTitle = { 'func': 'setTitle',
    'rParam':{
        'title': {'term': 'title', 'type': str, 'Text':True, 'desc':'Set the title of active figure'}},
    'oParam':{}}

plot = { 'func': 'plot',
    'rParam':{
        'xDataLabel':{'term': 'xDataLabel', 'type': str, 'Text':nameValidator, 'desc':'choose the x label to plot'},
        'yDataLabel':{'term': 'yDataLabel', 'type': str, 'Text':nameValidator, 'desc':'choose the y label to plot'}},
    'oParam':{
        'style':{'term':'style', 'type': str, 'Text': True, 'desc': 'set the style of plot.'},
        'xDataManagerIndex': {'term': 'xDataManagerIndex', 'type': int, 'Text':QIntValidator(0,20), 'desc':' Get x plotdata from data manager with this index. If not specified, use active data manager.'},
        'yDataManagerIndex': {'term': 'yDataManagerIndex', 'type': int, 'Text':QIntValidator(0,20), 'desc':' Get y plotdata from data manager with this index. If not specified, use active data manager.'},
        'label': {'term': 'legend Name', 'type': str, 'Text':True, 'desc':' the legend that will be desplayed'}}}

showLegends = { 'func': 'showLegends',
    'rParam':{},
    'oParam':{'loc':{'term': 'legend Location', 'type': str, 'option': {'ur':'upper right', 'ul':'upper left', 'll': 'lower left', 'lr':'lower right', 'r': 'right', 'l': 'center left'}, 'desc':' the legend position ulrl refers to up, low, right left'}}}
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
    'Show Legends': showLegends 
}