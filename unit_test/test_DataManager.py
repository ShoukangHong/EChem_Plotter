# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:56:14 2022

@author: shouk
"""
import sys
sys.path.append("..")
from data_process import Plotter_Core
 
class DataManagerTester:
    def __init__(self):
        self.testLoadDocInfo();
    
    def testLoadDocInfo(self):
        rawAddresses = ['', 'C:\\ab\cd/ef.g','!@#$%^&*()_+','C:\none\null.false.undefined',
                     r'C:\Users\shouk\Github\EChem_Plotter\test_data\EIS\Li-Li_polished_PEO_EO-LiTFSI_20-1_0_05mm_600000MW_50celcius_Sh_01132021_C06.txt']
        answers = [['','/','','.'],
                   ['C:/ab/cd/ef.g', 'C:/ab/cd/', 'ef', '.g'],
                   ['!@#$%^&*()_+', '/', '', '.!@#$%^&*()_+'],
                   ['C:/none/null.false.undefined', 'C:/none/', 'null.false', '.undefined'],
                   ['C:/Users/shouk/Github/EChem_Plotter/test_data/EIS/Li-Li_polished_PEO_EO-LiTFSI_20-1_0_05mm_600000MW_50celcius_Sh_01132021_C06.txt',
                    'C:/Users/shouk/Github/EChem_Plotter/test_data/EIS/', 'Li-Li_polished_PEO_EO-LiTFSI_20-1_0_05mm_600000MW_50celcius_Sh_01132021_C06', '.txt']]
        for i, rawAddress in enumerate(rawAddresses):
            dataManager = Plotter_Core.DataManager(rawAddress)
            assert dataManager.docInfo('address') == answers[i][0], "expected: " + answers[i][0] + ", yours: " + dataManager.docInfo('address')
            assert dataManager.docInfo('path') == answers[i][1], "expected: " + answers[i][1] + ", yours: " + dataManager.docInfo('path')
            assert dataManager.docInfo('name') == answers[i][2], "expected: " + answers[i][2] + ", yours: " + dataManager.docInfo('name')
            assert dataManager.docInfo('type') == answers[i][3], "expected: " + answers[i][3] + ", yours: " + dataManager.docInfo('type')
            print('test ' + str(i) + ' ...pass')
        address = Plotter_Core.DataManager(rawAddresses[-1]).docInfo('address')
        doc = open(address, 'r')
        text = doc.readlines()
        print('all test of LoadDocInfo passed!')