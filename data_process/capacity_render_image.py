# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import capacity_process as capacity

filepath =  'C:/STUDY/research data/2112 lab data/07232020-LiFePO4-TFEE-LPE20,F-LPE50/'
filename = 'Fluorinated_ether_LPE-20_0_35mLiTFSI-LiFePO4_1 M LiPF6_EC-DEC_0_5C-SH_01_C01'
filename2 = 'Fluorinated_ether_LPE-50_0_35mLiTFSI-LiFePO4_1 M LiPF6_EC-DEC_0_5C-SH_02_C03'
filetype = '.mpt'

active_material_weight = 0.00855     #unit is gram
active_material_weight2 = 0.00855    #unit is gram

savepath = 'C:/STUDY/'
savename = 'test'
saveformat = '.png'
resolution = 300

capacity_scale = 300
efficiency_scale = 120
cycle_number = 50

fig, ax = plt.subplots()
ax.axis([0, cycle_number, 0, capacity_scale])
ax2 = ax.twinx()
ax2.axis([None, None, 0, efficiency_scale])

# (file_name, file_path, legend_cap, legend_eff, file_type='.mpt', rounds=1000, style_cap='bo', style_eff='ro')
graph = capacity.capacity_plot(filename, filepath, active_material_weight, 'capacity', 'efficiency',
                               file_type = filetype, rounds = cycle_number, style_cap='bo', style_eff='ro')
graph2 = capacity.capacity_plot(filename2, filepath, active_material_weight2, 'capacity2', 'efficiency2',
                                file_type = filetype, rounds = cycle_number, style_cap='ro', style_eff='go')
graph.plot(ax, ax2)
graph2.plot(ax, ax2)

ax.legend(loc = "lower left")
ax2.legend(loc = "lower right")
ax.set_xlabel("Cycle number", fontsize='large')
ax.set_ylabel('Specific capacity / mAh g $^{-1}$', fontsize='large')
ax2.set_ylabel('Coulumbic Efficiency / %', fontsize='large')
#plt.autoscale(enable=True, axis='x', tight=True)

#plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")