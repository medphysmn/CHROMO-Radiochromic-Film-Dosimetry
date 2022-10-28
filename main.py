#!/usr/bin/env python
# coding: utf-8

#TODO PROIEZIONI - NET IMAGE - BKG - CORREZIONE LATERALE - FILE CONFIGURAZIONE TXT
import warnings
import sys
import tkinter
import tkinter.ttk as ttk
from tkinter import filedialog
from sys import exit

sys.path.append(".")
from constants import *
from functions import *
from doseClass import *
from rootFolderClass import *
from calibrationClass import *
from fitResultsSingleChannel import *

warnings.filterwarnings("ignore")

global path
path = selectDirectory() 
rootFolder = rootFolderClass(path)

###
chromoTk = tk.Toplevel()
chromoTk.title('CHROMO: Radiochromic Film Dosimetry')
chromoTk.geometry(str(widthTk)+"x"+str(heightTk))
chromoTk.config(background = "white")
chromoTk.resizable(False, False)

tabsystem = ttk.Notebook(chromoTk)
denoiser = tk.Frame(tabsystem, width= widthTk, height= heightTk)
singleChannelTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
multiChannelTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
propertiesTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
generalPropertiesTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
tabsystem.add(denoiser, text='Denoiser')
tabsystem.add(singleChannelTk, text='Single Channel Dosimetry')
tabsystem.add(multiChannelTk, text='Multi Channel Dosimetry')
tabsystem.add(propertiesTk, text='Calibration Properties')
tabsystem.add(generalPropertiesTk, text='Properties')
tabsystem.grid(column = 1, row = 0)

# =============================================================================
imageframe = tk.Frame(denoiser, width=imagedim, height=imagedim)
imageResized = pilimage.open("blank.jpg").resize((imagedim,imagedim))
img = itk.PhotoImage(imageResized)
labelImage = tk.Label(imageframe, image = img)

label_denoising = tk.Label(denoiser, text="CHOOSE ONE OPTION TO LOAD \n AND DENOISE CALIBRATION AND \n TREATMENT IMAGES:", fg="blue", font=("Arial", 15), width=35)
label_treatmentImage = tk.Label(denoiser, text="TREATMENT IMAGE", font=("Arial", 10))

tk.Label(denoiser, text="Enter Median Kernel:", font=("Arial")).grid(column = 1, row = 8)
medinalval = tk.IntVar(denoiser, value=3)
medianKernelTk=tk.Entry(denoiser, width=80, textvariable=medinalval)

tk.Label(denoiser, text="Enter Wiener Kernel:", font=("Arial")).grid(column = 1, row = 10)
wienerval = tk.IntVar(denoiser, value=3)
wienerKernelTk=tk.Entry(denoiser, width=80, textvariable=wienerval)

imageframe.grid(column = 2, row = 3, padx=10, pady=10,rowspan=5)
labelImage.grid(column = 2, row = 3)
medianKernelTk.grid(column = 2, row = 8)
wienerKernelTk.grid(column = 2, row = 10)
label_denoising.grid(column = 1, row = 3, padx=10, pady=10)
label_treatmentImage.grid(column = 2, row = 3, padx=10, pady=10)


button_median = tk.Button(denoiser, text = "DENOISE IMAGES WITH MEDIAN FILTER", #background="yellow",
                       command = lambda: median(rootFolder, label_denoising,denoiser, labelImage, medianKernelTk)).grid(column = 1, row = 4, padx=10, pady=10)
button_wiener = tk.Button(denoiser, text = "DENOISE IMAGES WITH WIENER FILTER",  #background="yellow",
                       command = lambda: wiener(rootFolder, rootFolder.nonFilteredCalibrationPath, rootFolder.nonFilteredTreatmentPath, label_denoising,denoiser, labelImage, True, wienerKernelTk)).grid(column = 1, row = 5, padx=10, pady=10)
button_medianandwiener = tk.Button(denoiser, text = "DENOISE IMAGES WITH WIENER AND MEDIAN FILTER", #background="yellow",
                                command = lambda: medianAndWiener(rootFolder, label_denoising, denoiser, labelImage,medianKernelTk ,wienerKernelTk)).grid(column = 1, row = 6, padx=10, pady=10)
