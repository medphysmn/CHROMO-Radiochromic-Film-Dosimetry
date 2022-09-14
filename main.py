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
from scipy.signal import medfilt, wiener

sys.path.append(".")
from constants import *
from functions import *
from doseClass import *
from calibrationClass import *

cleanOutputDirectory()
warnings.filterwarnings("ignore")

for unexposed_filepath in unexposed_calibration_list:
    calibrationObjects.append(calibrationClass(cv2.imread(unexposed_filepath), redChannel, greenChannel, blueChannel, 0, 999))
    
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
      
    dose_red_nonfiltered =  inverse_recalibrated_multichannel_response_curve_red(netImage[:,:,redChannel], a_red, b_red, fitResults)
    dose_red_filtered, min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred = dose_calculation_with_filters(dose_red_nonfiltered, netImage[:,:,redChannel], 'r', 0, 0, inverse_recalibrated_multichannel_response_curve_red, inverse_recalibrated_multichannel_response_curve_green, inverse_recalibrated_multichannel_response_curve_blue, a_red, b_red, a_green, b_green, a_blue, b_blue, fitResults)
    redDosObjArr.append(doseClass(dose_red_filtered, min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred))
    
    dose_green_nonfiltered =  inverse_recalibrated_multichannel_response_curve_green(netImage[:,:,greenChannel], a_green, b_green, fitResults)
    dose_green_filtered, min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen = dose_calculation_with_filters(dose_green_nonfiltered, netImage[:,:,greenChannel], 'g', 0, 0, inverse_recalibrated_multichannel_response_curve_red, inverse_recalibrated_multichannel_response_curve_green, inverse_recalibrated_multichannel_response_curve_blue, a_red, b_red, a_green, b_green, a_blue, b_blue, fitResults)
    greenDosObjArr.append(doseClass(dose_green_filtered, min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen))    
    
    dose_blue_nonfiltered =  inverse_recalibrated_multichannel_response_curve_blue(netImage[:,:,greenChannel], a_blue, b_blue, fitResults)
    dose_blue_filtered, min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue = dose_calculation_with_filters(dose_blue_nonfiltered, netImage[:,:,blueChannel], 'b', 0, 0, inverse_recalibrated_multichannel_response_curve_red, inverse_recalibrated_multichannel_response_curve_green, inverse_recalibrated_multichannel_response_curve_blue, a_red, b_red, a_green, b_green, a_blue, b_blue, fitResults)
    blueDosObjArr.append(doseClass(dose_blue_filtered, min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue))  
    
    dose_3ch = (dose_blue_center + dose_red_center + dose_green_center)/3
    bkgx3ch, bkgy3ch  = (bkgxred + bkgxgreen + bkgxblue)/3 , (bkgyred + bkgygreen + bkgyblue)/3   
    dose_3ch_filtered, min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x,half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch = dose_calculation_with_filters(dose_3ch, [], '3ch', bkgx3ch, bkgy3ch, inverse_recalibrated_multichannel_response_curve_red, inverse_recalibrated_multichannel_response_curve_green, inverse_recalibrated_multichannel_response_curve_blue, a_red, b_red, a_green, b_green, a_blue, b_blue, fitResults)
    trheechDosObjArr.append(doseClass(dose_3ch_filtered, min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x, half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch))  

for enum, (redDosObjTrm, greenDosObjTrm, blueDosObjTrm, threechDosObjTrm) in enumerate(zip(redDosObjArr, greenDosObjArr, blueDosObjArr, trheechDosObjArr )):
    
    print("TREATMENT NUMBER " , enum+1, '\n')
    print(" filepath = %s" % (treatment_list[enum]), '\n')
    print('DOSES AND PROFILES: \n')

    plot_dose(redDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Red', '/RED/dose_red', enum)
    plot_dose(greenDosObjTrm.dosefiltered,redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Green', '/GREEN/dose_green', enum)
    plot_dose(blueDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Blue', '/BLUE/dose_blue', enum)
    plot_dose((redDosObjTrm.dosefiltered + greenDosObjTrm.dosefiltered + blueDosObjTrm.dosefiltered)/3, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, '3 channel', '/3CH/dose_3ch', enum)
    plt.show()
    
    #plot_projections(redDosObjTrm.dosefiltered, 'red', 'r-', redDosObjTrm.half_maximum_xdos, redDosObjTrm.half_maximum_ydos, 'ro:')
    #plot_projections(greenDosObjTrm.dosefiltered, 'green', 'g-', greenDosObjTrm.half_maximum_xdos, greenDosObjTrm.half_maximum_ydos, 'go:')
    #plot_projections(blueDosObjTrm.dosefiltered, 'blue', 'b-', blueDosObjTrm.half_maximum_xdos, blueDosObjTrm.half_maximum_ydos, 'bo:')
    #plot_projections((redDosObjTrm.dosefiltered + greenDosObjTrm.dosefiltered + blueDosObjTrm.dosefiltered)/3, '3 channel', 'y-', threechDosObjTrm.half_maximum_xdos, threechDosObjTrm.half_maximum_ydos, 'yo:')
    