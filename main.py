#!/usr/bin/env python
# coding: utf-8

#TODO PROIEZIONI - NET IMAGE - BKG - CORREZIONE LATERALE - FILE CONFIGURAZIONE TXT
#WEINER
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

sys.path.append(".")
from constants import *
from functions import *
from doseClass import *
from calibrationClass import *

cleanOutputDirectory()
createOutputDirectories()
warnings.filterwarnings("ignore")

if medianFilter == True:
    print('Starting denoising of calibration images with median filter...')
    denoiserArg1 = '-d ' + nonFilteredCalibrationPath + ' -f median -k ' + str(medianKernel)
    os.system(denoiserPath + " " + denoiserArg1)
    for file in os.listdir(denoiserFolder):
        if(file.endswith(".tif")):
            move(file,calibrationPath)
    for file1 in os.listdir(path):
        if(file1.endswith(".tif")):
            move(file1,calibrationPath)
    
    print('Starting denoising of treatment images with median filter...')     
    denoiserArg2 = '-d ' + nonFilteredTreatmentPath + ' -f median -k ' + str(medianKernel)
    os.system(denoiserPath + " " + denoiserArg2)
    for file in os.listdir(denoiserFolder):
        if(file.endswith(".tif")):
            move(file,treatmentPath)
    for file1 in os.listdir(path):
        if(file1.endswith(".tif")):
            move(file1,treatmentPath)
else:
    for fileNonFilteredCalibration in os.listdir(nonFilteredCalibrationPath):
        copyfile(fileNonFilteredCalibration, calibrationPath)
    for fileNonFilteredTreatment in os.listdir(nonFilteredTreatmentPath):
            copyfile(fileNonFilteredTreatment, treatmentPath)

if wienerFilter == True:
    print('Starting denoising of calibration images with wiener filter...')
    denoiserArg3 = '-d ' + calibrationPath + ' -f wiener -k ' + str(wienerKernel)
    os.system(denoiserPath + " " + denoiserArg3)
    for file in os.listdir(denoiserFolder):
        if(file.endswith(".tif")):
            dest0 = os.path.join(calibrationPath,file)
            move(file, dest0)
    for file1 in os.listdir(path):
        if(file1.endswith(".tif")):
            dest1 = os.path.join(calibrationPath,file1)
            move(file1, dest1)

    print('Starting denoising of treatment images with wiener filter...')     
    denoiserArg4 = '-d ' + treatmentPath + ' -f wiener -k ' + str(wienerKernel)
    os.system(denoiserPath + " " + denoiserArg4)
    for file in os.listdir(denoiserFolder):
        if(file.endswith(".tif")):
            dest2 = os.path.join(treatmentPath, file)
            move(file, dest2)
    for file1 in os.listdir(path):
        if(file1.endswith(".tif")):
            dest3 = os.path.join(treatmentPath,file1)
            move(file1, dest3)

for unexposed_filepath in unexposed_calibration_list:
    try:
        calibrationObjects.append(calibrationClass(cv2.imread(unexposed_filepath), redChannel, greenChannel, blueChannel, 0, 999))
    except:
        print('WARNING: No unexposed calibration film found')
        
for calibration_filepath in calibration_list:
     reg_search = re.search('.*calibration_(.*)Gy_.*', calibration_filepath)
     calibrationObjects.append(calibrationClass(cv2.imread(calibration_filepath), redChannel, greenChannel, blueChannel, reg_search.group(1), 999))

for i, (unexposed_treatment_filepath, maxdose_treatment_filepath) in enumerate(zip(unexposed_treatment_list, maxdose_treatment_list)):
    unexposedTreatmentObjects.append(calibrationClass(cv2.imread(unexposed_treatment_filepath), redChannel, greenChannel, blueChannel, 999, i))
    maxDoseTreatmentObjects.append(calibrationClass(cv2.imread(maxdose_treatment_filepath), redChannel, greenChannel, blueChannel, 999, i))  
     
calibrationObjects.sort(key=lambda x: x.calibration_dose)
calibration_dose = [x.calibration_dose for x in calibrationObjects]
calibration_red = [x.calibrationRed for x in calibrationObjects]
calibration_green = [x.calibrationGreen for x in calibrationObjects]
calibration_blue = [x.calibrationBlue for x in calibrationObjects]

fitResults, x_max_lsmodel, y_calibration_fit = plotCurves(calibration_dose, calibration_red, calibration_green , calibration_blue)