button_no_denoising = tk.Button(denoiser, text = "DON'T USE ANY FILTER ", #background="yellow", 
                             command = lambda: noDenoising(rootFolder, label_denoising, denoiser, labelImage)).grid(column = 1, row = 7, padx=10, pady=10)

# =============================================================================
tk.Label(singleChannelTk, text="choose fitting function (rational or exponential):", font=("Arial")).grid(column = 1, row = 1)
fittingval = tk.StringVar(singleChannelTk, value='rational')
fittingFunctionTk=tk.Entry(singleChannelTk, width=10, textvariable=fittingval)
fittingFunctionTk.grid(column = 2, row = 1)

label_rational = tk.Label(propertiesTk, text="RATIONAL FUNCTION: f(x)= a + b/(x+c)", fg="blue", font=("Arial", 15), width=35).grid(column = 1, row = 1)

tk.Label(propertiesTk, text="rational calibration fit, a_RED:", font=("Arial")).grid(column = 1, row = 2)
p0redval = tk.DoubleVar(propertiesTk, value=-10.)
p0redTk=tk.Entry(propertiesTk, width=10, textvariable=p0redval)
p0redTk.grid(column = 2, row = 2)

tk.Label(propertiesTk, text="rational calibration fit, b_RED:", font=("Arial")).grid(column = 1, row = 3)
p1redval = tk.DoubleVar(propertiesTk, value=200.)
p1redTk=tk.Entry(propertiesTk, width=10, textvariable=p1redval)
p1redTk.grid(column = 2, row = 3)

tk.Label(propertiesTk, text="rational calibration fit, c_RED:", font=("Arial")).grid(column = 1, row = 4)
p2redval = tk.DoubleVar(propertiesTk, value=3.)
p2redTk=tk.Entry(propertiesTk, width=10, textvariable=p2redval)
p2redTk.grid(column = 2, row = 4)

tk.Label(propertiesTk, text="inverse rational calibration fit, a_RED_inverse:", font=("Arial")).grid(column = 4, row = 2)
pinv0redval = tk.DoubleVar(propertiesTk, value=-10.)
pinv0redTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0redval)
pinv0redTk.grid(column = 5, row = 2)

tk.Label(propertiesTk, text="inverse rational calibration fit, b_RED_inverse:", font=("Arial")).grid(column = 4, row = 3)
pinv1redval = tk.DoubleVar(propertiesTk, value=300.)
pinv1redTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1redval)
pinv1redTk.grid(column = 5, row = 3)

tk.Label(propertiesTk, text="inverse rational calibration fit, c_RED_inverse:", font=("Arial")).grid(column = 4, row = 4)
pinv2redval = tk.DoubleVar(propertiesTk, value=3.)
pinv2redTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2redval)
pinv2redTk.grid(column = 5, row = 4)

tk.Label(propertiesTk, text="rational calibration fit, a_GREEN:", font=("Arial")).grid(column = 1, row = 5)
p0greenval = tk.DoubleVar(propertiesTk, value=-10.)
p0greenTk=tk.Entry(propertiesTk, width=10, textvariable=p0greenval)
p0greenTk.grid(column = 2, row = 5)

tk.Label(propertiesTk, text="rational calibration fit, b_GREEN:", font=("Arial")).grid(column = 1, row = 6)
p1greenval = tk.DoubleVar(propertiesTk, value=300.)
p1greenTk=tk.Entry(propertiesTk, width=10, textvariable=p1greenval)
p1greenTk.grid(column = 2, row = 6)

tk.Label(propertiesTk, text="rational calibration fit, c_GREEN:", font=("Arial")).grid(column = 1, row = 7)
p2greenval = tk.DoubleVar(propertiesTk, value=3.)
p2greenTk=tk.Entry(propertiesTk, width=10, textvariable=p2greenval)
p2greenTk.grid(column = 2, row = 7)

tk.Label(propertiesTk, text="inverse rational calibration fit, a_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 5)
pinv0greenval = tk.DoubleVar(propertiesTk, value=-10.)
pinv0greenTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0greenval)
pinv0greenTk.grid(column = 5, row = 5)

