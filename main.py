#!/usr/bin/env python
# coding: utf-8

#TODO PROIEZIONI - NET IMAGE - BKG - CORREZIONE LATERALE - FILE CONFIGURAZIONE TXT
import scipy
import numpy as np
import re
import matplotlib.pyplot as plt
import cv2
import warnings
import sys
from scipy.optimize import *
from scipy.interpolate import *
from shutil import move, copyfile
import os
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
tabsystem.add(denoiser, text='Denoiser')
tabsystem.add(singleChannelTk, text='Single Channel Dosimetry')
tabsystem.add(multiChannelTk, text='Multi Channel Dosimetry')
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
fittingFunctionTk=tk.Entry(singleChannelTk, width=80, textvariable=fittingval)
fittingFunctionTk.grid(column = 2, row = 1)

button_singleCalibrtion = tk.Button(singleChannelTk, text = "START CALIBRATION", #background="yellow", 
                                    command = lambda: singleChannelDosimetryGUI(rootFolder, fittingFunctionTk)).grid(column = 1, row = 10 , padx=10, pady=10)


# =============================================================================
button_multichannelCalibration = tk.Button(multiChannelTk, text = "START CALIBRATION", #background="yellow", 
                                    command = lambda: multiChannelDosimetryGUI(rootFolder)).grid(column = 1, row = 10 , padx=10, pady=10)


chromoTk.mainloop()


# imageframeRed = tk.Frame(singleChannelTk, width=200, height=200)
# imageResizedRed = pilimage.open("blank.jpg").resize((200,200))
# imgRed = itk.PhotoImage(imageResizedRed)
# labelImageRed = tk.Label(imageframeRed, image = img)

# =============================================================================
# for unexposed_filepath in rootFolder.unexposed_calibration_list:    
#     try:
#         calibrationObjects.append(calibrationClass(cv2.imread(unexposed_filepath), redChannel, greenChannel, blueChannel, 0, 999))
#     except:
#         print('WARNING: No unexposed calibration film found')
#             
# for calibration_filepath in rootFolder.calibration_list:
#     reg_search = re.search('.*calibration_(.*)Gy_.*', calibration_filepath)
#     calibrationObjects.append(calibrationClass(cv2.imread(calibration_filepath), redChannel, greenChannel, blueChannel, reg_search.group(1), 999))
# 
# calibrationObjects.sort(key=lambda x: x.calibration_dose)
# calibration_dose = [x.calibration_dose for x in calibrationObjects]
# calibration_red = [x.calibrationRed for x in calibrationObjects]
# calibration_green = [x.calibrationGreen for x in calibrationObjects]
# calibration_blue = [x.calibrationBlue for x in calibrationObjects]
# =============================================================================


     
# =============================================================================
# if singleChannelDosimetry:
#     
#     fitResults, x_max_lsmodel, y_calibration_fit = fitDataAndPlotCurves(calibration_dose, calibration_red, calibration_green , calibration_blue, rootFolder)
# 
#     for i, scan_filepath in enumerate(rootFolder.treatment_list):  
#            
#         print("TREATMENT NUMBER " , i+1, '\n')
#         print(" Treatment file analyzed = %s" % (scan_filepath), '\n')
#         
#         image = cv2.imread(scan_filepath)
#         netImage = image
#         
#         dose_red =  calculateSingleChannelDose(netImage[:,:,redChannel], fitResults.redFit).clip(min=0)
#         min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred = dose_calculations(dose_red, 'r', 0, 0)
#         redDosObjArr.append(doseClass(dose_red, min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred))
#         
#         dose_green =  calculateSingleChannelDose(netImage[:,:,greenChannel], fitResults.greenFit).clip(min=0)
#         min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen = dose_calculations(dose_green, 'g', 0, 0)
#         greenDosObjArr.append(doseClass(dose_green, min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen))    
#         
#         dose_blue =  calculateSingleChannelDose(netImage[:,:,blueChannel], fitResults.blueFit).clip(min=0)
#         min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue = dose_calculations(dose_blue, 'b', 0, 0)
#         blueDosObjArr.append(doseClass(dose_blue, min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue))  
#         
#     for enum, (redDosObjTrm, greenDosObjTrm, blueDosObjTrm) in enumerate(zip(redDosObjArr, greenDosObjArr, blueDosObjArr)):
#         
#         print("TREATMENT NUMBER " , enum+1, '\n')
#         print(" filepath = %s" % (rootFolder.treatment_list[enum]), '\n')
#         print('DOSES AND PROFILES: \n')
#     
#         plot_dose(redDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Red', '/RED/dose_red', enum, rootFolder)
#         plot_dose(greenDosObjTrm.dosefiltered,redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Green', '/GREEN/dose_green', enum, rootFolder)
#         plot_dose(blueDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Blue', '/BLUE/dose_blue', enum, rootFolder)
#         plt.show()
#         
#         if plotProfilesResults:
#             plot_projections(redDosObjTrm.dosefiltered, 'red', 'r-', redDosObjTrm.half_maximum_xdos, redDosObjTrm.half_maximum_ydos, 'ro:')
#             plot_projections(greenDosObjTrm.dosefiltered, 'green', 'g-', greenDosObjTrm.half_maximum_xdos, greenDosObjTrm.half_maximum_ydos, 'go:')
#             plot_projections(blueDosObjTrm.dosefiltered, 'blue', 'b-', blueDosObjTrm.half_maximum_xdos, blueDosObjTrm.half_maximum_ydos, 'bo:')
#         
#         rootFolder = rootFolderClass(path)
# =============================================================================


