# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math
import re


class capacity_plot:
    
    def __init__(self, file_name, file_path, weigth, legend_cap, legend_eff, file_type='.mpt', rounds=1000, style_cap='bo', style_eff='ro'):
        self._file = file_path + file_name + file_type
        self._weight = weigth
        self._cycle_list = []
        self._capacity_list = []
        self._efficiency_list = []
        self._rounds = rounds
        self._style_cap = style_cap
        self._style_eff = style_eff
        self._legend_cap = legend_cap
        self._legend_eff = legend_eff
        self.read()
        
    def get_index(self, head):
        head = head[:-1].split('\t')
        for idx in range(len(head)):
            if 'cycle number' in head[idx]:
                self._cycle_idx = idx
            elif 'Q discharge/mA.h' in head[idx]:
                self._capacity_idx = idx
            elif 'Efficiency/%' in head[idx]:
                self._efficiency_idx = idx
        
    def get_data(self, text):
        cycle = 0.0
        for line in text:
            line = line[:-1].split('\t')
            if float(line[self._cycle_idx]) == cycle:
                last_line = line
                continue
            elif float(line[self._cycle_idx]) > self._rounds:
                break
            cycle = float(line[self._cycle_idx])
            capacity = float(last_line[self._capacity_idx]) / self._weight
            efficiency = float(last_line[self._efficiency_idx])
            self._capacity_list.append(capacity)
            self._efficiency_list.append(efficiency)
            
    def read(self):
        raw = open(self._file, 'r', encoding = 'UTF-8', errors ='ignore')
        text = raw.readlines()
        head = text.pop(0)
        while not re.match('mode', head):
            head = text.pop(0)
        self.get_index(head)
        self.get_data(text)
        
    def plot(self, ax, ax2):
        ax.plot(range(1, len(self._capacity_list) + 1), self._capacity_list,
                self._style_cap, label = self._legend_cap)
        ax2.plot(range(1, len(self._efficiency_list) + 1), self._efficiency_list,
                self._style_eff, label = self._legend_eff)
        
    def __str__(self):
        return str(self._capacity_list) + '\n' + str(self._efficiency_list)

# back up method for get_data
# =============================================================================
#         cycle = 0.0
#         length = len(text)
#         step = length // 5000
#         for num in range(0, length, step):
#             line = text[num][:-1].split('\t')
#             if float(line[self._cycle_idx]) == cycle:
#                 continue
#             elif float(line[self._cycle_idx]) > self._rounds:
#                 break
#             else:
#                 idx = num
#                 while (float(line[self._cycle_idx])) != cycle:
#                     idx -= 1
#                     line = text[idx][:-1].split('\t')
#             cycle = float(line[self._cycle_idx]) + 1
#             capacity = float(line[self._capacity_idx]) * 100
#             efficiency = float(line[self._efficiency_idx])
#             self._capacity_list.append(capacity)
#             self._efficiency_list.append(efficiency)
# =============================================================================