tk.Label(propertiesTk, text="inverse rational calibration fit, b_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 6)
pinv1greenval = tk.DoubleVar(propertiesTk, value=300.)
pinv1greenTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1greenval)
pinv1greenTk.grid(column = 5, row = 6)

tk.Label(propertiesTk, text="inverse rational calibration fit, c_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 7)
pinv2greenval = tk.DoubleVar(propertiesTk, value=3.)
pinv2greenTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2greenval)
pinv2greenTk.grid(column = 5, row = 7)

tk.Label(propertiesTk, text="rational calibration fit, a_BLUE:", font=("Arial")).grid(column = 1, row = 8)
p0blueval = tk.DoubleVar(propertiesTk, value=-10.)
p0blueTk=tk.Entry(propertiesTk, width=10, textvariable=p0blueval)
p0blueTk.grid(column = 2, row = 8)

tk.Label(propertiesTk, text="rational calibration fit, b_BLUE:", font=("Arial")).grid(column = 1, row = 9)
p1blueval = tk.DoubleVar(propertiesTk, value=300.)
p1blueTk=tk.Entry(propertiesTk, width=10, textvariable=p1blueval)
p1blueTk.grid(column = 2, row = 9)

tk.Label(propertiesTk, text="rational calibration fit, c_BLUE:", font=("Arial")).grid(column = 1, row = 10)
p2blueval = tk.DoubleVar(propertiesTk, value=3.)
p2blueTk=tk.Entry(propertiesTk, width=10, textvariable=p2blueval)
p2blueTk.grid(column = 2, row = 10)

tk.Label(propertiesTk, text="inverse rational calibration fit, a_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 8)
pinv0blueval = tk.DoubleVar(propertiesTk, value=-10.)
pinv0blueTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0blueval)
pinv0blueTk.grid(column = 5, row = 8)

tk.Label(propertiesTk, text="inverse rational calibration fit, b_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 9)
pinv1blueval = tk.DoubleVar(propertiesTk, value=300.)
pinv1blueTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1blueval)
pinv1blueTk.grid(column = 5, row = 9)

tk.Label(propertiesTk, text="inverse rational calibration fit, c_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 10)
pinv2blueval = tk.DoubleVar(propertiesTk, value=3.)
pinv2blueTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2blueval)
pinv2blueTk.grid(column = 5, row = 10)

label_exponential = tk.Label(propertiesTk, text="EXPONENTIAL FUNCTION: f(x)= a*exp(-x/b) + c", fg="blue", font=("Arial", 15), width=45).grid(column = 1, row = 11)

tk.Label(propertiesTk, text="exponential calibration fit, a_RED:", font=("Arial")).grid(column = 1, row = 12)
p0redexpval = tk.DoubleVar(propertiesTk, value=-10.)
p0redexpTk=tk.Entry(propertiesTk, width=10, textvariable=p0redexpval)
p0redexpTk.grid(column = 2, row = 12)

tk.Label(propertiesTk, text="exponential calibration fit, b_RED:", font=("Arial")).grid(column = 1, row = 13)
p1redexpval = tk.DoubleVar(propertiesTk, value=200.)
p1redexpTk=tk.Entry(propertiesTk, width=10, textvariable=p1redexpval)
p1redexpTk.grid(column = 2, row = 13)

tk.Label(propertiesTk, text="exponential calibration fit, c_RED:", font=("Arial")).grid(column = 1, row = 14)
p2redexpval = tk.DoubleVar(propertiesTk, value=3.)
p2redexpTk=tk.Entry(propertiesTk, width=10, textvariable=p2redexpval)
p2redexpTk.grid(column = 2, row = 14)

tk.Label(propertiesTk, text="inverse exponential calibration fit, a_RED_inverse:", font=("Arial")).grid(column = 4, row = 12)
pinv0redexpval = tk.DoubleVar(propertiesTk, value=100.)
pinv0redexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0redexpval)
pinv0redexpTk.grid(column = 5, row = 12)

