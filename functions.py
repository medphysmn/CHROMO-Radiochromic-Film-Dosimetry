import numpy as np
import matplotlib.pyplot as plt
from scipy import asarray as exp
from scipy.optimize import *
from scipy.interpolate import *
import PIL
import sys
import cv2
import scipy
import math 
import os
import shutil
from sys import exit
from shutil import move, copyfile
from PIL import ImageTk as itk
from PIL import Image as pilimage
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import ImageTk
import re
from contextlib import contextmanager

from calibrationClass import *
from fitResultsSingleChannel import *
from rootFolderClass import *
from doseClass import *

def singleChannelDosimetryGUI(rootFolder, fitFunction, p0red, p0red1, p0green, p0green1, p0blue, p0blue1, p0redexp, p0red1exp, p0greenexp, p0green1exp, p0blueexp, p0blue1exp, a0multichannel, a0multichannel1, maximumIterationsFit, maxdoseRecalibration, cmap, doseRawImageOutputFormat , isodoseDifferenceGy , dimensioneRoiPixel, dimRoiCalibration, redChannel, greenChannel, blueChannel, resolution, dpi, dpiResolution, plotProfilesResults, doseresultsTk, labelImageres, labelImagegreenres, labelImageblueres, singleChannelTk, labelImageredcal, labelImagegreencal, labelImagebluecal):
    multiChannelDosimetry=False
    calibration_dose, calibration_red, calibration_green, calibration_blue, unexposed_caibration_film_maxchannel = getCalibrationdose(rootFolder, redChannel, greenChannel, blueChannel, dimRoiCalibration, multiChannelDosimetry)
    fitResultsInv, fitResults, x_max_lsmodel, y_calibration_fit = fitDataAndPlotCurves(calibration_dose, calibration_red, calibration_green , calibration_blue, rootFolder, fitFunction, multiChannelDosimetry, p0red, p0red1, p0green, p0green1, p0blue, p0blue1, p0redexp, p0red1exp, p0greenexp, p0green1exp, p0blueexp, p0blue1exp, a0multichannel, a0multichannel1, maximumIterationsFit, maxdoseRecalibration, cmap, doseRawImageOutputFormat , isodoseDifferenceGy , dimensioneRoiPixel, dimRoiCalibration, redChannel, greenChannel, blueChannel, resolution, dpi, dpiResolution )

    for i, scan_filepath in enumerate(rootFolder.treatment_list):  
           
        print("TREATMENT NUMBER " , i+1, '\n')
        print(" Treatment file analyzed = %s" % (scan_filepath), '\n')
        
        image = cv2.imread(scan_filepath)
        netImage = image
        
        dose_red =  calculateSingleChannelDose(netImage[:,:,redChannel], fitResultsInv.redFit, fitFunction).clip(min=0)
        min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred = dose_calculations(dose_red, 'r', 0, 0, multiChannelDosimetry, dimensioneRoiPixel)
        redDosObjArr.append(doseClass(dose_red, min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred))
        
        dose_green =  calculateSingleChannelDose(netImage[:,:,greenChannel], fitResultsInv.greenFit, fitFunction).clip(min=0)
        min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen = dose_calculations(dose_green, 'g', 0, 0, multiChannelDosimetry, dimensioneRoiPixel)
        greenDosObjArr.append(doseClass(dose_green, min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen))    
        
        dose_blue =  calculateSingleChannelDose(netImage[:,:,blueChannel], fitResultsInv.blueFit, fitFunction).clip(min=0)
        min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue = dose_calculations(dose_blue, 'b', 0, 0, multiChannelDosimetry, dimensioneRoiPixel)
        blueDosObjArr.append(doseClass(dose_blue, min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue))  
        
    for enum, (redDosObjTrm, greenDosObjTrm, blueDosObjTrm) in enumerate(zip(redDosObjArr, greenDosObjArr, blueDosObjArr)):
        
        #print("TREATMENT NUMBER " , enum+1, '\n')
        #print(" filepath = %s" % (rootFolder.treatment_list[enum]), '\n')
        #print('DOSES AND PROFILES: \n')
    
        plot_dose(redDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Red', '/RED/dose_red', enum, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat)
        plot_dose(greenDosObjTrm.dosefiltered,redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Green', '/GREEN/dose_green', enum, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat)
        plot_dose(blueDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Blue', '/BLUE/dose_blue', enum, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat)
        plt.show()
        
        if plotProfilesResults ==1:
            plot_projections(redDosObjTrm.dosefiltered, 'red', 'r-', redDosObjTrm.half_maximum_xdos, redDosObjTrm.half_maximum_ydos, 'ro:', dpiResolution)
            plot_projections(greenDosObjTrm.dosefiltered, 'green', 'g-', greenDosObjTrm.half_maximum_xdos, greenDosObjTrm.half_maximum_ydos, 'go:', dpiResolution)
            plot_projections(blueDosObjTrm.dosefiltered, 'blue', 'b-', blueDosObjTrm.half_maximum_xdos, blueDosObjTrm.half_maximum_ydos, 'bo:', dpiResolution)
        
        rootFolder = rootFolderClass(path)

    insertResImage(doseresultsTk, rootFolder, labelImageres, rootFolder.outputPath + '/RED/dose_red_treatment_1_figure.png', 452, 300)
    insertResImage(doseresultsTk, rootFolder, labelImagegreenres, rootFolder.outputPath + '/GREEN/dose_green_treatment_1_figure.png', 452, 300)
    insertResImage(doseresultsTk, rootFolder, labelImageblueres, rootFolder.outputPath + '/BLUE/dose_blue_treatment_1_figure.png', 452, 300)
    
    insertResImage(singleChannelTk, rootFolder, labelImageredcal, rootFolder.outputPath + '/RED/response-dose_calibration_plot_red.png', 432, 288)
    insertResImage(singleChannelTk, rootFolder, labelImagegreencal, rootFolder.outputPath + '/GREEN/response-dose_calibration_plot_green.png', 432, 288)
    insertResImage(singleChannelTk, rootFolder, labelImagebluecal, rootFolder.outputPath + '/BLUE/response-dose_calibration_plot_blue.png', 432, 288)
    
    clearVariablesAfterDosimetry()


def multiChannelDosimetryGUI(rootFolder, p0red, p0red1, p0green, p0green1, p0blue, p0blue1, p0redexp, p0red1exp, p0greenexp, p0green1exp, p0blueexp, p0blue1exp, a0multichannel, a0multichannel1, maximumIterationsFit, maxdoseRecalibration, cmap, doseRawImageOutputFormat , isodoseDifferenceGy , dimensioneRoiPixel, dimRoiCalibration, redChannel, greenChannel, blueChannel, resolution, dpi, dpiResolution, plotProfilesResults, doseresultsTk, labelImageres, labelImagegreenres, labelImageblueres, labelImage3chres, multiChannelTk, labelImageredcal1, labelImagegreencal1, labelImagebluecal1, labelImage3chcal1, labelImage3chcalRecal1):
    multiChannelDosimetry=True
    fitFunction='rational'
    #######################################################
    calibration_dose, calibration_red, calibration_green, calibration_blue, unexposed_caibration_film_maxchannel = getCalibrationdose(rootFolder, redChannel, greenChannel, blueChannel, dimRoiCalibration, multiChannelDosimetry)
    
    for i, (unexposed_treatment_filepath, maxdose_treatment_filepath) in enumerate(zip(rootFolder.unexposed_treatment_list, rootFolder.maxdose_treatment_list)):
        unexposed_recaltrtm_image= cv2.imread(unexposed_treatment_filepath)
        ######################################################################
        unexposed_recaltrtm_image_maxchannel = find_max_channel(unexposed_recaltrtm_image,redChannel,greenChannel,blueChannel)
        net_unexposed_recaltrtm_image = unexposed_recaltrtm_image/unexposed_recaltrtm_image_maxchannel
        unexposedTreatmentObjects.append(calibrationClass(net_unexposed_recaltrtm_image, redChannel, greenChannel, blueChannel, 999, i, dimRoiCalibration))
        ######################################################################
        net_maxdose_tretment_image = cv2.imread(maxdose_treatment_filepath)/unexposed_recaltrtm_image_maxchannel
        maxDoseTreatmentObjects.append(calibrationClass(net_maxdose_tretment_image, redChannel, greenChannel, blueChannel, 999, i, dimRoiCalibration))  
             
    fitResultsInv, fitResults, x_max_lsmodel, y_calibration_fit = fitDataAndPlotCurves(calibration_dose, calibration_red, calibration_green , calibration_blue, rootFolder, fitFunction, multiChannelDosimetry, p0red, p0red1, p0green, p0green1, p0blue, p0blue1, p0redexp, p0red1exp, p0greenexp, p0green1exp, p0blueexp, p0blue1exp, a0multichannel, a0multichannel1, maximumIterationsFit, maxdoseRecalibration, cmap, doseRawImageOutputFormat , isodoseDifferenceGy , dimensioneRoiPixel, dimRoiCalibration, redChannel, greenChannel, blueChannel, resolution, dpi, dpiResolution )
    
    for i, (scan_filepath, unexposed_treatment_filepath) in enumerate(zip(rootFolder.treatment_list, rootFolder.unexposed_treatment_list)):  
        
        a_red = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationRed, maxDoseTreatmentObjects[i].calibrationRed, fitResultsInv, maxdoseRecalibration)[0]  
        b_red = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationRed, maxDoseTreatmentObjects[i].calibrationRed, fitResultsInv, maxdoseRecalibration)[1]  
        
        a_green = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationGreen, maxDoseTreatmentObjects[i].calibrationGreen, fitResultsInv, maxdoseRecalibration)[0]  
        b_green = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationGreen, maxDoseTreatmentObjects[i].calibrationGreen, fitResultsInv, maxdoseRecalibration)[1]  
        
        a_blue = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationBlue, maxDoseTreatmentObjects[i].calibrationBlue, fitResultsInv, maxdoseRecalibration)[0]  
        b_blue = calibration_factors_calculator(unexposedTreatmentObjects[i].calibrationBlue, maxDoseTreatmentObjects[i].calibrationBlue, fitResultsInv, maxdoseRecalibration)[1]  
        
        a_3ch = calibration_factors_calculator((unexposedTreatmentObjects[i].calibrationRed + unexposedTreatmentObjects[i].calibrationGreen + unexposedTreatmentObjects[i].calibrationBlue)/3, 
                                                (maxDoseTreatmentObjects[i].calibrationRed + maxDoseTreatmentObjects[i].calibrationGreen + maxDoseTreatmentObjects[i].calibrationBlue)/3, 
                                                fitResultsInv, maxdoseRecalibration)[0]  
        b_3ch = calibration_factors_calculator((unexposedTreatmentObjects[i].calibrationRed + unexposedTreatmentObjects[i].calibrationGreen + unexposedTreatmentObjects[i].calibrationBlue)/3, 
                                                (maxDoseTreatmentObjects[i].calibrationRed + maxDoseTreatmentObjects[i].calibrationGreen + maxDoseTreatmentObjects[i].calibrationBlue)/3, 
                                                fitResultsInv, maxdoseRecalibration)[1] 
        
        print("TREATMENT NUMBER " , i+1, '\n')
        print(" Treatment file analyzed = %s" % (scan_filepath), '\n')
        
        image = cv2.imread(scan_filepath)
        unexposed_treatment_image = cv2.imread(unexposed_treatment_filepath)
        ######################################################################
        unexposed_treatment_image_maxchannel = find_max_channel(unexposed_treatment_image,redChannel,greenChannel,blueChannel) 
        netImage = image/unexposed_treatment_image_maxchannel
        
        # fitResultsInv3chRecalibrated, y_calibration_fit_recalibratedMC = fitDataRecalibrated(unexposedTreatmentObjects[i], maxDoseTreatmentObjects[i], a0multichannel1, a0multichannel1, maximumIterationsFit, maxdoseRecalibration, cmap, doseRawImageOutputFormat , isodoseDifferenceGy , dimensioneRoiPixel, dimRoiCalibration, redChannel, greenChannel, blueChannel, resolution, dpi, dpiResolution )
        
        # plotRecalibratedImages(x_max_lsmodel, unexposedTreatmentObjects[i], maxDoseTreatmentObjects[i], recalibrated_multichannel_response_curve_red, 
        #                        recalibrated_multichannel_response_curve_green, recalibrated_multichannel_response_curve_blue, y_calibration_fit_recalibratedMC, i, 
        #                        a_red, b_red, a_green, b_green, a_blue, b_blue, fitResultsInv, rootFolder, fitFunction, maxdoseRecalibration)
         
        
        plotRecalibratedImages(x_max_lsmodel, unexposedTreatmentObjects[i], maxDoseTreatmentObjects[i], recalibrated_multichannel_response_curve_red, 
                               recalibrated_multichannel_response_curve_green, recalibrated_multichannel_response_curve_blue, y_calibration_fit, i, 
                               a_red, b_red, a_green, b_green, a_blue, b_blue, a_3ch, b_3ch, fitResultsInv, rootFolder, fitFunction, maxdoseRecalibration, multiChannelDosimetry)
          
        
        dose_red =  inverse_recalibrated_multichannel_response_curve_red(netImage[:,:,redChannel], a_red, b_red, fitResultsInv).clip(min=0)
        min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred = dose_calculations(dose_red, 'r', 0, 0, multiChannelDosimetry, dimensioneRoiPixel)
        redDosObjArr.append(doseClass(dose_red, min_red, max_red, avg_red, std_red, half_maximum_red_x, half_maximum_red_y, dose_red_center, bkgxred, bkgyred))
        
        dose_green =  inverse_recalibrated_multichannel_response_curve_green(netImage[:,:,greenChannel], a_green, b_green, fitResultsInv).clip(min=0)
        min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen = dose_calculations(dose_green, 'g', 0, 0, multiChannelDosimetry, dimensioneRoiPixel)
        greenDosObjArr.append(doseClass(dose_green, min_green, max_green, avg_green, std_green, half_maximum_green_x, half_maximum_green_y, dose_green_center, bkgxgreen, bkgygreen))    
        
        dose_blue =  inverse_recalibrated_multichannel_response_curve_blue(netImage[:,:,blueChannel], a_blue, b_blue, fitResultsInv).clip(min=0)
        min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue = dose_calculations(dose_blue, 'b', 0, 0, multiChannelDosimetry, dimensioneRoiPixel)
        blueDosObjArr.append(doseClass(dose_blue, min_blue, max_blue, avg_blue, std_blue, half_maximum_blue_x, half_maximum_blue_y, dose_blue_center, bkgxblue, bkgyblue))  
        
        #dose_3ch = inverse_recalibrated_multichannel_response_curve_3ch(netImage3ch, fitResultsInv3chRecalibrated).clip(min=0) #(dose_blue_center + dose_red_center + dose_green_center)/3 
        netImage3ch = netImage.sum(axis=2)/3 #(netImage[:,:,redChannel] + netImage[:,:,greenChannel] + netImage[:,:,blueChannel)/3
        dose_3ch = inverse_recalibrated_multichannel_response_curve_3ch(netImage3ch, a_3ch, b_3ch, fitResultsInv).clip(min=0) #(dose_blue_center + dose_red_center + dose_green_center)/3 
        bkgx3ch, bkgy3ch  = 0, 0 #(bkgxred + bkgxgreen + bkgxblue)/3 , (bkgyred + bkgygreen + bkgyblue)/3   
        min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x,half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch = dose_calculations(dose_3ch, '3ch', bkgx3ch, bkgy3ch, multiChannelDosimetry, dimensioneRoiPixel)
        trheechDosObjArr.append(doseClass(dose_3ch, min_3ch, max_3ch, avg_3ch, std_3ch, half_maximum_3ch_x, half_maximum_3ch_y, dose_3ch_center, bkgx3ch, bkgy3ch))    
    
    for enum, (redDosObjTrm, greenDosObjTrm, blueDosObjTrm, threechDosObjTrm) in enumerate(zip(redDosObjArr, greenDosObjArr, blueDosObjArr, trheechDosObjArr )):
        
        #print("TREATMENT NUMBER " , enum+1, '\n')
        #print(" filepath = %s" % (rootFolder.treatment_list[enum]), '\n')
        #print('DOSES AND PROFILES: \n')
    
        plot_dose(redDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Red', '/RED/dose_red', enum, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat)
        plot_dose(greenDosObjTrm.dosefiltered,redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Green', '/GREEN/dose_green', enum, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat)
        plot_dose(blueDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos, blueDosObjTrm.maxdos, 'Blue', '/BLUE/dose_blue', enum, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat)
        plot_dose(threechDosObjTrm.dosefiltered, redDosObjTrm.maxdos, greenDosObjTrm.maxdos,blueDosObjTrm.maxdos, '3 channel', '/3CH/dose_3ch', enum, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat)
        plt.show()
        
        if plotProfilesResults==1:
            plot_projections(redDosObjTrm.dosefiltered, 'red', 'r-', redDosObjTrm.half_maximum_xdos, redDosObjTrm.half_maximum_ydos, 'ro:', dpiResolution)
            plot_projections(greenDosObjTrm.dosefiltered, 'green', 'g-', greenDosObjTrm.half_maximum_xdos, greenDosObjTrm.half_maximum_ydos, 'go:', dpiResolution)
            plot_projections(blueDosObjTrm.dosefiltered, 'blue', 'b-', blueDosObjTrm.half_maximum_xdos, blueDosObjTrm.half_maximum_ydos, 'bo:', dpiResolution)
            plot_projections(threechDosObjTrm.dosefiltered, '3 channel', 'y-', threechDosObjTrm.half_maximum_xdos, threechDosObjTrm.half_maximum_ydos, 'yo:', dpiResolution)
            
        rootFolder = rootFolderClass(path)
    
    insertResImage(doseresultsTk, rootFolder, labelImageres, rootFolder.outputPath + '/RED/dose_red_treatment_1_figure.png', 452, 300)
    insertResImage(doseresultsTk, rootFolder, labelImagegreenres, rootFolder.outputPath + '/GREEN/dose_green_treatment_1_figure.png', 452, 300)
    insertResImage(doseresultsTk, rootFolder, labelImageblueres, rootFolder.outputPath + '/BLUE/dose_blue_treatment_1_figure.png', 452, 300)
    insertResImage(doseresultsTk, rootFolder, labelImage3chres, rootFolder.outputPath + '/3CH/dose_3ch_treatment_1_figure.png', 452, 300)
    
    
    insertResImage(multiChannelTk, rootFolder, labelImageredcal1, rootFolder.outputPath + '/RED/response-dose_calibration_plot_red.png', 422, 240)
    insertResImage(multiChannelTk, rootFolder, labelImagegreencal1, rootFolder.outputPath + '/GREEN/response-dose_calibration_plot_green.png', 422, 240)
    insertResImage(multiChannelTk, rootFolder, labelImagebluecal1, rootFolder.outputPath + '/BLUE/response-dose_calibration_plot_blue.png', 422, 240)
    insertResImage(multiChannelTk, rootFolder, labelImage3chcal1, rootFolder.outputPath + '/3CH/dose-response_calibration_plot_3ch.png', 422, 240)
    insertResImage(multiChannelTk, rootFolder, labelImage3chcalRecal1, rootFolder.outputPath + '/3CH/dose-response_recalibrated_plot_treatment_1.png', 422, 240)

    clearVariablesAfterDosimetry()
        

def clearVariablesAfterDosimetry():
    calibrationObjects.clear()
    unexposedTreatmentObjects.clear()
    maxDoseTreatmentObjects.clear()
    redDosObjArr.clear()
    greenDosObjArr.clear()
    blueDosObjArr.clear()
    trheechDosObjArr.clear()
        
def cleanOutputDirectory(rootFolder):
    try:
        shutil.rmtree(os.path.join(rootFolder.dataPath, 'OUTPUT'))
    except:
        ...

def createOutputDirectories(rootFolder):
    try:
        rootFolder = rootFolderClass(path)
        os.mkdir(os.path.join(rootFolder.dataPath, 'OUTPUT'))
        os.mkdir(os.path.join(rootFolder.outputPath, '_CALIBRATION_FILTERED'))
        os.mkdir(os.path.join(rootFolder.outputPath, '_TREATMENT_FILTERED'))
    except:
        ...
        
def createOutputDirectoriesOnlyChannels(rootFolder):
    rootFolder = rootFolderClass(path)
    os.mkdir(os.path.join(rootFolder.outputPath, '3CH'))
    os.mkdir(os.path.join(rootFolder.outputPath, 'BLUE'))
    os.mkdir(os.path.join(rootFolder.outputPath, 'GREEN'))
    os.mkdir(os.path.join(rootFolder.outputPath, 'RED'))
        
def selectDirectory():
    global path
    browse = tk.Tk()
    browse.withdraw()
    browse.attributes('-topmost', True)
    path = filedialog.askdirectory(title='select root folder') + '/'
    return path
        
def insertImage(r, rootFolder, labelImage, image):
    newimage = ImageTk.PhotoImage(pilimage.open(image).resize((500,500)))
    labelImage.configure(image=newimage)
    labelImage.photo = newimage
    #print("updated image")    
    
def insertResImage(r, rootFolder, labelImage, image, w, h):
    newimage = ImageTk.PhotoImage(pilimage.open(image).resize((w,h)))
    labelImage.configure(image=newimage)
    labelImage.photo = newimage
    #print("updated image")   

import subprocess 
def median(rootFolder, label, r, labelImage, medianKernel):
    cleanOutputDirectory(rootFolder)
    createOutputDirectories(rootFolder)
    createOutputDirectoriesOnlyChannels(rootFolder)
    print('Starting denoising of calibration images with median filter...')
    denoiserArg1 = '-d ' + rootFolder.nonFilteredCalibrationPath + ' -f median -k ' + str(medianKernel.get())
    os.system(rootFolder.denoiserPath + " " + denoiserArg1)
    for file in os.listdir(rootFolder.denoiserFolder):
        if(file.endswith(".tif")):
            move(file,rootFolder.calibrationPath)
    for file1 in os.listdir(rootFolder.path):
        if(file1.endswith(".tif")):
            move(file1,rootFolder.calibrationPath)
    
    print('Starting denoising of treatment images with median filter...')   
    denoiserArg2 = '-d ' + rootFolder.nonFilteredTreatmentPath + ' -f median -k ' + str(medianKernel.get())
    os.system(rootFolder.denoiserPath + " " + denoiserArg2)
    for file in os.listdir(rootFolder.denoiserFolder):
        if(file.endswith(".tif")):
            move(file,rootFolder.treatmentPath)
    for file1 in os.listdir(rootFolder.path):
        if(file1.endswith(".tif")):
            move(file1,rootFolder.treatmentPath)
            
    label.config(text="MEDIAN FILTER APPLIED")
    insertImage(r, rootFolder, labelImage, rootFolder.treatment_list[0])

def wiener(rootFolder, wienerCalibrationPath, wienerTreatmentPath, label, r, labelImage, deleteFolders, wienerKernel):
    if deleteFolders:
        cleanOutputDirectory(rootFolder)
        createOutputDirectories(rootFolder)
        createOutputDirectoriesOnlyChannels(rootFolder)   
    print('Starting denoising of calibration images with wiener filter...')
    denoiserArg3 = '-d ' + wienerCalibrationPath + ' -f wiener -k ' + str(wienerKernel.get())
    os.system(rootFolder.denoiserPath + " " + denoiserArg3)
    for file in os.listdir(rootFolder.denoiserFolder):
        if(file.endswith(".tif")):
            dest0 = os.path.join(rootFolder.calibrationPath,file)
            move(file, dest0)
    for file1 in os.listdir(rootFolder.path):
        if(file1.endswith(".tif")):
            dest1 = os.path.join(rootFolder.calibrationPath,file1)
            move(file1, dest1)

    print('Starting denoising of treatment images with wiener filter...')     
    denoiserArg4 = '-d ' + wienerTreatmentPath + ' -f wiener -k ' + str(wienerKernel.get())
    os.system(rootFolder.denoiserPath + " " + denoiserArg4)
    for file in os.listdir(rootFolder.denoiserFolder):
        if(file.endswith(".tif")):
            dest2 = os.path.join(rootFolder.treatmentPath, file)
            move(file, dest2)
    for file1 in os.listdir(rootFolder.path):
        if(file1.endswith(".tif")):
            dest3 = os.path.join(rootFolder.treatmentPath,file1)
            move(file1, dest3)
    
    label.config(text="WIENER FILTER APPLIED")
    insertImage(r, rootFolder, labelImage, rootFolder.treatment_list[0])

def medianAndWiener(rootFolder, label, r, labelImage, medianKernel, wienerKernel):
    cleanOutputDirectory(rootFolder)
    createOutputDirectories(rootFolder)
    createOutputDirectoriesOnlyChannels(rootFolder)
    median(rootFolder, label, r, labelImage, medianKernel)
    wiener(rootFolder, rootFolder.calibrationPath, rootFolder.treatmentPath, label, r, labelImage, False, wienerKernel)
    
    label.config(text="WIENER AND MEDIAN FILTERS APPLIED")
    insertImage(r, rootFolder, labelImage, rootFolder.treatment_list[0])

def noDenoising(rootFolder, label, r, labelImage):
    cleanOutputDirectory(rootFolder)
    shutil.copytree(rootFolder.nonFilteredCalibrationPath,rootFolder.calibrationPath)
    shutil.copytree(rootFolder.nonFilteredTreatmentPath, rootFolder.treatmentPath)
    createOutputDirectories(rootFolder)
    createOutputDirectoriesOnlyChannels(rootFolder)
    label.config(text="NO FITLERS APPLIED")
    insertImage(r, rootFolder, labelImage, rootFolder.nonFilteredTreatment_list[0])

        
def a_recalibration(yp1, yp2, y1, y2):
    return (y2*yp1-y1*yp2)/(y2-y1)

def b_recalibration(yp1, yp2, y1, y2):
    return (yp2-yp1)/(y2-y1)

def rational(x, a, b, c):
    return a + b/(x+c)

def rational_inverse(x, a, b, c):
    return (b +a*c - x*c)/(x-a)

def exponential(x, a, b, c):
    return (a*np.exp(-x/b) + c)

def exponential_inverse(x, a, b, c): #TODO ORA È SEMPLICE ESPONENZIALE MA DOVRESTI FARE L'INVERSA
    return (-b)*np.log((x-c)/a) 

def multichannel_model(a, x): #x e' la dose
    return a[0] + a[1]/(x+a[2])

def multichannel_function(a, x, y):
    return multichannel_model(a, x) - y

def jac(a, x, y):
    J = np.empty((x.size, a.size))
    J[:, 0] = 1
    J[:, 1] = 1/(x + a[2])
    J[:, 2] = (-a[1])/(x+a[2])**2
    return J

def multichannel_function_inverse(a, x, y):
    return multichannel_model_inverse(a, x) - y 
    
def multichannel_model_inverse(a, x):
    return (a[1] + a[0]*a[2] - a[2]*x)/(x - a[0])

def jac_inverse(a, x, y):
    J = np.empty((x.size, a.size))
    J[:, 0] = (-a[1])/(x-a[0])**2
    J[:, 1] = 1/(x - a[0])
    J[:, 2] = -1
    return J

def recalibrated_multichannel_response_curve_red(x, a_red, b_red, fitResults):
    return a_red + b_red*multichannel_model(fitResults.x, x)
def inverse_recalibrated_multichannel_response_curve_red(y, a_red, b_red, fitResults):
    return (fitResults.x[1]*b_red + fitResults.x[0]*b_red*fitResults.x[2] + a_red*fitResults.x[2] - y*fitResults.x[2])/(y - a_red - fitResults.x[0]*b_red) #calcolato aniliticamente l'inverso
#inverse_recalibrated_multichannel_response_curve_red = inversefunc(recalibrated_multichannel_response_curve_red)
def recalibrated_multichannel_response_curve_green(x, a_green, b_green, fitResults):
    return a_green + b_green*multichannel_model(fitResults.x, x) 
def inverse_recalibrated_multichannel_response_curve_green(y, a_green, b_green, fitResults):
    return (fitResults.x[1]*b_green + fitResults.x[0]*b_green*fitResults.x[2] + a_green*fitResults.x[2] - y*fitResults.x[2])/(y - a_green - fitResults.x[0]*b_green)
def recalibrated_multichannel_response_curve_blue(x, a_blue, b_blue, fitResults):
    return a_blue + b_blue*multichannel_model(fitResults.x, x)
def inverse_recalibrated_multichannel_response_curve_blue(y, a_blue, b_blue, fitResults):
    return (fitResults.x[1]*b_blue + fitResults.x[0]*b_blue*fitResults.x[2] + a_blue*fitResults.x[2] - y*fitResults.x[2])/(y - a_blue - fitResults.x[0]*b_blue) 
def recalibrated_multichannel_response_curve_3ch(x, a_3ch, b_3ch, fitResults):
    return a_3ch + b_3ch*multichannel_model(fitResults.x, x)
def inverse_recalibrated_multichannel_response_curve_3ch(y, a_3ch, b_3ch, fitResults):
    return (fitResults.x[1]*b_3ch + fitResults.x[0]*b_3ch*fitResults.x[2] + a_3ch*fitResults.x[2] - y*fitResults.x[2])/(y - a_3ch - fitResults.x[0]*b_3ch) 
# def recalibrated_multichannel_response_curve_3ch(x, fitResultsRecal):
#     return multichannel_model(fitResultsRecal.x, x)
# def inverse_recalibrated_multichannel_response_curve_3ch(x, fitResultsRecal):
#     return (multichannel_model_inverse(fitResultsRecal.x, x)) 

def calculateSingleChannelDose(y, fitResultsSingle, fitFunction):
    if fitFunction=='rational':
        return (fitResultsSingle[1] + fitResultsSingle[0]*fitResultsSingle[2] - y*fitResultsSingle[2])/(y-fitResultsSingle[0]) 
        # (b +a*c - x*c)/(x-a)
    elif fitFunction=='exponential':
        return -fitResultsSingle[1]*np.log((y-fitResultsSingle[2])/fitResultsSingle[0])
        # (-b)*np.log((x-c)/a)
    else:
        raise Exception("Choose a valid fitting function: rational or exponential")               

def averageImages(images):
    sumIm = 0
    for im in images:
        sumIm += im
    return im/len(images)

def create_inverse_spline(spline):    
    def inverse_spline(x_array):
        if type(x_array) is np.float64:
            x_array
            return return_inverse(x_array, spline)
        else:
            shape = np.shape(x_array)
            dim = len(shape)
            y = np.zeros(shape)
            
            if dim == 1:
                for i, x in enumerate(x_array):
                    y[i] = return_inverse(x, spline)
                    
            else:                
                for i in range(shape[0]):
                    for j in range(shape[1]):
                        x = x_array[i, j]
                        y[i, j] = return_inverse(x, spline)
            return y 
    return inverse_spline

def return_inverse(x, spline):
    def to_minimise(y):
        return (spline(y) - x)**2
    result = minimize(to_minimise, [6])
    return result.x

def projection(image):
    proiezionex = []
    proiezioney = []
    sizex, sizey = image.shape
    for i in range(0,sizey):
        cumsumy = 0
        for j in range(0, sizex):
            cumsumy += image[i][j]
        proiezioney.append(cumsumy)
    proiezioney_arr = np.asanyarray(proiezioney)
    
    for i in range(0,sizex):
        cumsumx = 0
        for j in range(0, sizey):
            cumsumx += image[j][i]
        proiezionex.append(cumsumx)
    proiezionex_arr = np.asanyarray(proiezionex)
    return(proiezionex_arr, proiezioney_arr)

def projectionSingle(image):
    sizex, sizey = image.shape
    yprofile = image[: , int(sizey/2)]
    xprofile = image[int(sizex/2) , :]
    return(xprofile, yprofile)

def openresultfolder(rootFolder):
    os.startfile(rootFolder.outputPath)
    
def fitDataAndPlotCurves(calibration_dose, calibration_red, calibration_green, calibration_blue, rootFolder, fitFunction, multiChannelDosimetry, p0red, p0red1, p0green, p0green1, p0blue, p0blue1, p0redexp, p0red1exp, p0greenexp, p0green1exp, p0blueexp, p0blue1exp, a0multichannel, a0multichannel1, maximumIterationsFit, maxdoseRecalibration, cmap, doseRawImageOutputFormat , isodoseDifferenceGy , dimensioneRoiPixel, dimRoiCalibration, redChannel, greenChannel, blueChannel, resolution, dpi, dpiResolution ):
    
    if multiChannelDosimetry:
        pv_label = "NET PV"
    else:
        pv_label = "PV"
    d = np.linspace(np.min(calibration_dose), np.max(calibration_dose))
    r = np.linspace(np.min(calibration_red), np.max(calibration_red))
    g = np.linspace(np.min(calibration_green), np.max(calibration_green))
    b = np.linspace(np.min(calibration_blue), np.max(calibration_blue))
    x_max_lsmodel = 0 
    y_calibration_fit = []
    y_calibration_fit_inv = []
    
    
    #RED CURVES
    if fitFunction == 'rational':
        poptRed = curve_fit(rational, calibration_dose, calibration_red, p0red, maxfev=maximumIterationsFit)[0]
        plt.plot(d, rational(d, *poptRed), 'r-', label='fitted ' + fitFunction + ' model')
    if fitFunction == 'exponential':
        poptRed = curve_fit(exponential, calibration_dose, calibration_red, p0redexp, maxfev=maximumIterationsFit)[0]
        plt.plot(d, exponential(d, *poptRed), 'r-', label='fitted ' + fitFunction + ' model')
    plt.scatter(calibration_dose, calibration_red, color='red', label='red data')
    plt.xlabel("DOSE (Gy)")
    plt.ylabel(pv_label)
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.redPath + "/dose-response_calibration_plot_red.png", format='png')
    plt.show()

    if fitFunction == 'rational':
        poptRedInverse = curve_fit(rational_inverse, calibration_red, calibration_dose, p0red1, maxfev=maximumIterationsFit)[0]
        plt.plot(r, rational_inverse(r, *poptRedInverse), 'r-', label='fitted ' + fitFunction + ' model')
    if fitFunction == 'exponential':
        poptRedInverse = curve_fit(exponential_inverse, calibration_red, calibration_dose, p0red1exp, maxfev=maximumIterationsFit)[0]
        plt.plot(r, exponential_inverse(r, *poptRedInverse), 'r-', label='fitted ' + fitFunction + ' model')
    plt.scatter(calibration_red, calibration_dose, color='red', label='red data')
    plt.xlabel(pv_label)
    plt.ylabel("DOSE (Gy)")
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.redPath + "/response-dose_calibration_plot_red.png", format='png')
    plt.show()

    #GREEN CURVES
    if fitFunction == 'rational':
        poptGreen = curve_fit(rational, calibration_dose, calibration_green, p0green, maxfev=maximumIterationsFit)[0]
        plt.plot(d, rational(d, *poptGreen), 'g-', label='fitted ' + fitFunction + ' model')
    if fitFunction == 'exponential':
        poptGreen = curve_fit(exponential, calibration_dose, calibration_green, p0greenexp, maxfev=maximumIterationsFit)[0]
        plt.plot(d, exponential(d, *poptGreen), 'g-', label='fitted ' + fitFunction + ' model')
    plt.scatter(calibration_dose, calibration_green, color='green', label='green data')
    plt.xlabel("DOSE (Gy)")
    plt.ylabel(pv_label)
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.greenPath + "/dose-response_calibration_plot_green.png", format='png')
    plt.show()

    if fitFunction == 'rational':
        poptGreenInverse = curve_fit(rational_inverse, calibration_green, calibration_dose, p0green1, maxfev=maximumIterationsFit)[0]
        plt.plot(g, rational_inverse(g, *poptGreenInverse), 'g-', label='fitted ' + fitFunction + ' model')
    if fitFunction == 'exponential':
        poptGreenInverse = curve_fit(exponential_inverse, calibration_green, calibration_dose, p0green1exp, maxfev=maximumIterationsFit)[0]
        plt.plot(g, exponential_inverse(g, *poptGreenInverse), 'g-', label='fitted ' + fitFunction + ' model')
    plt.scatter(calibration_green, calibration_dose, color='green', label='green data')
    plt.xlabel(pv_label)
    plt.ylabel("DOSE (Gy)")
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.greenPath + "/response-dose_calibration_plot_green.png", format='png')
    plt.show()

    #BLUE CURVES
    if fitFunction == 'rational':
        poptBlue = curve_fit(rational, calibration_dose, calibration_blue, p0blue, maxfev=maximumIterationsFit)[0]
        plt.plot(d, rational(d, *poptBlue), 'b-', label='fitted ' + fitFunction + ' model')
    if fitFunction == 'exponential':
        poptBlue = curve_fit(exponential, calibration_dose, calibration_blue, p0blueexp, maxfev=maximumIterationsFit)[0]
        plt.plot(d, exponential(d, *poptBlue), 'b-', label='fitted ' + fitFunction + ' model')
    plt.scatter(calibration_dose, calibration_blue, color='blue', label='blue data')
    plt.xlabel("DOSE (Gy)")
    plt.ylabel(pv_label)
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.bluePath + "/dose-response_calibration_plot_blue.png", format='png')
    plt.show()

    if fitFunction == 'rational':
        poptBlueInverse = curve_fit(rational_inverse, calibration_blue, calibration_dose, p0blue1, maxfev=maximumIterationsFit)[0]
        plt.plot(b, rational_inverse(b, *poptBlueInverse), 'b-', label='fitted ' + fitFunction + ' model')
    if fitFunction == 'exponential':
        poptBlueInverse = curve_fit(exponential_inverse, calibration_blue, calibration_dose, p0blue1exp, maxfev=maximumIterationsFit)[0]
        plt.plot(b, exponential_inverse(b, *poptBlueInverse), 'b-', label='fitted ' + fitFunction + ' model')
    plt.scatter(calibration_blue, calibration_dose, color='blue', label='blue data')
    plt.xlabel(pv_label)
    plt.ylabel("DOSE (Gy)")
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.bluePath + "/response-dose_calibration_plot_blue.png", format='png')
    plt.show()
    
    fitResults = fitResultsSingleChannel(poptRed, poptGreen, poptBlue)
    fitResults_inv = fitResultsSingleChannel(poptRedInverse, poptGreenInverse, poptBlueInverse)
    # print(poptRedInverse)
    # print(poptGreenInverse)
    # print(poptBlueInverse)
    
    if multiChannelDosimetry:
        
        #MULTICHANNELCURVES
        xi = np.append(np.asanyarray(calibration_dose), np.asanyarray(calibration_dose))
        x = np.append( xi, np.asanyarray(calibration_dose))
        x_max_lsmodel = max(x)
    
        yi = np.append(np.asanyarray(calibration_red), np.asanyarray(calibration_green))
        y = np.append( yi, np.asanyarray(calibration_blue))
        
        fitResults = least_squares(multichannel_function, a0multichannel1, jac=jac, args=(x, y), verbose=1)
        fitResults.x
        
        x_calibration_fit = np.linspace(0, x_max_lsmodel)
        y_calibration_fit = multichannel_model(fitResults.x, x_calibration_fit)
    
        plt.scatter(calibration_dose, calibration_red, color='red', label='red data')
        plt.scatter(calibration_dose, calibration_green, color='green', label='green data')
        plt.scatter(calibration_dose, calibration_blue, color='blue', label='blue data')
        plt.plot(x_calibration_fit, y_calibration_fit, label='fitted multichannel LS model', ls='dashed')
        plt.xlabel("DOSE (GY)")
        plt.ylabel(pv_label)
        plt.legend(loc='upper right')
        plt.savefig(rootFolder.tchPath + "/dose-response_calibration_plot_3ch.png", format='png')
        plt.show()
        
        xi = np.append(np.asanyarray(calibration_red), np.asanyarray(calibration_green))
        x = np.append(xi, np.asanyarray(calibration_blue))
        yi = np.append(np.asanyarray(calibration_dose), np.asanyarray(calibration_dose))
        y = np.append(yi, np.asanyarray(calibration_dose))
    
        fitResults_inv = least_squares(multichannel_function_inverse, a0multichannel, args=(x, y), max_nfev=maximumIterationsFit*1000, verbose=1)
        fitResults_inv.x
    
        x_calibration_fit = np.linspace(min(x), max(x))
        y_calibration_fit_inv = multichannel_model_inverse(fitResults_inv.x, x_calibration_fit)
        plt.scatter(calibration_red, calibration_dose, color='red', label='red data')
        plt.scatter(calibration_green, calibration_dose,color='green', label='green data')
        plt.scatter(calibration_blue, calibration_dose, color='blue', label='blue data')
        plt.plot(x_calibration_fit, y_calibration_fit_inv, label='fitted multichannel LS model', ls='dashed')
        plt.xlabel(pv_label)
        plt.ylabel("DOSE (Gy)")
        plt.legend(loc='upper right')
        plt.savefig(rootFolder.tchPath + "/response-dose_calibration_plot_3ch.png", format='png')
        plt.show()
        
    return fitResults_inv, fitResults, x_max_lsmodel, y_calibration_fit_inv