for i, scan_filepath in enumerate(treatment_list):  
       
    a_red = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationRed, maxDoseTreatmentObjects[i].calibrationRed, fitResults)[0]  
    b_red = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationRed, maxDoseTreatmentObjects[i].calibrationRed, fitResults)[1]  
    a_green = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationGreen, maxDoseTreatmentObjects[i].calibrationGreen, fitResults)[0]  
    b_green = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationGreen, maxDoseTreatmentObjects[i].calibrationGreen, fitResults)[1]  
    a_blue = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationBlue, maxDoseTreatmentObjects[i].calibrationBlue, fitResults)[0]  
    b_blue = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationBlue, maxDoseTreatmentObjects[i].calibrationBlue, fitResults)[1]  
    
    print("TREATMENT NUMBER " , i+1, '\n')
    print(" Treatment file analyzed = %s" % (scan_filepath), '\n')
    
    image = cv2.imread(scan_filepath)
    netImage= image
    
    plotRecalibratedImages(x_max_lsmodel, unexposedTreatmentObjects[i], maxDoseTreatmentObjects[i], recalibrated_multichannel_response_curve_red, recalibrated_multichannel_response_curve_green, recalibrated_multichannel_response_curve_blue, y_calibration_fit, i, a_red, b_red, a_green, b_green, a_blue, b_blue, fitResults)
      
    dose_red =  inverse_recalibrated_multichannel_response_curve_red(netImage[:,:,redChannel], a_red, b_red, fitResults).clip(min=0)
    min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred = dose_calculations(dose_red, 'r', 0, 0)
    redDosObjArr.append(doseClass(dose_red, min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred))
    
    dose_green =  inverse_recalibrated_multichannel_response_curve_green(netImage[:,:,greenChannel], a_green, b_green, fitResults).clip(min=0)
    min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen = dose_calculations(dose_green, 'g', 0, 0)
    greenDosObjArr.append(doseClass(dose_green, min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen))    
    
    dose_blue =  inverse_recalibrated_multichannel_response_curve_blue(netImage[:,:,blueChannel], a_blue, b_blue, fitResults).clip(min=0)
    min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue = dose_calculations(dose_blue, 'b', 0, 0)
    blueDosObjArr.append(doseClass(dose_blue, min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue))  
    
    dose_3ch = (dose_blue_center + dose_red_center + dose_green_center)/3
    bkgx3ch, bkgy3ch  = (bkgxred + bkgxgreen + bkgxblue)/3 , (bkgyred + bkgygreen + bkgyblue)/3   
    min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x,half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch = dose_calculations(dose_3ch, '3ch', bkgx3ch, bkgy3ch)
    trheechDosObjArr.append(doseClass(dose_3ch, min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x, half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch))  

for enum, (redDosObjTrm, greenDosObjTrm, blueDosObjTrm, threechDosObjTrm) in enumerate(zip(redDosObjArr, greenDosObjArr, blueDosObjArr, trheechDosObjArr )):
    
    print("TREATMENT NUMBER " , enum+1, '\n')
    print(" filepath = %s" % (treatment_list[enum]), '\n')
    print('DOSES AND PROFILES: \n')

    plot_dose(redDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Red', '/RED/dose_red', enum)
    plot_dose(greenDosObjTrm.dosefiltered,redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Green', '/GREEN/dose_green', enum)
    plot_dose(blueDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Blue', '/BLUE/dose_blue', enum)
    plot_dose((redDosObjTrm.dosefiltered + greenDosObjTrm.dosefiltered + blueDosObjTrm.dosefiltered)/3, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, '3 channel', '/3CH/dose_3ch', enum)
    plt.show()
    
    if plotProfilesResults == True:
        plot_projections(redDosObjTrm.dosefiltered, 'red', 'r-', redDosObjTrm.half_maximum_xdos, redDosObjTrm.half_maximum_ydos, 'ro:')
        plot_projections(greenDosObjTrm.dosefiltered, 'green', 'g-', greenDosObjTrm.half_maximum_xdos, greenDosObjTrm.half_maximum_ydos, 'go:')
        plot_projections(blueDosObjTrm.dosefiltered, 'blue', 'b-', blueDosObjTrm.half_maximum_xdos, blueDosObjTrm.half_maximum_ydos, 'bo:')
        plot_projections((redDosObjTrm.dosefiltered + greenDosObjTrm.dosefiltered + blueDosObjTrm.dosefiltered)/3, '3 channel', 'y-', threechDosObjTrm.half_maximum_xdos, threechDosObjTrm.half_maximum_ydos, 'yo:')

os._exit(00)