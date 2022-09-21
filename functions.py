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

sys.path.append(".")
from constants import *

from fitResultsSingleChannel import *

def cleanOutputDirectory(rootFolder):
    try:
        shutil.rmtree(os.path.join(rootFolder.dataPath, 'OUTPUT'))
    except:
        ...

def createOutputDirectories(rootFolder):
    try:
        os.mkdir(os.path.join(rootFolder.dataPath, 'OUTPUT'))
        os.mkdir(os.path.join(rootFolder.outputPath, '3CH'))
        os.mkdir(os.path.join(rootFolder.outputPath, 'BLUE'))
        os.mkdir(os.path.join(rootFolder.outputPath, 'GREEN'))
        os.mkdir(os.path.join(rootFolder.outputPath, 'RED'))
        os.mkdir(os.path.join(rootFolder.outputPath, '_CALIBRATION_FILTERED'))
        os.mkdir(os.path.join(rootFolder.outputPath, '_TREATMENT_FILTERED'))
    except:
        ...
        
def selectDirectory():
    global path
    browse = tk.Tk()
    browse.withdraw()
    browse.attributes('-topmost', True)
    path = filedialog.askdirectory(title='select root folder') + '/'
    return path
        
def insertFilteredImage(r, rootFolder, labelImage):
    filtered = ImageTk.PhotoImage(pilimage.open(rootFolder.treatment_list[0]).resize((500,500)))
    labelImage.configure(image=filtered)
    labelImage.photo = filtered
    print("updated image")    

def median(rootFolder, label, r, labelImage):
    cleanOutputDirectory(rootFolder)
    createOutputDirectories(rootFolder)
    print('Starting denoising of calibration images with median filter...')
    denoiserArg1 = '-d ' + rootFolder.nonFilteredCalibrationPath + ' -f median -k ' + str(medianKernel)
    os.system(rootFolder.denoiserPath + " " + denoiserArg1)
    for file in os.listdir(rootFolder.denoiserFolder):
        if(file.endswith(".tif")):
            move(file,rootFolder.calibrationPath)
    for file1 in os.listdir(rootFolder.path):
        if(file1.endswith(".tif")):
            move(file1,rootFolder.calibrationPath)
    
    print('Starting denoising of treatment images with median filter...')     
    denoiserArg2 = '-d ' + rootFolder.nonFilteredTreatmentPath + ' -f median -k ' + str(medianKernel)
    os.system(rootFolder.denoiserPath + " " + denoiserArg2)
    for file in os.listdir(rootFolder.denoiserFolder):
        if(file.endswith(".tif")):
            move(file,rootFolder.treatmentPath)
    for file1 in os.listdir(rootFolder.path):
        if(file1.endswith(".tif")):
            move(file1,rootFolder.treatmentPath)
            
    label.config(text="MEDIAN FILTER APPLIED")
    insertFilteredImage(r, rootFolder, labelImage)

def wiener(rootFolder, wienerCalibrationPath, wienerTreatmentPath, label, r, labelImage):
    print('Starting denoising of calibration images with wiener filter...')
    denoiserArg3 = '-d ' + wienerCalibrationPath + ' -f wiener -k ' + str(wienerKernel)
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
    denoiserArg4 = '-d ' + wienerTreatmentPath + ' -f wiener -k ' + str(wienerKernel)
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
    insertFilteredImage(r, rootFolder, labelImage)

def medianAndWiener(rootFolder, label, r, labelImage):
    cleanOutputDirectory(rootFolder)
    createOutputDirectories(rootFolder)
    median(rootFolder, label, r, labelImage)
    wiener(rootFolder, rootFolder.calibrationPath, rootFolder.treatmentPath, label, r, labelImage)
    
    label.config(text="WIENER AND MEDIAN FILTERS APPLIED")
    insertFilteredImage(r, rootFolder, labelImage)