# def fitDataRecalibrated(unexposedTreatmentObjects, maxDoseTreatmentObjects, a0multichannel, a0multichannel1, maximumIterationsFit, maxdoseRecalibration, cmap, doseRawImageOutputFormat , isodoseDifferenceGy , dimensioneRoiPixel, dimRoiCalibration, redChannel, greenChannel, blueChannel, resolution, dpi, dpiResolution ):
    
#     xi = np.append(np.asanyarray([unexposedTreatmentObjects.calibrationRed, maxDoseTreatmentObjects.calibrationRed]), 
#                    np.asanyarray([unexposedTreatmentObjects.calibrationGreen, maxDoseTreatmentObjects.calibrationGreen]))
#     x = np.append(xi, np.asanyarray([unexposedTreatmentObjects.calibrationBlue, maxDoseTreatmentObjects.calibrationBlue]))
#     yi = np.append(np.array([0, maxdoseRecalibration]), np.array([0, maxdoseRecalibration]))
#     y = np.append(yi, np.array([0, maxdoseRecalibration]))
    
#     x_calibration_fit = np.linspace(min(x), max(x))
#     fitResults_inv = least_squares(multichannel_function_inverse, a0multichannel, jac=jac_inverse, method='lm', args=(x, y), max_nfev=maximumIterationsFit*1000, verbose=1)
#     fitResults_inv.x
    