tk.Label(propertiesTk, text="inverse exponential calibration fit, b_RED_inverse:", font=("Arial")).grid(column = 4, row = 13)
pinv1redexpval = tk.DoubleVar(propertiesTk, value=5.)
pinv1redexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1redexpval)
pinv1redexpTk.grid(column = 5, row = 13)

tk.Label(propertiesTk, text="inverse exponential calibration fit, c_RED_inverse:", font=("Arial")).grid(column = 4, row = 14)
pinv2redexpval = tk.DoubleVar(propertiesTk, value=0.)
pinv2redexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2redexpval)
pinv2redexpTk.grid(column = 5, row = 14)

tk.Label(propertiesTk, text="exponential calibration fit, a_GREEN:", font=("Arial")).grid(column = 1, row = 15)
p0greenexpval = tk.DoubleVar(propertiesTk, value=500.)
p0greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=p0greenexpval)
p0greenexpTk.grid(column = 2, row = 15)

tk.Label(propertiesTk, text="exponential calibration fit, b_GREEN:", font=("Arial")).grid(column = 1, row = 16)
p1greenexpval = tk.DoubleVar(propertiesTk, value=-500.)
p1greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=p1greenexpval)
p1greenexpTk.grid(column = 2, row = 16)

tk.Label(propertiesTk, text="exponential calibration fit, c_GREEN:", font=("Arial")).grid(column = 1, row = 17)
p2greenexpval = tk.DoubleVar(propertiesTk, value=300.)
p2greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=p2greenexpval)
p2greenexpTk.grid(column = 2, row = 17)

tk.Label(propertiesTk, text="inverse exponential calibration fit, a_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 15)
pinv0greenexpval = tk.DoubleVar(propertiesTk, value=100.)
pinv0greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0greenexpval)
pinv0greenexpTk.grid(column = 5, row = 15)

tk.Label(propertiesTk, text="inverse exponential calibration fit, b_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 16)
pinv1greenexpval = tk.DoubleVar(propertiesTk, value=10.)
pinv1greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1greenexpval)
pinv1greenexpTk.grid(column = 5, row = 16)

tk.Label(propertiesTk, text="inverse exponential calibration fit, c_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 17)
pinv2greenexpval = tk.DoubleVar(propertiesTk, value=30.)
pinv2greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2greenexpval)
pinv2greenexpTk.grid(column = 5, row = 17)

tk.Label(propertiesTk, text="exponential calibration fit, a_BLUE:", font=("Arial")).grid(column = 1, row = 18)
p0blueexpval = tk.DoubleVar(propertiesTk, value=500.)
p0blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=p0blueexpval)
p0blueexpTk.grid(column = 2, row = 18)

tk.Label(propertiesTk, text="exponential calibration fit, b_BLUE:", font=("Arial")).grid(column = 1, row = 19)
p1blueexpval = tk.DoubleVar(propertiesTk, value=-150.)
p1blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=p1blueexpval)
p1blueexpTk.grid(column = 2, row = 19)

tk.Label(propertiesTk, text="exponential calibration fit, c_BLUE:", font=("Arial")).grid(column = 1, row = 20)
p2blueexpval = tk.DoubleVar(propertiesTk, value=300.)
p2blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=p2blueexpval)
p2blueexpTk.grid(column = 2, row = 20)

tk.Label(propertiesTk, text="inverse exponential calibration fit, a_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 18)
pinv0blueexpval = tk.DoubleVar(propertiesTk, value=100.)
pinv0blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0blueexpval)
pinv0blueexpTk.grid(column = 5, row = 18)

tk.Label(propertiesTk, text="inverse exponential calibration fit, b_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 19)
pinv1blueexpval = tk.DoubleVar(propertiesTk, value=5.)
pinv1blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1blueexpval)
pinv1blueexpTk.grid(column = 5, row = 19)

tk.Label(propertiesTk, text="inverse exponential calibration fit, c_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 20)
pinv2blueexpval = tk.DoubleVar(propertiesTk, value=0.)
pinv2blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2blueexpval)
pinv2blueexpTk.grid(column = 5, row = 20)

label_exponential = tk.Label(propertiesTk, text="MULTICHANNEL CALIBRATION", fg="blue", font=("Arial", 15), width=45).grid(column = 1, row = 21)