def noDenoising(rootFolder, label, r, labelImage):
    cleanOutputDirectory(rootFolder)
    shutil.copytree(rootFolder.nonFilteredCalibrationPath,rootFolder.calibrationPath)
    shutil.copytree(rootFolder.nonFilteredTreatmentPath, rootFolder.treatmentPath)
    createOutputDirectories(rootFolder)
    label.config(text="NO FITLERS APPLIED")
    insertFilteredImage(r, rootFolder, labelImage)

    
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

def exponential_inverse(x, a, b, c):
    return (-b)*np.log((x-c)/a) #TODO ORA È SEMPLICE ESPONENZIALE MA DOVRESTI FARE L'INVERSA

def multichannel_model(a, x):
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

def calculateSingleChannelDose(y, fitResultsSingle):
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

def fitDataAndPlotCurves(calibration_dose, calibration_red, calibration_green, calibration_blue, rootFolder):
    
    d = np.linspace(np.min(calibration_dose), np.max(calibration_dose))
    r = np.linspace(np.min(calibration_red), np.max(calibration_red))
    g = np.linspace(np.min(calibration_green), np.max(calibration_green))
    b = np.linspace(np.min(calibration_blue), np.max(calibration_blue))
    x_max_lsmodel = 0 
    y_calibration_fit = []
    
    #RED CURVES
    if fitFunction == 'rational':
        poptRed = curve_fit(rational, calibration_dose, calibration_red, p0red, maxfev=maximumIterationsFit)[0]
        plt.plot(d, rational(d, *poptRed), 'r-', label='fitted ' + fitFunction + ' model')
    if fitFunction == 'exponential':
        poptRed = curve_fit(exponential, calibration_dose, calibration_red, p0redexp, maxfev=maximumIterationsFit)[0]
        plt.plot(d, exponential(d, *poptRed), 'r-', label='fitted ' + fitFunction + ' model')
    plt.scatter(calibration_dose, calibration_red, color='red', label='red data')
    plt.xlabel("DOSE (Gy)")
    plt.ylabel("PV")
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
    plt.xlabel("PV")
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
    plt.ylabel("PV")
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
    plt.xlabel("PV")
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
    plt.ylabel("PV")
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
    plt.xlabel("PV")
    plt.ylabel("DOSE (Gy)")
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.bluePath + "/response-dose_calibration_plot_blue.png", format='png')
    plt.show()
    
    fitResults = fitResultsSingleChannel(poptRedInverse, poptGreenInverse, poptBlueInverse)
    print(poptRedInverse)
    print(poptGreenInverse)
    print(poptBlueInverse)
    
    if multiChannelDosimetry:
        
        #MULTICHANNELCURVES
        xi = np.append(np.asanyarray(calibration_red), np.asanyarray(calibration_green))
        x = np.append(xi, np.asanyarray(calibration_blue))
        yi = np.append(np.asanyarray(calibration_dose), np.asanyarray(calibration_dose))
        y = np.append(yi, np.asanyarray(calibration_dose))
    
        fitResults_inv = least_squares(multichannel_function_inverse, a0multichannel, jac=jac_inverse, method='lm', args=(x, y), max_nfev=maximumIterationsFit*1000, verbose=1)
        fitResults_inv.x
    
        x_calibration_fit = np.linspace(min(x), max(x))
        y_calibration_fit = multichannel_model_inverse(fitResults_inv.x, x_calibration_fit)
        plt.scatter(calibration_red, calibration_dose, color='red', label='red data')
        plt.scatter(calibration_green, calibration_dose,color='green', label='green data')
        plt.scatter(calibration_blue, calibration_dose, color='blue', label='blue data')
        plt.plot(x_calibration_fit, y_calibration_fit, label='fitted multichannel LS model', ls='dashed')
        plt.xlabel("PV")
        plt.ylabel("DOSE (Gy)")
        plt.legend(loc='upper right')
        plt.savefig(rootFolder.tchPath + "/response-dose_calibration_plot_3ch.png", format='png')
        plt.show()
        
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
        plt.ylabel("PV")
        plt.legend(loc='upper right')
        plt.savefig(rootFolder.tchPath + "/dose-response_calibration_plot_3ch.png", format='png')
        plt.show()
    
    return fitResults, x_max_lsmodel, y_calibration_fit

