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
sys.path.append("..")
from data_process import Plotter_Core

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
            spliter = dataManager.createSpliter(split[i])
            starter = dataManager.createStarter(start[i])
            ender = dataManager.createEnder(end[i])
            dataManager.formatRawData(spliter, starter, ender, 3)
            self._dataManagers.append(dataManager)
            assert len(dataManager.getData()) == lenghts[i], 'expected length: '+ lenghts[i] + ', yours: ' + str(len(dataManager.getData()))
            colx = dataManager.getCol('x')
            coly = dataManager.getCol(1)
            for j in range(lenghts[i]):
                assert abs(colx[j] - funcX[i](j)) < 0.001, 'expected x: ' + str(funcX[i](j)) + ', yours: ' + str(colx[j])
                assert abs(coly[j] - funcY[i](colx[j]))<0.001, 'expected y: ' + str(funcY[i](colx[j])) + ', yours: ' + str(coly[j])
        print('\nformat data test passed!\n')
        self.testPlotDataSet()
        
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
            dataManager.createPlotData('x', stringsX[i], label = 'x')
            dataManager.createPlotData('x', stringsY[i], label = 'y') #use x as y
            beforeX = dataManager.getCol('x')
            afterX = dataManager.getPlotDataValues('x')
            beforeY = dataManager.getCol('x')
            afterY = dataManager.getPlotDataValues('y')
            for j in range(30):
                assert funcX[i](beforeX[j]) == afterX[j],'loop '+ str(j) + ', beforeX value: ' + str(beforeX[j]) + ', expected after value: ' + funcX[i](beforeX[j]) + ', yours: ' + str(afterX[j])
                assert funcY[i](beforeY[j], afterX[j]) == afterY[j],'loop '+ str(j) + ', beforeY value: ' + str(beforeY[j]) + ', expected after value: ' + str(funcY[i](beforeY[j], afterX[j])) + ', yours: ' + str(afterY[j])
        print('\nplot data test passed!\n')
    
    def testPlotter(self):
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.setSubPlots(2,1)
        seq = [0, 0, 1]
        for i, dataManager in enumerate(self._dataManagers):
            label = dataManager.docInfo('name')
            dataManager.createPlotData(0, label = 'x')
            dataManager.createPlotData(1, label = 'y')
            plotter.addDataManager(dataManager)
            if i < 2:
                xData = plotter.activeDataManager().getPlotDataValues('x')
                yData = plotter.activeDataManager().getPlotDataValues('y')
                plotter.plot(xData, yData, axIndex = seq[i], legend = label)
            else:
                plotter.activeDataManager().setPlotRangeByValue('x', 1, 3)
                xData = plotter.activeDataManager().getPlotDataValues('x')
                yData = plotter.activeDataManager().getPlotDataValues('y')
                assert xData[0] == 1 and xData[-1] == 3, 'xData[0] = ' + str(xData[0]) + ', expected: 1.0, ' + 'xData[-1] = ' + str(xData[-1]) + ',  expected: 3.0'
                plotter.plot(xData, yData, axIndex = seq[i], legend = label + ' x range 1-3')
                turnHandler = ' y(i-1) > y(i) and y(i) < y(i+1)'
                plotter.activeDataManager().setPlotRangeByTurn('y', turnHandler, 3, 4)
                xData = plotter.activeDataManager().getPlotDataValues('x')
                yData = plotter.activeDataManager().getPlotDataValues('y')
                assert xData[0] == 3.5 and xData[-1] == 5.5, 'xData[0] = ' + str(xData[0]) + ', expected: 3.5, ' + 'xData[-1] = ' + str(xData[-1]) + 'expected: 5.5'
                plotter.plot(xData, yData, axIndex = seq[i], legend = label + ' turn 3')

            plotter.setXAxLabel('x Axis', axIndex = seq[i])
            plotter.setYAxLabel('y Axis', axIndex = seq[i])
            plotter.setAxScale(xStart = 0, axIndex = seq[i])
            plotter.showLegend(axIndex = seq[i])

        address = dataManager.formatAddress(self._saveAddress + r'\Basic.png') 
        plotter.pyplot().savefig(address, dpi=300, bbox_inches="tight")
        print('Finish! check the plot! Linear and power are in upper plot, sin is in bottom plot with two parts!')
        
    def testRealData(self):
        self.testCACP()
        self.testCV()
        self.testCycle()
    
    def testCACP(self):
        start_time = time.time()
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.newFig()
        plotter.setSubPlots(2,1)
        rawAddresses = [r'C:\Users\shouk\Github\EChem_Plotter\test_data\CA\200nm-AAO-TiN-V2O5_Lithiate-2_02_CA_C04.txt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CA\AAO-TiN-V2O5_Lithiate_02_CA_C08.txt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CP\200nm-AAO-TiN-V2O5_Lithiate-2_01_CP_C04.txt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CP\AAO-TiN-V2O5_Lithiate_01_CP_C08.txt']
        labelY = ['I/mA', 'Ewe/V']
        for i, rawAddress in enumerate(rawAddresses):
            dataManager = Plotter_Core.DataManager(rawAddress)
            plotter.addDataManager(dataManager)
            dataManager.formatRawData()
            dataManager.createPlotData('time/s')
            dataManager.createPlotData(labelY[i//2])
            xData = dataManager.getPlotDataValues('time/s')
            yData = dataManager.getPlotDataValues(labelY[i//2])
            plotter.plot(xData, yData, axIndex = i // 2, legend = dataManager.docInfo('name'))
            plotter.setXAxLabel('time/s', axIndex = i // 2)
            plotter.setYAxLabel(labelY[i//2], axIndex = i // 2)
            if i % 2 == 1:
                plotter.setAxScale(xStart = 0, axIndex = i // 2)
                plotter.showLegend(axIndex = i // 2)
        address = dataManager.formatAddress(self._saveAddress + r'\CACP.png') 
        plotter.pyplot().savefig(address, dpi=300, bbox_inches="tight")
        print("testCACP takes %s seconds" % (time.time() - start_time))
        
    def testCV(self):
        start_time = time.time()
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.newFig()
        plotter.setSubPlots(1,1)
        rawAddresses = [r'C:\Users\shouk\Github\EChem_Plotter\test_data\CV\11142021-Li-EC-DMC-LiPF6-V2O5_CV_0_1mV_C02.mpt',
                        r'C:\Users\shouk\Github\EChem_Plotter\test_data\CV\11142021-Li-PC-LiClO4-V2O5_CV-0_1mV_C04.mpt']
        name = ['Li-EC-DMC-LiPF6-V2O5', 'Li-PC-LiClO4-V2O5']
        for i, rawAddress in enumerate(rawAddresses):
            dataManager = Plotter_Core.DataManager(rawAddress)
            starter = dataManager.createStarter('mode')
            plotter.addDataManager(dataManager)
            dataManager.formatRawData(starter = starter)
            dataManager.createPlotData('cycle number')
            dataManager.createPlotData('control/V')
            dataManager.createPlotData('<I>/mA')
            for j in range(2, 4):
                plotter.activeDataManager().setPlotRangeByValue('cycle number' , j, j)
                xData = dataManager.getPlotDataValues('control/V')
                yData = dataManager.getPlotDataValues('<I>/mA')
                plotter.plot(xData, yData, legend = name[i] + ' cy-' + str(j))
            plotter.setXAxLabel('control/V')
            plotter.setYAxLabel('I/mA')
            plotter.showLegend()
        address = dataManager.formatAddress(self._saveAddress + r'\CV.png') 
        plotter.pyplot().savefig(address, dpi=300, bbox_inches="tight")
        print("testCVtakes %s seconds" % (time.time() - start_time))
        
    def testCycle(self):
        start_time = time.time()
        plotter = self._plotter
        pyplot = plotter.pyplot()
        plotter.newFig()
        plotter.setSubPlots(2,1)
        rawAddress = r'C:\Users\shouk\Github\EChem_Plotter\test_data\Cycle\ACC_S_253_3_94mg_TFEE-DOL_3-1_1MLiTFSI_50cy_DME-DOL_0_35MLiTFSI_1wtLiNO3_0_5C_SHong_09242020.xls'
        name = 'ACC_S_pretreat-50'

        dataManager = Plotter_Core.DataManager(rawAddress, 1)
        plotter.addDataManager(dataManager)
        dataManager.formatRawData()
        dataManager.createPlotData('Step_Index', label = 'Step_Index')
        dataManager.createPlotData('Voltage', label = 'Voltage')
        dataManager.createPlotData('Test_Time', label = 'Test_Time')
        plotter.activeDataManager().setPlotRangeByValue('Step_Index', 2)
        xData = dataManager.getPlotDataValues('Test_Time')
        yData = dataManager.getPlotDataValues('Voltage')
        dataManager.createVariable('startTime', xData[0])
        handler = '(val - Test_Time(startIndex))/3600'
        xData = dataManager.modifyValues(xData, handler)
        plotter.plot(xData, yData, legend = name)
        plotter.setAxScale(xStart = 0, xEnd = 100)
        plotter.setXAxLabel('Time/h')
        plotter.setYAxLabel('Voltage/V')
        plotter.activeAx().set_title('Long term cycle')
        plotter.showLegend()
        
        dataManager = Plotter_Core.DataManager(rawAddress, 'Statistics_1-017')
        plotter.addDataManager(dataManager)
        dataManager.formatRawData()
        handlerCharge = '1000 * (val - Charge_Capacity(i - 1, 0))'
        handlerDischarge = '1000 * (val - Discharge_Capacity(i - 1, 0))'
        handlerEfficiency = '100 * Discharge_Capacity(i)/Charge_Capacity(i - 1, val)'
        dataManager.createPlotData('Cycle_Index', label = 'Cycle_Index')
        dataManager.createPlotData('Charge_Capacity', handlerCharge, label = 'Charge_Capacity')
        dataManager.createPlotData('Discharge_Capacity', handlerDischarge, label = 'Discharge_Capacity')
        dataManager.createPlotData('Discharge_Capacity', handlerEfficiency, label = 'Efficiency')
        dataManager.setPlotRangeByValue('Cycle_Index' , 2)
        xData = dataManager.getPlotDataValues('Cycle_Index')
        yData = dataManager.getPlotDataValues('Discharge_Capacity')
        y2Data = dataManager.getPlotDataValues('Efficiency')
        plotter.setActiveAx(1)
        plotter.plot(xData, yData, legend = name)
        plotter.setAxScale(xStart = 0, yStart = 0, yEnd = 5)
        plotter.setXAxLabel('Cycle')
        plotter.setYAxLabel('Capacity/mAh')
        plotter.addTwinX(1)
        plotter.setYAxLabel(r'Efficiency/%')
        plotter.plot(xData, y2Data, legend = 'Efficiency', style = 'ro')
        plotter.setAxScale(yStart = 50, yEnd = 110)
        plotter.activeAx().set_title('Capacity degradation')
        plotter.showLegend()
        
        address = dataManager.formatAddress(self._saveAddress + r'\cycle.png')
        pyplot.savefig(address, dpi=300, bbox_inches="tight")
        print("testCycletakes %s seconds" % (time.time() - start_time))
        
# =============================================================================
# rawAddresses = [r'C:\Users\shouk\Github\EChem_Plotter\test_data\CA\AAO-TiN-V2O5_Lithiate_02_CA_C08.txt',
#                         r'C:\Users\shouk\Github\EChem_Plotter\test_data\CP\AAO-TiN-V2O5_Lithiate_01_CP_C08.txt',
#                         r'C:\Users\shouk\Github\EChem_Plotter\test_data\CV\11142021-Li-PC-LiClO4-V2O5_CV-0_1mV_C04.mpt',
#                         r'C:\Users\shouk\Github\EChem_Plotter\test_data\Cycle\ACC_S_259_3_94mg_TFEE-DOL_1-1_1MLiTFSI_0cy_0_5C_SHong_09242020.xls']
# =============================================================================
if (__name__ == '__main__'):

    # tester = DataManagerTester()
    # tester.testCycle()

    #DataManagerTester().testLoadDocInfo()
    
    tester = DataManagerTester()
    tester.testDataProcess()
    tester.testPlotter()
    tester.testRealData()