#     y_calibration_fit_recal = multichannel_model(fitResults_inv.x, x_calibration_fit)

    
#     return fitResults_inv, y_calibration_fit_recal

def getCalibrationdose(rootFolder, redChannel, greenChannel, blueChannel, dimRoiCalibration, multiChannelDosimetry):
    for unexposed_filepath in rootFolder.unexposed_calibration_list:    
        try:
            unexposed_caibration_film = cv2.imread(unexposed_filepath)
            unexposed_caibration_film_maxchannel = find_max_channel(unexposed_caibration_film,redChannel,greenChannel,blueChannel)
            ######################################################################
            if multiChannelDosimetry:
                net_unexposed_caibration_film = unexposed_caibration_film/unexposed_caibration_film_maxchannel
            else :
                net_unexposed_caibration_film = unexposed_caibration_film
            calibrationObjects.append(calibrationClass(net_unexposed_caibration_film, redChannel, greenChannel, blueChannel, 0, 999, dimRoiCalibration))
        except:
            if multiChannelDosimetry:
                print('WARNING: No unexposed calibration film found')
                
    for calibration_filepath in rootFolder.calibration_list:
        reg_search = re.search('.*calibration_(.*)Gy_.*', calibration_filepath)
        if multiChannelDosimetry:
            ######################################################################
            net_calibration_dose = cv2.imread(calibration_filepath)/unexposed_caibration_film_maxchannel
        else:
            net_calibration_dose = cv2.imread(calibration_filepath)
        calibrationObjects.append(calibrationClass(net_calibration_dose, redChannel, greenChannel, blueChannel, reg_search.group(1), 999, dimRoiCalibration))
    
    calibrationObjects.sort(key=lambda x: x.calibration_dose)
    calibration_dose = [x.calibration_dose for x in calibrationObjects]
    calibration_red = [x.calibrationRed for x in calibrationObjects]
    calibration_green = [x.calibrationGreen for x in calibrationObjects]
    calibration_blue = [x.calibrationBlue for x in calibrationObjects]
    
    return calibration_dose, calibration_red, calibration_green, calibration_blue, unexposed_caibration_film_maxchannel

