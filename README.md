# EChem_Plotter

## Introduction
For scientific research, some experiments can be highly repetitive and so does their data. 
EChem Plotter is a software designed to ease the plotting of experimental data that has identical format and process procedure.
With this software, you can program without coding knowledge and use your template to process all the similar data.

The open-sourced software is based on python and modules including pyQt5, matplotlib, numpy and pandas.

The software includes some templates designed for data generated by EC-Lab battery station. These templates can easily plot CV, CA, CP, Cycle and EIS,
which are very common electro chemistry experiments. The templates are a good start point and can be easily extended to fit other needs. You can also start from scratch and make your own template.

#### Images plotted by these templates:
<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/CV_Cycle_EIS.png">

## Install
Download the zip folder and unzip. 

## How to Use

Excecute the EChem_Plotter.exe and you are ready to go!
You will first see a black window, which is the console, be patient and wait for the main window to pop up:

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/mainWindow.png" width="700" height="600">

The UI is composed of 4 parts:
The left top part is data Manager Tab, where you control how to process your data.
The right top part is data Info Window, where you can view your data.
The left bottom part is plotter, where you control what to plot.
The right bottom part is image preview, where you can preview and make adjustment to the image.

### Quick Start
There are some provided templates for you to start with. First, go to menu and select 'Load Template':

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/loadTemplate.png" width="300" height="200">

A select file dialog will pop up and you will see a 'DemoDataAndTemplate' folder, go to DemoDataAndTemplate\Basic\ and select Base_Template.tmp.

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/selectBaseTemplate.png" width="350" height="80">

A template contains code for all the data managers and plotter. This template is designed for the linear.txt, so lets' click on the 'Data File' button in the Data Managers part.

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/selectDataFile.png" width="350" height="300">

Then, select linear.txt, the linear txt data will show up on the info window, please ignore the '...' which is a small display bug:

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/rawDataLinear.png" width="350" height="300">

Now, let's take a look at what the program does, if you double click on the list items, a dialog will show up, let's click on the 'Format Raw Data' row:

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/formatRawData.png" width="500" height="400">

You can see that we are spliting the raw data with tab. Hover on the parameter text will show you description of the parameter.
You can edit the action and parameters to do different things, but for now let's just close the dialog and click 'run and plot' in the plotter part.

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/runAndPlot.png" width="350" height="300">

And that's it, the plot is there and you can click 'save image' to save it!
You can use the tool bar above image preview to adjust the image, you can also go to menu->setting->image format to change the size and dpi of the image.
To verify that the data are correctly processed, you can click on the Data/Variable/Plot Data tabs in the info part. Note that only plot data is used for plotting.

<img src="https://github.com/ShoukangHong/EChem_Plotter/blob/main/images/basicDone.png" width="700" height="600">

Now you can play around with the program, you can try other templates and data file, edit parameters, and plot! If you don't understand what a button/parameter does,
hover on it and a help text may show up!

## TODO:

#### DataManager Action Dialog

#### Plotter Action Dialog

#### Documentation