# =============================================================================
#     
# if multiChannelDosimetry:
#       
#     for i, (unexposed_treatment_filepath, maxdose_treatment_filepath) in enumerate(zip(rootFolder.unexposed_treatment_list, rootFolder.maxdose_treatment_list)):
#         unexposedTreatmentObjects.append(calibrationClass(cv2.imread(unexposed_treatment_filepath), redChannel, greenChannel, blueChannel, 999, i))
#         maxDoseTreatmentObjects.append(calibrationClass(cv2.imread(maxdose_treatment_filepath), redChannel, greenChannel, blueChannel, 999, i))  
#              
#     fitResults, x_max_lsmodel, y_calibration_fit = fitDataAndPlotCurves(calibration_dose, calibration_red, calibration_green , calibration_blue, rootFolder)
#     
#     for i, scan_filepath in enumerate(rootFolder.treatment_list):  
#         
#         a_red = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationRed, maxDoseTreatmentObjects[i].calibrationRed, fitResults)[0]  
#         b_red = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationRed, maxDoseTreatmentObjects[i].calibrationRed, fitResults)[1]  
#         a_green = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationGreen, maxDoseTreatmentObjects[i].calibrationGreen, fitResults)[0]  
#         b_green = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationGreen, maxDoseTreatmentObjects[i].calibrationGreen, fitResults)[1]  
#         a_blue = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationBlue, maxDoseTreatmentObjects[i].calibrationBlue, fitResults)[0]  
#         b_blue = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationBlue, maxDoseTreatmentObjects[i].calibrationBlue, fitResults)[1]  
#         
#         print("TREATMENT NUMBER " , i+1, '\n')
#         print(" Treatment file analyzed = %s" % (scan_filepath), '\n')
#         
#         image = cv2.imread(scan_filepath)
#         netImage = image
#         
#         plotRecalibratedImages(x_max_lsmodel, unexposedTreatmentObjects[i], maxDoseTreatmentObjects[i], recalibrated_multichannel_response_curve_red, 
#                                recalibrated_multichannel_response_curve_green, recalibrated_multichannel_response_curve_blue, y_calibration_fit, i, 
#                                a_red, b_red, a_green, b_green, a_blue, b_blue, fitResults, rootFolder)
#           
#         dose_red =  inverse_recalibrated_multichannel_response_curve_red(netImage[:,:,redChannel], a_red, b_red, fitResults).clip(min=0)
#         min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred = dose_calculations(dose_red, 'r', 0, 0)
#         redDosObjArr.append(doseClass(dose_red, min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred))
#         
#         dose_green =  inverse_recalibrated_multichannel_response_curve_green(netImage[:,:,greenChannel], a_green, b_green, fitResults).clip(min=0)
#         min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen = dose_calculations(dose_green, 'g', 0, 0)
#         greenDosObjArr.append(doseClass(dose_green, min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen))    
#         
#         dose_blue =  inverse_recalibrated_multichannel_response_curve_blue(netImage[:,:,blueChannel], a_blue, b_blue, fitResults).clip(min=0)
#         min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue = dose_calculations(dose_blue, 'b', 0, 0)
#         blueDosObjArr.append(doseClass(dose_blue, min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue))  
#         
#         dose_3ch = (dose_blue_center + dose_red_center + dose_green_center)/3
#         bkgx3ch, bkgy3ch  = (bkgxred + bkgxgreen + bkgxblue)/3 , (bkgyred + bkgygreen + bkgyblue)/3   
#         min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x,half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch = dose_calculations(dose_3ch, '3ch', bkgx3ch, bkgy3ch)
#         trheechDosObjArr.append(doseClass(dose_3ch, min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x, half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch))  
#     
#     for enum, (redDosObjTrm, greenDosObjTrm, blueDosObjTrm, threechDosObjTrm) in enumerate(zip(redDosObjArr, greenDosObjArr, blueDosObjArr, trheechDosObjArr )):
#         
#         print("TREATMENT NUMBER " , enum+1, '\n')
#         print(" filepath = %s" % (rootFolder.treatment_list[enum]), '\n')
#         print('DOSES AND PROFILES: \n')
#     
#         plot_dose(redDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Red', '/RED/dose_red', enum, rootFolder)
#         plot_dose(greenDosObjTrm.dosefiltered,redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Green', '/GREEN/dose_green', enum, rootFolder)
#         plot_dose(blueDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Blue', '/BLUE/dose_blue', enum, rootFolder)
#         plot_dose((redDosObjTrm.dosefiltered + greenDosObjTrm.dosefiltered + blueDosObjTrm.dosefiltered)/3, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, 
#                   blueDosObjTrm.maxdos, '3 channel', '/3CH/dose_3ch', enum, rootFolder)
#         plt.show()
#         
#         if plotProfilesResults:
#             plot_projections(redDosObjTrm.dosefiltered, 'red', 'r-', redDosObjTrm.half_maximum_xdos, redDosObjTrm.half_maximum_ydos, 'ro:')
#             plot_projections(greenDosObjTrm.dosefiltered, 'green', 'g-', greenDosObjTrm.half_maximum_xdos, greenDosObjTrm.half_maximum_ydos, 'go:')
#             plot_projections(blueDosObjTrm.dosefiltered, 'blue', 'b-', blueDosObjTrm.half_maximum_xdos, blueDosObjTrm.half_maximum_ydos, 'bo:')
#             plot_projections((redDosObjTrm.dosefiltered + greenDosObjTrm.dosefiltered + blueDosObjTrm.dosefiltered)/3, '3 channel', 'y-', 
#                              threechDosObjTrm.half_maximum_xdos, threechDosObjTrm.half_maximum_ydos, 'yo:')
#             
#         rootFolder = rootFolderClass(path)
#         
# =============================================================================