tk.Label(propertiesTk, text="multichannel calibration fit, a_MC:", font=("Arial")).grid(column = 1, row = 22)
a0mcvalval = tk.DoubleVar(propertiesTk, value=0.)
a0mcTk=tk.Entry(propertiesTk, width=10, textvariable=a0mcvalval)
a0mcTk.grid(column = 2, row = 22)

tk.Label(propertiesTk, text="multichannel calibration fit, b_MC:", font=("Arial")).grid(column = 1, row = 23)
a1mcvalval = tk.DoubleVar(propertiesTk, value=1000.)
a1mcTk=tk.Entry(propertiesTk, width=10, textvariable=a1mcvalval)
a1mcTk.grid(column = 2, row = 23)

tk.Label(propertiesTk, text="multichannel calibration fit, c_MC:", font=("Arial")).grid(column = 1, row = 24)
a2mcvalval = tk.DoubleVar(propertiesTk, value=5.)
a2mcTk=tk.Entry(propertiesTk, width=10, textvariable=a2mcvalval)
a2mcTk.grid(column = 2, row = 24)

tk.Label(propertiesTk, text="inverse multichannel calibration fit, a_MC_inverse:", font=("Arial")).grid(column = 4, row = 22)
a0invmcvalval = tk.DoubleVar(propertiesTk, value=0.)
a0invmcTk=tk.Entry(propertiesTk, width=10, textvariable=a0invmcvalval)
a0invmcTk.grid(column = 5, row = 22)

tk.Label(propertiesTk, text="inverse multichannel calibration fit, b_MC_inverse:", font=("Arial")).grid(column = 4, row = 23)
a1invmcvalval = tk.DoubleVar(propertiesTk, value=1000.)
a1invmcTk=tk.Entry(propertiesTk, width=10, textvariable=a1mcvalval)
a1invmcTk.grid(column = 5, row = 23)

tk.Label(propertiesTk, text="inverse multichannel calibration fit, c_MC_inverse:", font=("Arial")).grid(column = 4, row = 24)
a2invmcvalval = tk.DoubleVar(propertiesTk, value=5.)
a2invmcTk=tk.Entry(propertiesTk, width=10, textvariable=a2invmcvalval)
a2invmcTk.grid(column = 5, row = 24)

tk.Label(propertiesTk, text="maximum number of fit iterations:", font=("Arial")).grid(column = 1, row = 0)
maxitval = tk.IntVar(propertiesTk, value=100000)
maxitvalTk=tk.Entry(propertiesTk, width=10, textvariable=maxitval)
maxitvalTk.grid(column = 2, row = 0)

tk.Label(propertiesTk, text="maximum recalibration dose:", font=("Arial")).grid(column = 4, row = 0)
recval = tk.IntVar(propertiesTk, value=6)
recvalTk=tk.Entry(propertiesTk, width=10, textvariable=recval)
recvalTk.grid(column = 5, row = 0)

tk.Label(propertiesTk, text="maximum recalibration dose:", font=("Arial")).grid(column = 4, row = 0)
recval = tk.IntVar(propertiesTk, value=6)
recvalTk=tk.Entry(propertiesTk, width=10, textvariable=recval)
recvalTk.grid(column = 5, row = 0)

tk.Label(generalPropertiesTk, text="resolution:", font=("Arial")).grid(column = 1, row = 0)
resval = tk.DoubleVar(generalPropertiesTk, value=25.4)
resvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=resval)
resvalTk.grid(column = 2, row = 0)

tk.Label(generalPropertiesTk, text="dpi:", font=("Arial")).grid(column = 3, row = 0)
dpival = tk.IntVar(generalPropertiesTk, value=150)
dpivalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=dpival)
dpivalTk.grid(column = 4, row = 0)

tk.Label(generalPropertiesTk, text="red channel:", font=("Arial")).grid(column = 1, row = 1)
redchval = tk.IntVar(generalPropertiesTk, value=2)
redchvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=redchval)
redchvalTk.grid(column = 2, row = 1)

