# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math
import re

class cycle_plot:
    
    def __init__(self, file_name, file_path, file_type = '.mpt', plot_number = 1000, rounds = 1000, legend = None, style = '-'):
        self._file = file_path + file_name + file_type
        self._plot_number = plot_number
        self._t_list = []
        self._v_list = []
        self._rounds = rounds
        self._style = style
        if legend == None:
            self._legend = file_name[:30]
        else:
            self._legend = legend
        self.read()
        
    def get_index(self, head):
        head = head[:-1].split('\t')
        for idx in range(len(head)):
            if 'mode' in head[idx]:
                self._mode_idx = idx
            elif 'time' in head[idx]:
                self._t_idx = idx
            elif 'Ewe/V' in head[idx]:
                self._v_idx = idx
            elif 'cycle number' in head[idx]:
                self._cycle_idx = idx   
        
    def get_data(self, text):
        time_0 = 0
        for line in text:
            line = line[:-1].split('\t')
            if float(line[self._mode_idx]) == 3:
                time_0 = float(line[self._t_idx]) / 3600
                continue
            elif float(line[self._cycle_idx]) > self._rounds:
                break
            time = float(line[self._t_idx]) / 3600 - time_0
            volt = float(line[self._v_idx])
            self._t_list.append(time)
            self._v_list.append(volt)
            
    def read(self):
        raw = open(self._file, 'r', encoding = 'UTF-8', errors ='ignore')
        text = raw.readlines()
        head = text.pop(0)
        while not re.match('mode', head):
            head = text.pop(0)
        self.get_index(head)
        step = math.ceil(len(text) / self._plot_number)
        self.get_data(text[0::step])
        
    def plot(self):
        plt.plot(self._t_list, self._v_list,
                self._style, label = self._legend)
        
    def __str__(self):
        string = 'this is too large, str not available'
        return string