def plotRecalibratedImages(x_max_lsmodel, unexposedObject, maxDoseObject, recalibrated_multichannel_response_curve_red, recalibrated_multichannel_response_curve_green, 
                           recalibrated_multichannel_response_curve_blue, y_calibration_fit, treatmentNumber, a_red, b_red, a_green, b_green, a_blue, b_blue, fitResults, rootFolder):
    x_calibration_fit = np.linspace(0, x_max_lsmodel)
    y_calibration_fit_red = recalibrated_multichannel_response_curve_red(x_calibration_fit, a_red, b_red, fitResults)
    y_calibration_fit_green = recalibrated_multichannel_response_curve_green(x_calibration_fit,a_green, b_green, fitResults)
    y_calibration_fit_blue = recalibrated_multichannel_response_curve_blue(x_calibration_fit,a_blue, b_blue, fitResults)
    plt.scatter(0, unexposedObject.calibrationRed, color='purple', label='red recalibration data')
    plt.scatter(0, unexposedObject.calibrationGreen, color='lime', label='green recalibration data')
    plt.scatter(0, unexposedObject.calibrationBlue, color='dodgerblue', label='blue recalibration data')
    plt.scatter(maxdoseRecalibration, maxDoseObject.calibrationRed, color='purple')
    plt.scatter(maxdoseRecalibration, maxDoseObject.calibrationGreen, color='lime')
    plt.scatter(maxdoseRecalibration, maxDoseObject.calibrationBlue, color='dodgerblue')
    plt.plot(x_calibration_fit, y_calibration_fit_red, 'purple', label='recalibrated RED ' + fitFunction + ' model')
    plt.plot(x_calibration_fit, y_calibration_fit_green, 'lime', label='recalibrated GREEN ' + fitFunction + ' model')
    plt.plot(x_calibration_fit, y_calibration_fit_blue, 'dodgerblue', label= 'recalibrated BLUE ' + fitFunction + ' model')
    plt.plot(x_calibration_fit, y_calibration_fit, label='fitted multichannel LS model', ls='dashed')
    plt.xlabel("DOSE (Gy)")
    plt.ylabel("PV")
    plt.legend(loc='upper right')
    plt.savefig(rootFolder.tchPath + "/dose-response_recalibrated_plot_" + "treatment_" + str(treatmentNumber + 1) + ".png", format='png')
    plt.show()

def calibration_factors_calculator(zeroResponse, maxdoseResponse, fitResults):
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

def find_fwhm_analytical(dose, halfvaluex, halfvaluey, stringColor):
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

def plot_dose(dose, max_red, max_green, max_blue, stringcolor, stringoutput, i, rootFolder):
    shape = np.shape(dose)
    x = np.arange(shape[1])*dpiResolution
    y = np.arange(shape[0])*dpiResolution
    xx, yy = np.meshgrid(x, y)
    levels = np.arange(0, int(math.ceil(max(max_red,max_green,max_blue)+3*isodoseDifferenceGy)), isodoseDifferenceGy)
    
    from PIL import Image
    doseImage = Image.fromarray(dose)
    doseImage.save(rootFolder.outputPath + stringoutput+ "_treatment_" +str(i+1) + "_raw." + doseRawImageOutputFormat)
        
    
    plt.figure()
    c = plt.contourf(xx, yy, dose, cmap=cmap, levels=levels)
    plt.colorbar(c, label="Dose (Gy)")
    plt.title(stringcolor + " dose")
    plt.xlabel("x (mm)")
    plt.ylabel("y (mm)")
    plt.axis("scaled")
    plt.grid(True)
    plt.savefig(rootFolder.outputPath + stringoutput + "_treatment_" + str(i+1) + "_figure.png", format='png')
    print("Dose image saved as: \n" + rootFolder.outputPath + stringoutput+ "_treatment_" + str(i+1) + "_raw." + doseRawImageOutputFormat + " \n" + rootFolder.outputPath + stringoutput+str(i) + "_figure.png \n")
    plt.show()

