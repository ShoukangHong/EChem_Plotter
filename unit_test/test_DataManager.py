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
        rawAddresses = ['', 'C:\\ab\cd/ef.g','!@#$%^&*()_+','C:\none\null.undefined',
                     'D:\RPG\Github\EChem_Plotter\test_data\EIS\Li-Li_polished_PEO_EO-LiTFSI_20-1_0_05mm_600000MW_50celcius_Sh_01132021_C06.txt']
        answers = [['','/','','.'],
                   ['C:/ab/cd/ef.g', 'C:/ab/cd/', 'ef', '.g'],
                   ['!@#$%^&*()_+', '/', '', '.!@#$%^&*()_+'],
                   ['C:/none/null.undefined', 'C:/none/', 'null', '.undefined'],
                   ['D:/RPG/Github/EChem_Plotter/test_data/EIS/Li-Li_polished_PEO_EO-LiTFSI_20-1_0_05mm_600000MW_50celcius_Sh_01132021_C06.txt',
                    'D:/RPG/Github/EChem_Plotter/test_data/EIS/', 'Li-Li_polished_PEO_EO-LiTFSI_20-1_0_05mm_600000MW_50celcius_Sh_01132021_C06', '.txt']]
        for rawAddress in rawAddresses:
            dataManager = Plotter_Core.DataManager(rawAddress)
            print(dataManager.docInfo('address'),
                  dataManager.docInfo('path'),
                  dataManager.docInfo('name'),
                  dataManager.docInfo('type'))
            
        address = Plotter_Core.DataManager(rawAddresses[-1]).docInfo('address')
        doc = open(address, 'r')
        text = doc.readlines()
        print(text)
            
DataManagerTester()