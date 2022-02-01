# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math
import re

class EIS_plot:
    
    def __init__(self, file_name, file_path, rounds = [1], legend = None, style = 'o'):
        self._file = file_path + file_name + '.txt'
        self._freq_list = [[]]
        self._re_list = [[]]
        self._im_list = [[]]
        self._rounds = rounds
        self._style = style
        if legend == None:
            self._legend = file_name[:30]
        else:
            self._legend = legend
        self.read()
        
    def get_labels(self, head):
        head = head[:-1].split()
        self._label_re = head[1]
        self._label_im = head[2]
        
        
    def get_data(self, text):
        count = 0
        freq = math.inf
        for line in text:
            if not re.match('\d.', line):
                break
            line = line[:-1].split()
            new_freq = float(line[0])
            #print(new_freq, freq)
            if new_freq > freq:
                count += 1
                self._freq_list.append([])
                self._re_list.append([])
                self._im_list.append([])
            freq = new_freq
            self._freq_list[count].append(freq)
            self._re_list[count].append(float(line[1]))
            self._im_list[count].append( - float(line[2]))

            
    def read(self):
        raw = open(self._file, 'r')
        text = raw.readlines()
        head = text.pop(0)
        self.get_labels(head)
        self.get_data(text)
        
    def plot(self):
        #plt.xlabel(self._label_re)
        #plt.ylabel(self._label_im)
        count = 1
        for idx in self._rounds:
            if len(self._rounds) > 1:
                cur_legend = self._legend + '-' + str(count)
                count += 1
            else:
                cur_legend = self._legend
            plt.plot(self._re_list[idx - 1], self._im_list[idx - 1],
                     self._style, label = cur_legend)
        plt.xlabel("Z' / ohm", fontsize='large')
        plt.ylabel('- Z" / ohm', fontsize='large')
        #plt.legend()
        
    def __str__(self):
        string = ''
        for idx in range(len(self._re_list) - 1):
            string += 'real:' + str(idx + 1) + '\n'
            string += str(self._re_list[idx]) + '\n'
            string += 'image:' + str(idx + 1) + '\n'
            string += str(self._im_list[idx]) + '\n'
        return string
        