#TODO mettere a posto!!!
def calculatebkg(dose, dose_shapex, dose_shapey):
    bkgx = np.mean(dose[0 : int(dose_shapex), 0 : 5])
    bkgy = np.mean(dose[0 : 5, 0 : int(dose_shapey)])
    return bkgx, bkgy

def plot_projections(dose, stringcolor, stringgrafico, half_x, half_y, stringcolorgaussian):
    dose_x, dose_y = projectionSingle(dose)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.title.set_text('X ' + stringcolor + ' Dose projection')
    ax1.set_ylabel('Projected signal')
    ax1.set_xlabel('x (mm)')
    ax1.plot(dose_x, stringgrafico)
    ax2.title.set_text('Y ' + stringcolor + ' Dose projection')
    ax2.set_ylabel('Projected signal')
    ax2.set_xlabel('y (mm)')
    ax2.plot(dose_y, stringgrafico)
    find_fwhm_analytical(dose, half_x, half_y, stringcolor)
    plt.show()
    
def dose_calculations(input_dose, color, bkgx3ch, bkgy3ch):
    if color =='3ch':
        dose = input_dose.clip(min=0)
        dose_center = input_dose
        bkgx=bkgx3ch
        bkgy=bkgy3ch
        maxd = np.max(dose)
        avg = np.mean(dose)
        mind = np.min(dose)  
        std = np.std(dose)
        half_maximum_x = (avg + bkgx3ch)/2
        half_maximum_y = (avg + bkgy3ch)/2
        print("3 CHANNELS DOSIMETRY WITH RECALIBRATION METHOD: mean dose at center = %0.01f Gy" % (avg))
        print("3 CHANNELS DOSIMETRY WITH RECALIBRATION METHOD: standard deviation of dose = %0.01f Gy" % (std), '\n') 
            
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
                print("RED CHANNEL DOSIMETRY WITH RECALIBRATION METHOD: mean dose at center = %0.001f Gy" % (avg))
                print("RED CHANNEL DOSIMETRY WITH RECALIBRATION METHOD: standard deviation of dose = %0.001f Gy" % (std), '\n')       
            else:
                print("RED CHANNEL DOSIMETRY WITH SINGLE CHANNEL METHOD: mean dose at center = %0.01f Gy" % (avg))
                print("RED CHANNEL DOSIMETRY WITH SINGLE CHANNEL METHOD: standard deviation of dose = %0.01f Gy" % (std), '\n') 

        elif color == 'g':
            if multiChannelDosimetry:
                print("GREEN CHANNEL DOSIMETRY WITH RECALIBRATION METHOD: mean dose at center = %0.001f Gy" % (avg))
                print("GREEN CHANNEL DOSIMETRY WITH RECALIBRATION METHOD: standard deviation of dose = %0.001f Gy" % (std), '\n')       
            else:
                print("GREEN CHANNEL DOSIMETRY WITH SINGLE CHANNEL METHOD: mean dose at center = %0.01f Gy" % (avg))
                print("GREENCHANNEL DOSIMETRY WITH SINGLE CHANNEL METHOD: standard deviation of dose = %0.01f Gy" % (std), '\n') 

        elif color == 'b':
            if multiChannelDosimetry:
                print("BLUE CHANNEL DOSIMETRY WITH RECALIBRATION METHOD: mean dose at center = %0.001f Gy" % (avg))
                print("BLUE CHANNEL DOSIMETRY WITH RECALIBRATION METHOD: standard deviation of dose = %0.001f Gy" % (std), '\n')       
            else:
                print("BLUE CHANNEL DOSIMETRY WITH SINGLE CHANNEL METHOD: mean dose at center = %0.01f Gy" % (avg))
                print("BLUE CHANNEL DOSIMETRY WITH SINGLE CHANNEL METHOD: standard deviation of dose = %0.01f Gy" % (std), '\n') 

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






