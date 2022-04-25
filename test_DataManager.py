# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:56:14 2022

@author: shouk
"""
import sys
import math
import re
import time
import numpy
import Plotter_Core

class DataManagerTester:
    def __init__(self):
        self._dataManagers = []
        self._plotter = Plotter_Core.EchemPlotter()
        self._saveAddress = r'C:\Users\shouk\Github\EChem_Plotter\unit_test\expected_results'
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
            print('test address: ' + repr(rawAddresses[i]))
            dataManager = Plotter_Core.DataManager(rawAddress)
            assert dataManager.docInfo('address') == answers[i][0], "test "+ str(i+1) + " address fail, expected: " + answers[i][0] + ", yours: " + dataManager.docInfo('address')
            assert dataManager.docInfo('path') == answers[i][1], "test "+ str(i+1) + " path fail, expected: " + answers[i][1] + ", yours: " + dataManager.docInfo('path')
            assert dataManager.docInfo('name') == answers[i][2], "test "+ str(i+1) + " name fail, expected: " + answers[i][2] + ", yours: " + dataManager.docInfo('name')
            assert dataManager.docInfo('type') == answers[i][3], "test "+ str(i+1) + " type fail, expected: " + answers[i][3] + ", yours: " + dataManager.docInfo('type')
        address = Plotter_Core.DataManager(rawAddresses[-1]).docInfo('address')
        doc = open(address, 'r')
        text = doc.readlines()
        print('\nall test of LoadDocInfo passed!\n')
    
    def testDataProcess(self):
        '''test base case data and store them in self._dataManager for later tests'''
        rawAddresses = [r'C:\Users\shouk\Github\EChem_Plotter\test_data\BaseTest\linear.txt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\BaseTest\power.xlsx',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\BaseTest\sin.mpt']
        split = ['\t',None,'\t']
        start = ['x\ty','x',None]
        funcX = [lambda x:x+1, lambda x:x+1, lambda x:0.1*x]
        funcY = [lambda x:2*x, lambda x:x*x, lambda x:math.sin(x * math.pi)]
        lenghts = [30, 30, 60]
        end = ['these are some', None, None]
        for i, rawAddress in enumerate(rawAddresses):
            print('testing file: ' + rawAddress)
            dataManager = Plotter_Core.DataManager(rawAddress)
            dataManager.formatRawData(split[i], start[i], end[i])
            self._dataManagers.append(dataManager)
            assert len(dataManager.getData()) == lenghts[i], 'expected length: '+ str(lenghts[i]) + ', yours: ' + str(len(dataManager.getData()))
            colx = dataManager.getCol('x', 3)
            coly = dataManager.getCol(1, 4)
            for j in range(lenghts[i]):
                assert abs(colx[j] - funcX[i](j)) < 0.001, 'expected x: ' + str(funcX[i](j)) + ', yours: ' + str(colx[j])
                assert abs(coly[j] - funcY[i](colx[j]))<0.001, 'expected y: ' + str(funcY[i](colx[j])) + ', yours: ' + str(coly[j])
        print('\nformat data test passed!\n')
    
    def testPlotDataSet(self):
        '''excecute using'''
        stringsX = ['','-val','val * val']
        stringsY = ['val + 2 * x(i)','val - x(i) + 2 * num / number','val * x(i) * a * value']
        variables = [ {},{'num': 1, 'number': 3}, {'a': 2, 'value': 3}]
        funcX = [lambda x:x, lambda x:-x,lambda x:x**2]
        funcY = [lambda y, x: y + 2 * x,
                 lambda y, x: y - x + 2 * variables[1]['num'] / variables[1]['number'],
                 lambda y, x: y * x * variables[2]['a'] * variables[2]['value']]
        for i, dataManager in enumerate(self._dataManagers):
            print('testing file: ' + dataManager.docInfo('address'))
            for key, val in variables[i].items():
                dataManager.createVariable(key, val)
            dataManager.createPlotData('x', 'x', stringsX[i])
            dataManager.createPlotData('x', 'y', stringsY[i]) #use x as y
            beforeX = dataManager.getCol('x')
            afterX = dataManager.getPlotDataValues('x')
            beforeY = dataManager.getCol('x')
            afterY = dataManager.getPlotDataValues('y')
            for j in range(30):
                assert funcX[i](beforeX[j]) == afterX[j],'loop '+ str(j) + ', beforeX value: ' + str(beforeX[j]) + ', expected after value: ' + str(funcX[i](beforeX[j])) + ', yours: ' + str(afterX[j])
                assert funcY[i](beforeY[j], afterX[j]) == afterY[j],'loop '+ str(j) + ', beforeY value: ' + str(beforeY[j]) + ', expected after value: ' + str(funcY[i](beforeY[j], afterX[j])) + ', yours: ' + str(afterY[j])
        print('\nplot data test passed!\n')
    
    def testPlotter(self):
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.newFigure(2,1)
        seq = [0, 0, 1]
        for i, dataManager in enumerate(self._dataManagers):
            plotter.setActiveAx(seq[i])
            label = dataManager.docInfo('name')
            dataManager.createPlotData(0, 'x')
            dataManager.createPlotData(1, 'y')
            plotter.addDataManager(dataManager)
            if i < 2:
                plotter.plot('x', 'y', label = label)
            else:
                plotter.activeDataManager().truncatePlotDataByValue('x',('x', 'y'), None,1, 3)
                xData = plotter.activeDataManager().getPlotDataValues('x')
                yData = plotter.activeDataManager().getPlotDataValues('y')
                assert xData[0] == 1 and xData[-1] == 3, 'xData[0] = ' + str(xData[0]) + ', expected: 1.0, ' + 'xData[-1] = ' + str(xData[-1]) + ',  expected: 3.0'
                plotter.plot('x', 'y', label = label + ' x range 1-3')
                turnHandler = ' y(i-1) > y(i) and y(i) < y(i+1)'
                dataManager.createPlotData(0, label = 'x')
                dataManager.createPlotData(1, label = 'y')
                plotter.activeDataManager().truncatePlotDataByTurn('y', turnHandler, ('x', 'y'), None, 3, 3)
                xData = plotter.activeDataManager().getPlotDataValues('x')
                yData = plotter.activeDataManager().getPlotDataValues('y')
                assert xData[0] == 3.5 and xData[-1] == 5.5, 'xData[0] = ' + str(xData[0]) + ', expected: 3.5, ' + 'xData[-1] = ' + str(xData[-1]) + 'expected: 5.5'
                plotter.plot('x', 'y', label = label + ' turn 3')

            plotter.setXAxLabel('x Axis')
            plotter.setYAxLabel('y Axis')
            plotter.setAxScale(left = 0)
            plotter.showLegends()

        address = plotter.activeDataManager().formatAddress(self._saveAddress + r'\Basic.png') 
        #plotter.pyplot().savefig(address, dpi=300, bbox_inches="tight")
        print('Finish! check the plot! Linear and power are in upper plot, sin is in bottom plot with two parts!')
    
    def testSave(self):
        '''test save documents'''
        for i, dataManager in enumerate(self._dataManagers):
            dataManager.saveData(step = i + 1)
            dataManager.savePlotData(step = i + 1)
            
    def testRealData(self):
        self.testCACP()
        self.testCV()
        self.testCycle()
    
    def testCACP(self):
        start_time = time.time()
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.newFigure(2,1)
        rawAddresses = [r'C:\Users\shouk\Github\EChem_Plotter\test_data\CA\200nm-AAO-TiN-V2O5_Lithiate-2_02_CA_C04.txt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CA\AAO-TiN-V2O5_Lithiate_02_CA_C08.txt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CP\200nm-AAO-TiN-V2O5_Lithiate-2_01_CP_C04.txt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CP\AAO-TiN-V2O5_Lithiate_01_CP_C08.txt']
        labelY = ['I/mA', 'Ewe/V']
        for i, rawAddress in enumerate(rawAddresses):
            dataManager = Plotter_Core.DataManager(rawAddress)
            plotter.addDataManager(dataManager)
            plotter.setActiveAx(i//2)
            dataManager.formatRawData()
            if i >= 2:
                dataManager.createPlotData('time/s', label = 'time')
            else:
                dataManager.createPlotData('time/s', label = 'time', funcString = 'val - time(0, val)')
            dataManager.createPlotData(labelY[i//2])
            plotter.plot('time', labelY[i//2], label = dataManager.docInfo('name'))
            plotter.setXAxLabel('time/s')
            plotter.setYAxLabel(labelY[i//2])
            if i % 2 == 1:
                plotter.setAxScale(left = -1000)
                plotter.showLegends()
                plotter.setTickInterval('y', tickNum = 7, minor = True, realign = 'se')
        address = dataManager.formatAddress(self._saveAddress + r'\CACP.png') 
        #plotter.pyplot().savefig(address, dpi=600, bbox_inches="tight")
        print("testCACP takes %s seconds" % (time.time() - start_time))
        
    def testCV(self):
        start_time = time.time()
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.newFigure(1,1)
        rawAddresses = [r'C:\Users\shouk\Github\EChem_Plotter\test_data\CV\11142021-Li-EC-DMC-LiPF6-V2O5_CV_0_1mV_C02.mpt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CV\11142021-Li-PC-LiClO4-V2O5_CV-0_1mV_C04.mpt']
        name = ['Li-EC-DMC-LiPF6-V2O5', 'Li-PC-LiClO4-V2O5']
        for i, rawAddress in enumerate(rawAddresses):
            dataManager = Plotter_Core.DataManager(rawAddress)
            plotter.addDataManager(dataManager)
            dataManager.formatRawData(starter='mode')
            print(dataManager._header)
            dataManager.createPlotData('control/V')
            dataManager.createPlotData('<I>/mA')
            dataManager.createPlotData('cycle number')
            for j in range(2, 4):
                plotter.activeDataManager().truncatePlotDataByValue('cycle number', ('control/V', '<I>/mA'), ('v-'+str(j), 'I-'+str(j)), j, j)
                plotter.plot('v-'+str(j), 'I-'+str(j), label = name[i] + ' cy-' + str(j))
            #dataManager.savePlotData(labels = ['control/V', 'cycle number', '<I>/mA'])
            plotter.setXAxLabel('control/V')
            plotter.setYAxLabel('I/mA')
            plotter.showLegends()
        address = dataManager.formatAddress(self._saveAddress + r'\CV.png') 
        #plotter.pyplot().savefig(address, dpi=600, bbox_inches="tight")
        print("testCVtakes %s seconds" % (time.time() - start_time))
        
    def testCycle(self):
        start_time = time.time()
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.newFigure(2,1)
        rawAddress = r'C:\Users\shouk\Github\EChem_Plotter\test_data\Cycle\ACC_S_253_3_94mg_TFEE-DOL_3-1_1MLiTFSI_50cy_DME-DOL_0_35MLiTFSI_1wtLiNO3_0_5C_SHong_09242020.xls'
        name = 'ACC_S_pretreat-50'

        dataManager = Plotter_Core.DataManager(rawAddress, 1)
        plotter.addDataManager(dataManager)
        dataManager.formatRawData()
        dataManager.createPlotData('Step_Index', label = 'Step_Index')
        dataManager.createPlotData('Voltage', label = 'Voltage')
        dataManager.createPlotData('Test_Time', label = 'Test_Time')
        plotter.activeDataManager().truncatePlotDataByValue('Step_Index',('Test_Time', 'Voltage'), None, 2)
        dataManager.modifyPlotDataValues('Test_Time', funcString= '(val - Test_Time(0))/3600')
        plotter.plot('Test_Time', 'Voltage', label = name)
        plotter.setAxScale(left = 0, bottomBlank=0.1, topBlank=0.1)
        plotter.setTickInterval('x', tickNum=10, minor = True)
        plotter.setTickInterval('y', tickNum=5, realign = 'se')
        plotter.setXAxLabel('Time/h')
        plotter.setYAxLabel('Voltage/V')
        plotter.activeAx().set_title('Long term cycle')
        plotter.showLegends()
        
        dataManager = Plotter_Core.DataManager(rawAddress, 'Statistics_1-017')
        plotter.addDataManager(dataManager)
        dataManager.formatRawData()
        handlerCharge = '1000 * (val - Charge_Capacity(i - 1, 0))'
        handlerDischarge = '1000 * (val - Discharge_Capacity(i - 1, 0))'
        handlerEfficiency = '100 * Discharge_Capacity(i)/Charge_Capacity(i - 1, val)'
        dataManager.createPlotData('Cycle_Index', label = 'Cycle_Index')
        dataManager.createPlotData('Charge_Capacity','Charge_Capacity', handlerCharge)
        dataManager.createPlotData('Discharge_Capacity', 'Discharge_Capacity', handlerDischarge)
        dataManager.createPlotData('Discharge_Capacity', 'Efficiency', handlerEfficiency)
        dataManager.truncatePlotDataByValue('Cycle_Index' , ('Cycle_Index', 'Discharge_Capacity', 'Efficiency'), None, 2)
        plotter.setActiveAx(1)
        plotter.plot('Cycle_Index', 'Discharge_Capacity', label = name)
        plotter.setAxScale(left = 0, bottom = 0, topBlank=0.3)
        plotter.setTickInterval('y', tickNum=10, realign = 'se')
        plotter.setXAxLabel('Cycle')
        plotter.setYAxLabel('Capacity/mAh')
        plotter.addTwinX()
        plotter.setYAxLabel(r'Efficiency/%')
        plotter.plot('Cycle_Index', 'Efficiency', label = 'Efficiency', style = 'ro')
        plotter.setAxScale(bottom = 50, topBlank=0.1)
        plotter.setTickInterval('x', tickNum=7, minor = 2)
        plotter.setTickInterval('y', interval = 10, minor = 2)
        plotter.activeAx().set_title('Capacity degradation')
        plotter.showLegends()
        
        address = dataManager.formatAddress(self._saveAddress + r'\cycle.png')
        #pyplot.savefig(address, dpi=600, bbox_inches="tight")
        print("testCycletakes %s seconds" % (time.time() - start_time))
        
# =============================================================================
# rawAddresses = [r'C:\Users\shouk\Github\EChem_Plotter\test_data\CA\AAO-TiN-V2O5_Lithiate_02_CA_C08.txt',
#                         r'C:\Users\shouk\Github\EChem_Plotter\test_data\CP\AAO-TiN-V2O5_Lithiate_01_CP_C08.txt',
#                         r'C:\Users\shouk\Github\EChem_Plotter\test_data\CV\11142021-Li-PC-LiClO4-V2O5_CV-0_1mV_C04.mpt',
#                         r'C:\Users\shouk\Github\EChem_Plotter\test_data\Cycle\ACC_S_259_3_94mg_TFEE-DOL_1-1_1MLiTFSI_0cy_0_5C_SHong_09242020.xls']
# =============================================================================
if (__name__ == '__main__'):

    tester = DataManagerTester()
    tester.testDataProcess()
    tester.testPlotDataSet()
    #tester.testSave()
    tester.testPlotter()
    tester.testRealData()

    #DataManagerTester().testLoadDocInfo()
    
    # tester = DataManagerTester()
    # tester.testDataProcess()
    # tester.testPlotter()
    # tester.testRealData()