tk.Label(generalPropertiesTk, text="green channel:", font=("Arial")).grid(column = 1, row = 2)
greenchval = tk.IntVar(generalPropertiesTk, value=1)
greenchvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=greenchval)
greenchvalTk.grid(column = 2, row = 2)

tk.Label(generalPropertiesTk, text="blue channel:", font=("Arial")).grid(column = 1, row = 3)
bluechval = tk.IntVar(generalPropertiesTk, value=0)
bluechvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=bluechval)
bluechvalTk.grid(column = 2, row = 3)

tk.Label(generalPropertiesTk, text="calibration Roi dimension:", font=("Arial")).grid(column = 3, row = 1)
calroidimval = tk.IntVar(generalPropertiesTk, value=5)
calroidimvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=calroidimval)
calroidimvalTk.grid(column = 4, row = 1)

tk.Label(generalPropertiesTk, text="Roi dimension in pixel:", font=("Arial")).grid(column = 3, row = 2)
dimRoiCalibrationval = tk.IntVar(generalPropertiesTk, value=10)
dimRoiCalibrationvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=dimRoiCalibrationval)
dimRoiCalibrationvalTk.grid(column = 4, row = 2)

tk.Label(generalPropertiesTk, text="isodose difference in Gy:", font=("Arial")).grid(column = 3, row = 3)
isodoseDifferenceGyval = tk.DoubleVar(generalPropertiesTk, value=0.1)
isodoseDifferenceGyvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=isodoseDifferenceGyval)
isodoseDifferenceGyvalTk.grid(column = 4, row = 3)

tk.Label(generalPropertiesTk, text="raw dose image output format:", font=("Arial")).grid(column = 3, row = 4)
doseRawImageOutputFormatval = tk.StringVar(generalPropertiesTk, value='tiff')
doseRawImageOutputFormatvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=doseRawImageOutputFormatval)
doseRawImageOutputFormatvalTk.grid(column = 4, row = 4)

tk.Label(generalPropertiesTk, text="figures color map:", font=("Arial")).grid(column = 3, row = 5)
cmapval = tk.StringVar(generalPropertiesTk, value='rainbow')
cmapvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=cmapval)
cmapvalTk.grid(column = 4, row = 5)

tk.Label(generalPropertiesTk, text="plot profiles of dose maps results:", font=("Arial")).grid(column = 3, row = 6)
plotprofilesval = tk.BooleanVar(generalPropertiesTk, value=False)
plotprofilesvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=plotprofilesval)
plotprofilesvalTk.grid(column = 4, row = 6)


button_singleCalibrtion = tk.Button(singleChannelTk, text = "START CALIBRATION", #background="yellow", 
                                    command = lambda: singleChannelDosimetryGUI(rootFolder, 
                                                                                fittingFunctionTk.get(), 
                                                                                (float(p0redTk.get()), float(p1redTk.get()), float(p2redTk.get())), 
                                                                                (float(pinv0redTk.get()), float(pinv1redTk.get()), float(pinv2redTk.get() )), 
                                                                                (float(p0greenTk.get()), float(p1greenTk.get()), float(p2greenTk.get())), 
                                                                                (float(pinv0greenTk.get()), float(pinv1greenTk.get()), float(pinv2greenTk.get() )), 
                                                                                (float(p0blueTk.get()), float(p1blueTk.get()), float(p2blueTk.get())), 
                                                                                (float(pinv0blueTk.get()), float(pinv1blueTk.get()), float(pinv2blueTk.get()) ), 
                                                                                (float(p0redexpTk.get()), float(p1redexpTk.get()), float(p2redexpTk.get())) , 
                                                                                (float(pinv0redexpTk.get()), float(pinv1redexpTk.get()), float(pinv2redexpTk.get() )), 
                                                                                (float(p0greenexpTk.get()), float(p1greenexpTk.get()), float(p2greenexpTk.get())), 
                                                                                (float(pinv0greenexpTk.get()), float(pinv1greenexpTk.get()), float(pinv2greenexpTk.get() )), 
                                                                                (float(p0blueexpTk.get()), float(p1blueexpTk.get()), float(p2blueexpTk.get())) , 
                                                                                (float(pinv0blueexpTk.get()), float(pinv1blueexpTk.get()), float(pinv2blueexpTk.get() )), 
                                                                                np.array([float(a0mcTk.get()), float(a1mcTk.get()), float(a2mcTk.get())]), #da cambiare eventualmente il punto iniziale
                                                                                np.array([float(a0invmcTk.get()), float(a1invmcTk.get()), float(a2invmcTk.get())]), #da cambiare eventualmente il punto iniziale
                                                                                int(maxitvalTk.get()), 
                                                                                int(recvalTk.get()), 
                                                                                cmapvalTk.get(), 
                                                                                doseRawImageOutputFormatvalTk.get() , 
                                                                                float(isodoseDifferenceGyvalTk.get()) , 
                                                                                int(dimRoiCalibrationvalTk.get()), 
                                                                                int(calroidimvalTk.get()), 
                                                                                int(redchvalTk.get()), 
                                                                                int(greenchvalTk.get()), 
                                                                                int(bluechvalTk.get()), 
                                                                                float(resvalTk.get()), 
                                                                                float(dpivalTk.get()), 
                                                                                (float(resvalTk.get())/float(dpivalTk.get())),
                                                                                plotprofilesvalTk.get())).grid(column = 1, row = 15 , padx=10, pady=10)