def plotRecalibratedImages(x_max_lsmodel, unexposedObject, maxDoseObject, recalibrated_multichannel_response_curve_red, recalibrated_multichannel_response_curve_green, 
                           recalibrated_multichannel_response_curve_blue, y_calibration_fit, treatmentNumber, a_red, b_red, a_green, b_green, a_blue, b_blue, a_3ch, b_3ch, fitResults, rootFolder, fitFunction, maxdoseRecalibration, multiChannelDosimetry):
        if multiChannelDosimetry:
            pv_label = "NET PV"
        else:
            pv_label = "PV"
        x_calibration_fit = np.linspace(0, x_max_lsmodel)
        y_calibration_fit_red = recalibrated_multichannel_response_curve_red(x_calibration_fit, a_red, b_red, fitResults)
        y_calibration_fit_green = recalibrated_multichannel_response_curve_green(x_calibration_fit,a_green, b_green, fitResults)
        y_calibration_fit_blue = recalibrated_multichannel_response_curve_blue(x_calibration_fit,a_blue, b_blue, fitResults)
        y_calibration_fit_3ch = recalibrated_multichannel_response_curve_3ch(x_calibration_fit,a_3ch, b_3ch, fitResults)
        plt.title("TREATMENT "+ str(treatmentNumber + 1))
        plt.scatter(0, unexposedObject.calibrationRed, color='purple', label='red recalibration data')
        plt.scatter(0, unexposedObject.calibrationGreen, color='lime', label='green recalibration data')
        plt.scatter(0, unexposedObject.calibrationBlue, color='dodgerblue', label='blue recalibration data')
        plt.scatter(0, (unexposedObject.calibrationRed + unexposedObject.calibrationGreen + unexposedObject.calibrationBlue)/3, color='black', label='MC recalibration data')
        plt.scatter(maxdoseRecalibration, maxDoseObject.calibrationRed, color='purple')
        plt.scatter(maxdoseRecalibration, maxDoseObject.calibrationGreen, color='lime')
        plt.scatter(maxdoseRecalibration, maxDoseObject.calibrationBlue, color='dodgerblue')
        plt.scatter(maxdoseRecalibration, (maxDoseObject.calibrationRed + maxDoseObject.calibrationGreen + maxDoseObject.calibrationBlue)/3, color='black')
        plt.plot(x_calibration_fit, y_calibration_fit_red, 'purple', label='recalibrated RED ' + fitFunction + ' model')
        plt.plot(x_calibration_fit, y_calibration_fit_green, 'lime', label='recalibrated GREEN ' + fitFunction + ' model')
        plt.plot(x_calibration_fit, y_calibration_fit_blue, 'dodgerblue', label= 'recalibrated BLUE ' + fitFunction + ' model')
        plt.plot(x_calibration_fit, y_calibration_fit_3ch, label='recalibrated mc fit of treatment ' + str(treatmentNumber + 1), ls='dashed')
        plt.xlabel("DOSE (Gy)")
        plt.ylabel(pv_label)
        plt.legend(loc='upper right')
        plt.savefig(rootFolder.tchPath + "/dose-response_recalibrated_plot_" + "treatment_" + str(treatmentNumber + 1) + ".png", format='png')
        plt.show()

