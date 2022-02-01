# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:25:23 2021

@author: shouk
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import EIS_process as EIS
import numpy as np
import math


def plotEIS(filePath, fileName, rounds = [1], legend = '', style = '-'):
    # arguments: filename, filepath, rounds = [1], legend, style = 'o'
    graph1 = EIS.EIS_plot(fileName, filePath, rounds, legend, style =style)
    print(graph1)
    graph1.plot()
    #plt.title("Simple Plot")

filePath =  'C:/STUDY/research data/All-in-one/PEO-AAO-EIS/07282021-bareAAO-gold-EIS/'

#plotEIS(filePath, 'SH_PEO-ACN_64-1_AAO-EIS_18C-08242021_C04', [1], '18 \N{DEGREE SIGN}C');
#plotEIS(filePath, 'SH_PEO-ACN_64-1_AAO-EIS_30C-08242021_C04', [1], '30 \N{DEGREE SIGN}C');
#plotEIS(filePath, 'SH_PEO-ACN_64-1_AAO-EIS_40C-08242021_C04', [2], '40 \N{DEGREE SIGN}C');
#plotEIS(filePath, 'SH_PEO-ACN_64-1_AAO-EIS_50C-08242021_C04', [1], '50 \N{DEGREE SIGN}C');
#plotEIS(filePath, 'SH_PEO-ACN_64-1_AAO-EIS_60C-08052021_C04', [2], '60 \N{DEGREE SIGN}C');
plotEIS(filePath,
        'SH-bareAAO-EIS-07282021_C04', [1], 'bare AAO');
plotEIS(filePath,
        'SH-bareAAO-gold-2min-EIS-07282021_C04', [1], 'AAO-gold-2 min');
plotEIS(filePath,
        'SH-plastic_plate-EIS-07282021_C04', [1], 'plastic plate');

save = True
savePath = filePath
saveName = 'AAO EIS compare'
saveformat = '.tif'
resolution = 300
plt.title('AAO EIS compare')
boundY = 100000
boundX = 10000
plt.axis([0, boundX, 0, boundY])
plt.legend(loc = "lower right")



if save:
    plt.savefig(savePath + saveName + saveformat, dpi=resolution, bbox_inches="tight")