# =============================================================================
button_multichannelCalibration = tk.Button(multiChannelTk, text = "START CALIBRATION", #background="yellow", 
                                    command = lambda: multiChannelDosimetryGUI(rootFolder, 
                                                                               (float(p0redTk.get()), float(p1redTk.get()), float(p2redTk.get())), 
                                                                               (float(pinv0redTk.get()), float(pinv1redTk.get()), float(pinv2redTk.get() )), 
                                                                               (float(p0greenTk.get()), float(p1greenTk.get()), float(p2greenTk.get())), 
                                                                               (float(pinv0greenTk.get()), float(pinv1greenTk.get()), float(pinv2greenTk.get() )), 
                                                                               (float(p0blueTk.get()), float(p1blueTk.get()), float(p2blueTk.get())), 
                                                                               (float(pinv0blueTk.get()), float(pinv1blueTk.get()), float(pinv2blueTk.get() )), 
                                                                               (float(p0redexpTk.get()), float(p1redexpTk.get()), float(p2redexpTk.get())) , 
                                                                               (float(pinv0redexpTk.get()), float(pinv1redexpTk.get()), float(pinv2redexpTk.get()) ), 
                                                                               (float(p0greenexpTk.get()), float(p1greenexpTk.get()), float(p2greenexpTk.get())), 
                                                                               (float(pinv0greenexpTk.get()), float(pinv1greenexpTk.get()), float(pinv2greenexpTk.get()) ), 
                                                                               (float(p0blueexpTk.get()), float(p1blueexpTk.get()), float(p2blueexpTk.get())) , 
                                                                               (float(pinv0blueexpTk.get()), float(pinv1blueexpTk.get()), float(pinv2blueexpTk.get()) ), 
                                                                               np.array([float(a0mcTk.get()), float(a1mcTk.get()), float(a2mcTk.get())]), #da cambiare eventualmente il punto iniziale
                                                                               np.array([float(a0invmcTk.get()), float(a1invmcTk.get()), float(a2invmcTk.get())]), #da cambiare eventualmente il punto iniziale                                                                            
                                                                               int(maxitvalTk.get()), 
                                                                               int(recvalTk.get()), 
                                                                               cmapvalTk.get(), 
                                                                               doseRawImageOutputFormatvalTk.get() , 
                                                                               float(isodoseDifferenceGyvalTk.get()) ,
                                                                               int(dimRoiCalibrationvalTk.get()), 
                                                                               int(calroidimvalTk.get()), 
                                                                               int(redchvalTk.get()), 
                                                                               int(greenchvalTk.get()), 
                                                                               int(bluechvalTk.get()), 
                                                                               float(resvalTk.get()), 
                                                                               float(dpivalTk.get()), 
                                                                               (float(resvalTk.get())/float(dpivalTk.get())),
                                                                               plotprofilesvalTk.get())).grid(column = 1, row = 10 , padx=10, pady=10)



chromoTk.mainloop()