def calibration_factors_calculator(zeroResponse, maxdoseResponse, fitResults, maxdoseRecalibration):
        a = a_recalibration(zeroResponse, #x1
                            maxdoseResponse, #x2
                            multichannel_model(fitResults.x, 0), #n1
                            multichannel_model(fitResults.x, maxdoseRecalibration)) #n2
        b = b_recalibration(zeroResponse,
                            maxdoseResponse,
                            multichannel_model(fitResults.x, 0), #n1
                            multichannel_model(fitResults.x, maxdoseRecalibration)) #n2 
        return (a, b)

def find_nearest(array, value):
    length = len(array)
    middle_index = int(length // 2)
    array1 = array[:middle_index]
    array2 = array[middle_index:]
    
    array1 = np.asarray(array1)
    array2 = np.asarray(array2)
    idx1 = (np.abs(array1 - value)).argmin()
    idx2 = (np.abs(array2 - value)).argmin() + middle_index
    return (idx1, idx2)

def find_fwhm_analytical(dose, halfvaluex, halfvaluey, stringColor, dpiResolution):
    projx, projy = projectionSingle(dose) 
    idx1, idx2 = find_nearest(projx, halfvaluex)
    idy1, idy2 = find_nearest(projy, halfvaluey)
    fwhmx = (idx2 - idx1)*dpiResolution
    fwhmy = (idy2 - idy1)*dpiResolution

    print('FWHM of ' + stringColor + ' x dose: ' + str(round(fwhmx,3)) +' mm')
    print('FWHM of ' + stringColor + ' y dose: ' + str(round(fwhmy,3)) +' mm')
    return (fwhmx, fwhmy)

def calculate_final_dose_statistics(dose, dose_center, dose_shapex, dose_shapey):
    dose_background_mean_x, dose_background_mean_y = calculatebkg(dose, dose_shapex, dose_shapey )
    maxd = np.round(np.max(dose_center),3)
    avg = np.round(np.mean(dose_center),3)
    mind = np.round(np.min(dose_center),3)
    std = np.round(np.std(dose_center),3)
    half_maximum_x = np.round((avg + dose_background_mean_x)/2,3)
    half_maximum_y = np.round((avg + dose_background_mean_y)/2,3)
    return dose_background_mean_x, dose_background_mean_y, maxd, avg, mind, std, half_maximum_x, half_maximum_y

def plot_dose(dose, max_red, max_green, max_blue, stringcolor, stringoutput, i, rootFolder, resolution, dpi, dpiResolution, isodoseDifferenceGy, cmap, doseRawImageOutputFormat):
    shape = np.shape(dose)
    x = np.arange(shape[1])*dpiResolution
    y = np.arange(shape[0])*dpiResolution
    xx, yy = np.meshgrid(x, y)
    levels = np.arange(0, int(math.ceil(max(max_red,max_green,max_blue)+1)), isodoseDifferenceGy)
    
    from PIL import Image
    doseImage = Image.fromarray(dose)
    doseImage.save(rootFolder.outputPath + stringoutput+ "_treatment_" +str(i+1) + "_raw." + doseRawImageOutputFormat)
        
    
    plt.figure()
    c = plt.contourf(xx, yy, dose, cmap=cmap, levels=levels)
    plt.colorbar(c, label="DOSE (Gy)")
    plt.title(stringcolor.upper() + " DOSE")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.axis("scaled")
    plt.grid(True)
    plt.savefig(rootFolder.outputPath + stringoutput + "_treatment_" + str(i+1) + "_figure.png", format='png')
    #print("Dose image saved as: \n" + rootFolder.outputPath + stringoutput+ "_treatment_" + str(i+1) + "_raw." + doseRawImageOutputFormat + " \n" + rootFolder.outputPath + stringoutput+str(i) + "_figure.png \n")
    plt.show()

#TODO mettere a posto!!!
def calculatebkg(dose, dose_shapex, dose_shapey):
    bkgx = np.mean(dose[0 : int(dose_shapex), 0 : 5])
    bkgy = np.mean(dose[0 : 5, 0 : int(dose_shapey)])
    return bkgx, bkgy

def find_max_channel(img,redChannel,greenChannel,blueChannel):
    avgR = np.mean(img[:,:,redChannel])
    avgG = np.mean(img[:,:,greenChannel])
    avgB = np.mean(img[:,:,blueChannel])
    if max(avgR,avgG,avgB) == avgR:
        maxchannel = img[:,:,redChannel]
    elif max(avgR,avgG,avgB) == avgG:
        maxchannel = img[:,:,greenChannel]
    else:
        maxchannel = img[:,:,blueChannel]
    
    unexposed_treatment_image_maxchannel = np.zeros([int(maxchannel.shape[0]),int(maxchannel.shape[1]) ,3])
    unexposed_treatment_image_maxchannel[:,:,0] = maxchannel
    unexposed_treatment_image_maxchannel[:,:,1] = maxchannel
    unexposed_treatment_image_maxchannel[:,:,2] = maxchannel
    return unexposed_treatment_image_maxchannel

def plot_projections(dose, stringcolor, stringgrafico, half_x, half_y, stringcolorgaussian, dpiResolution):
    dose_x, dose_y = projectionSingle(dose)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.title.set_text('X ' + stringcolor + ' Dose projection')
    ax1.set_ylabel('Projected signal')
    ax1.set_xlabel('X (mm)')
    ax1.plot(dose_x, stringgrafico)
    ax2.title.set_text('Y ' + stringcolor + ' Dose projection')
    ax2.set_ylabel('Projected signal')
    ax2.set_xlabel('Y (mm)')
    ax2.plot(dose_y, stringgrafico)
    find_fwhm_analytical(dose, half_x, half_y, stringcolor, dpiResolution)
    plt.show()
    
def dose_calculations(input_dose, color, bkgx3ch, bkgy3ch, multiChannelDosimetry, dimensioneRoiPixel):
    if color =='3ch':
        dose = input_dose.clip(min=0)
        dose_shapex = dose.shape[0]
        dose_shapey = dose.shape[1]
        dose_center = dose[int(dose_shapex/2) - int(dimensioneRoiPixel/2) : int(dose_shapex/2) + int(dimensioneRoiPixel/2),
                           int(dose_shapey/2) - int(dimensioneRoiPixel/2) : int(dose_shapey/2) + int(dimensioneRoiPixel/2)]
        bkgx=bkgx3ch
        bkgy=bkgy3ch
        maxd = np.max(dose)
        avg = np.mean(dose_center)
        mind = np.min(dose)  
        std = np.std(dose)
        half_maximum_x = (avg + bkgx3ch)/2
        half_maximum_y = (avg + bkgy3ch)/2
        print("3 CH DOSE AT CENTER WITH RECALIBRATION METHOD = %0.01f Gy" % (avg))
        print("3 CH DOSE STD AT CENTER WITH RECALIBRATION METHOD = %0.01f Gy" % (std), '\n') 
            
    else:
           
        # filtered_median = cv2.medianBlur(netImageChannel, ksize=3)
        # filtered = scipy.signal.wiener(filtered_median, (5,5))  
        # filtered = netImageChannel.clip(min=0)
        
        # if color == 'r':
        #     dose = inverse_recalibrated_multichannel_response_curve_red(filtered, a_red, b_red, fitResults)
        # elif color == 'g':
        #     dose = inverse_recalibrated_multichannel_response_curve_green(filtered, a_green, b_green, fitResults)
        # elif color == 'b':
        #     dose = inverse_recalibrated_multichannel_response_curve_blue(filtered, a_blue, b_blue, fitResults)
        # else:
        #     raise Exception("error no color recognized")
            
        dose = input_dose.clip(min=0)
        dose_shapex = dose.shape[0]
        dose_shapey = dose.shape[1]
        dose_center = dose[int(dose_shapex/2) - int(dimensioneRoiPixel/2) : int(dose_shapex/2) + int(dimensioneRoiPixel/2),
                           int(dose_shapey/2) - int(dimensioneRoiPixel/2) : int(dose_shapey/2) + int(dimensioneRoiPixel/2)]
        bkgx, bkgy, maxd, avg, mind, std, half_maximum_x, half_maximum_y = calculate_final_dose_statistics(dose, dose_center, dose_shapex, dose_shapey)
                            
        if color == 'r':
            if multiChannelDosimetry:
                print("RED CH DOSE AT CENTER WITH RECALIBRATION METHOD = %0.001f Gy" % (avg))
                print("RED CH STD DOSE WITH RECALIBRATION METHOD = %0.001f Gy" % (std), '\n')       
            else:
                print("RED CH DOSE AT CENTER WITH SINGLE CHANNEL METHOD = %0.01f Gy" % (avg))
                print("RED CH STD DOSE AT CENTER WITH SINGLE CHANNEL METHOD = %0.01f Gy" % (std), '\n') 

        elif color == 'g':
            if multiChannelDosimetry:
                print("GREEN CH DOSE AT CENTER WITH RECALIBRATION METHOD = %0.001f Gy" % (avg))
                print("GREEN CH STD DOSE AT CENTER WITH RECALIBRATION METHOD = %0.001f Gy" % (std), '\n')       
            else:
                print("GREEN CH DOSE AT CENTER WITH SINGLE CHANNEL METHOD = %0.01f Gy" % (avg))
                print("GREEN CH STD DOSE DOSIMETRY WITH SINGLE CHANNEL METHOD = %0.01f Gy" % (std), '\n') 

        elif color == 'b':
            if multiChannelDosimetry:
                print("BLUE CH DOSE AT CENTER WITH RECALIBRATION METHOD = %0.001f Gy" % (avg))
                print("BLUE CH STD DOSE WITH RECALIBRATION METHOD = %0.001f Gy" % (std), '\n')       
            else:
                print("BLUE CH DOSE AT CENTER WITH SINGLE CHANNEL METHOD = %0.01f Gy" % (avg))
                print("BLUE CH STD DOSE AT CENTER WITH SINGLE CHANNEL METHOD = %0.01f Gy" % (std), '\n') 

        else:
            raise Exception("error no color recognized")
    return mind, maxd, avg, std, half_maximum_x, half_maximum_y, dose_center, bkgx, bkgy


calibrationObjects = []
unexposedTreatmentObjects = []
maxDoseTreatmentObjects = []

redDosObjArr = []
greenDosObjArr = []
blueDosObjArr = []
trheechDosObjArr = []









