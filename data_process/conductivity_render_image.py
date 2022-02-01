# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

conductivity = [-5.280805587, -5.114685586, -4.47389452, -3.591963283, -3.414525753, -3.212679761, -3.159576734]
inverse_k = [3.355704698, 3.194888179, 3.095975232, 3.003003003, 2.915451895, 2.83286119, 2.754820937]
k = [25, 40, 50 ,60, 70, 80, 90]
savepath = 'C:/STUDY/'
savename = 'test'
saveformat = '.png'
resolution = 300

capacity_scale = 300
efficiency_scale = 120
cycle_number = 50

fig, ax = plt.subplots()
ax.axis([25, 100, -5.5, -3])

# (file_name, file_path, legend_cap, legend_eff, file_type='.mpt', rounds=1000, style_cap='bo', style_eff='ro')
#graph2 = capacity.capacity_plot(filename2, filepath, active_material_weight2, 'capacity2', 'efficiency2',
#                               file_type = filetype, rounds = cycle_number, style_cap='ro', style_eff='go')

ax.plot(k, conductivity, label = 'PEO-LiTFSI')
plt.legend(loc = "upper left")
ax.set_xlabel("Temperature / \N{DEGREE SIGN}C", fontsize='large')
ax.set_ylabel('log(\u03C3 / S cm$^{-1}$)', fontsize='large')
plt.autoscale(enable=True, axis='x', tight=True)
plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")