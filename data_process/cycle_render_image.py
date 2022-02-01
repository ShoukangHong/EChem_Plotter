# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import cycle_process as cycle
'''
filepath =  ''
filename = 'testdoc2'
filetype = '.mpt'

savepath = 'C:/STUDY/'
savename = 'test'
saveformat = '.png'
resolution = 300

graph = cycle.cycle_plot(filename, filepath, file_type = '.mpt', plot_number = 1000, rounds = 100, legend = 'Li-Li', style = 'b-')
'''

filepath =  'C:/STUDY/research data/All-in-one/AAO-V2O5Cycle/11052021-200nmAAO-V2O5-400_gold-2min/'
filename = '11052021-200nmAAO-V2O5-400_gold-2min_01_CP_C02'
filetype = '.txt'

savepath = 'C:/STUDY/research data/All-in-one/AAO-V2O5Cycle/11052021-200nmAAO-V2O5-400_gold-2min/'
savename = '11052021-200nmAAO-V2O5-400_gold-2min_01_CP_C02'
saveformat = '.png'
resolution = 300

graph = cycle.cycle_plot(filename, filepath, file_type = filetype, plot_number = 1000, rounds = 1, legend = 'Li-Li', style = 'b-')

graph.plot()
plt.legend(loc = "upper left")
plt.xlabel("Time / h", fontsize='large')
plt.ylabel('Voltage / V', fontsize='large')
plt.autoscale(enable=True, axis='x', tight=True)
plt.axis([0, None, None, None])

plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")


'''
graph.plot()
plt.legend(loc = "upper left")
plt.xlabel("Time / h", fontsize='large')
plt.ylabel('Voltage / V', fontsize='large')
plt.autoscale(enable=True, axis='x', tight=True)
plt.axis([0, None, None, None])

plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")
'''