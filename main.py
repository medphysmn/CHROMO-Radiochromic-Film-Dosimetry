#!/usr/bin/env python
# coding: utf-8

#TODO NET IMAGE - BKG - CORREZIONE LATERALE
import sys
import tkinter
import tkinter.ttk as ttk
from tkinter import filedialog

sys.path.append(".")
from functions import *
from rootFolderClass import *

widthTk = 1100
heightTk = 850
imagedim = 500
imagedimres = 432
imagedimresh = 288
imagedimcal = 400
imagedimcalh = 220

global path
path = selectDirectory() 
rootFolder = rootFolderClass(path)

chromoTk = tk.Toplevel()
chromoTk.title('CHROMO: Radiochromic Film Dosimetry Tool')
chromoTk.geometry(str(widthTk)+"x"+str(heightTk))
chromoTk.config(background = "white")
chromoTk.resizable(True, True)

tabsystem = ttk.Notebook(chromoTk)
denoiser = tk.Frame(tabsystem, width= widthTk, height= heightTk)
singleChannelTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
multiChannelTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
doseresultsTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
propertiesTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)
generalPropertiesTk = tk.Frame(tabsystem, width= widthTk, height= heightTk)

tabsystem.add(denoiser, text='Denoiser')
tabsystem.add(singleChannelTk, text='Single Channel Dosimetry')
tabsystem.add(multiChannelTk, text='Multi Channel Dosimetry')
tabsystem.add(doseresultsTk, text='Dose Results')
tabsystem.add(propertiesTk, text='Calibration Properties')
tabsystem.add(generalPropertiesTk, text='General Properties')
tabsystem.grid(column = 1, row = 0)

imageframe = tk.Frame(denoiser, width=imagedim, height=imagedim)
imageResized = pilimage.open("blank.jpg").resize((imagedim,imagedim))
img = itk.PhotoImage(imageResized)
labelImage = tk.Label(imageframe, image = img)

imageframeredcal = tk.Frame(singleChannelTk, width=imagedimcal, height=imagedimcal)
imageResizedredcal = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
imgredcal = itk.PhotoImage(imageResizedredcal)
labelImageredcal = tk.Label(imageframeredcal, image = imgredcal)

imageframegreencal = tk.Frame(singleChannelTk, width=imagedimcal, height=imagedimcal)
imageResizedgreencal = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
imggreencal = itk.PhotoImage(imageResizedgreencal)
labelImagegreencal = tk.Label(imageframegreencal, image = imggreencal)

imageframebluecal = tk.Frame(singleChannelTk, width=imagedimcal, height=imagedimcal)
imageResizedbluecal = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
imgbluecal = itk.PhotoImage(imageResizedbluecal)
labelImagebluecal = tk.Label(imageframebluecal, image = imgbluecal)



imageframeredcal1 = tk.Frame(multiChannelTk, width=imagedimcal, height=imagedimcal)
imageResizedredcal1 = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
imgredcal1 = itk.PhotoImage(imageResizedredcal1)
labelImageredcal1 = tk.Label(imageframeredcal1, image = imgredcal1)

imageframegreencal1 = tk.Frame(multiChannelTk, width=imagedimcal, height=imagedimcal)
imageResizedgreencal1 = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
imggreencal1 = itk.PhotoImage(imageResizedgreencal1)
labelImagegreencal1 = tk.Label(imageframegreencal1, image = imggreencal1)

imageframebluecal1 = tk.Frame(multiChannelTk, width=imagedimcal, height=imagedimcal)
imageResizedbluecal1 = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
imgbluecal1 = itk.PhotoImage(imageResizedbluecal1)
labelImagebluecal1 = tk.Label(imageframebluecal1, image = imgbluecal1)

imageframe3chcal1 = tk.Frame(multiChannelTk, width=imagedimcal, height=imagedimcal)
imageResized3chcal1 = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
img3chcal1 = itk.PhotoImage(imageResized3chcal1)
labelImage3chcal1 = tk.Label(imageframe3chcal1, image = img3chcal1)

imageframe3chcalRecal1 = tk.Frame(multiChannelTk, width=imagedimcal, height=imagedimcal)
imageResized3chcalRecal1 = pilimage.open("blankres.jpg").resize((imagedimcal,imagedimcalh))
img3chcalRecal1 = itk.PhotoImage(imageResized3chcalRecal1)
labelImage3chcalRecal1 = tk.Label(imageframe3chcalRecal1, image = img3chcalRecal1)

imageframeredres = tk.Frame(doseresultsTk, width=imagedimres, height=imagedimres)
imageResizedredres = pilimage.open("blankres.jpg").resize((imagedimres,imagedimresh))
imgredres = itk.PhotoImage(imageResizedredres)
labelImageredres = tk.Label(imageframeredres, image = imgredres)

imageframegreenres = tk.Frame(doseresultsTk, width=imagedimres, height=imagedimres)
imageResizedgreenres = pilimage.open("blankres.jpg").resize((imagedimres,imagedimresh))
imggreenres = itk.PhotoImage(imageResizedgreenres)
labelImagegreenres = tk.Label(imageframegreenres, image = imggreenres)

imageframeblueres = tk.Frame(doseresultsTk, width=imagedimres, height=imagedimres)
imageResizedblueres = pilimage.open("blankres.jpg").resize((imagedimres,imagedimresh))
imgblueres = itk.PhotoImage(imageResizedblueres)
labelImageblueres = tk.Label(imageframeblueres, image = imgblueres)

imageframe3chres = tk.Frame(doseresultsTk, width=imagedimres, height=imagedimres)
imageResized3chres = pilimage.open("blankres.jpg").resize((imagedimres,imagedimresh))
img3chres = itk.PhotoImage(imageResized3chres)
labelImage3chres = tk.Label(imageframe3chres, image = img3chres)

label_denoising = tk.Label(denoiser, text="CHOOSE ONE OPTION TO LOAD \n AND DENOISE CALIBRATION AND \n TREATMENT IMAGES:", fg="blue", font=("Arial", 15), width=35)
# label_treatmentImage = tk.Label(denoiser, text="FILTERED RADIOCHROMIC FILM", font=("Arial", 10))

tk.Label(denoiser, text="Enter Median Kernel:", font=("Arial")).grid(column = 1, row = 8, pady=5)
medinalval = tk.IntVar(denoiser, value=3)
medianKernelTk=tk.Entry(denoiser, width=80, textvariable=medinalval)

tk.Label(denoiser, text="Enter Wiener Kernel:", font=("Arial")).grid(column = 1, row = 10)
wienerval = tk.IntVar(denoiser, value=3)
wienerKernelTk=tk.Entry(denoiser, width=80, textvariable=wienerval)

imageframe.grid(column = 2, row = 3, padx=40, pady=80, rowspan=5)
labelImage.grid(column = 2, row = 3, padx=40)
medianKernelTk.grid(column = 2, row = 8, padx=40)
wienerKernelTk.grid(column = 2, row = 10, padx=40)
label_denoising.grid(column = 1, row = 3, padx=40, pady=10)
# label_treatmentImage.grid(column = 2, row = 3, padx=10, pady=10)

imageframeredcal.grid(column = 2, row = 2, padx=30, pady=10)
labelImageredcal.grid(column = 2, row = 2, padx=30, pady=10)
imageframegreencal.grid(column = 1, row = 3, padx=30, pady=10)
labelImagegreencal.grid(column = 1, row = 3, padx=30, pady=10)
imageframebluecal.grid(column = 2, row = 3, padx=30, pady=10)
labelImagebluecal.grid(column = 2, row = 3, padx=30, pady=10)

imageframeredcal1.grid(column = 2, row = 2, padx=30, pady=3)
labelImageredcal1.grid(column = 2, row = 2, padx=30, pady=3)
imageframegreencal1.grid(column = 1, row = 3, padx=30, pady=3)
labelImagegreencal1.grid(column = 1, row = 3, padx=30, pady=3)
imageframebluecal1.grid(column = 2, row = 3, padx=30, pady=3)
labelImagebluecal1.grid(column = 2, row = 3, padx=30, pady=3)
imageframe3chcal1.grid(column = 1, row = 4, padx=30, pady=3)
labelImage3chcal1.grid(column = 1, row = 4, padx=30, pady=3)
imageframe3chcalRecal1.grid(column = 2, row = 4, padx=30, pady=3)
labelImage3chcalRecal1.grid(column = 2, row = 4, padx=30, pady=3)

imageframeredres.grid(column = 0, row = 1, padx=25, pady=20)
labelImageredres.grid(column = 0, row = 1, padx=25, pady=20)
imageframegreenres.grid(column = 1, row = 1, padx=25, pady=20)
labelImagegreenres.grid(column = 1, row = 1, padx=25, pady=20)
imageframeblueres.grid(column = 0, row = 2, padx=25, pady=20)
labelImageblueres.grid(column = 0, row = 2, padx=25, pady=20)
imageframe3chres.grid(column = 1, row = 2, padx=25, pady=20)
labelImage3chres.grid(column = 1, row = 2, padx=25, pady=20)

denoisingval = tk.StringVar(singleChannelTk, value='none')
button_median = tk.Radiobutton(denoiser, text = "DENOISE CALIBRATION AND TEST FILMS WITH MEDIAN FILTER", variable=denoisingval,value="m",
                       command = lambda: median(rootFolder, label_denoising,denoiser, labelImage, medianKernelTk)).grid(column = 1, row = 4, padx=10, pady=5)
button_wiener = tk.Radiobutton(denoiser, text = "DENOISE CALIBRATION AND TEST FILMS WITH WIENER FILTER", variable=denoisingval,value="w",
                       command = lambda: wiener(rootFolder, rootFolder.nonFilteredCalibrationPath, rootFolder.nonFilteredTreatmentPath, label_denoising,denoiser, labelImage, True, wienerKernelTk)).grid(column = 1, row = 5, padx=10, pady=5)
button_medianandwiener = tk.Radiobutton(denoiser, text = "DENOISE CALIBRATION AND TEST FILMS WITH WIENER AND MEDIAN FILTER", variable=denoisingval,value="w e m",
                                command = lambda: medianAndWiener(rootFolder, label_denoising, denoiser, labelImage,medianKernelTk ,wienerKernelTk)).grid(column = 1, row = 6, padx=10, pady=5)
button_no_denoising = tk.Radiobutton(denoiser, text = "DON'T USE ANY FILTER ", variable=denoisingval,value="no filter",
                             command = lambda: noDenoising(rootFolder, label_denoising, denoiser, labelImage)).grid(column = 1, row = 7, padx=10, pady=5)

fittingfunctionselected = "rational"
def selected():
    global fittingfunctionselected
    fittingfunctionselected = fittingval.get()

tk.Label(multiChannelTk, text="Maximum recalibration dose:", font=("Arial")).grid(column = 1, row = 0, padx=30, pady=10)
recval = tk.IntVar(multiChannelTk, value=6)
recvalTk=tk.Entry(multiChannelTk, width=10, textvariable=recval)
recvalTk.grid(column = 2, row = 0, pady=10)

tk.Label(singleChannelTk, text="Choose one fitting function:", font=("Arial")).grid(column = 1, row = 0, pady=50, padx=10,rowspan=2)
fittingval = tk.StringVar(singleChannelTk, value='rational')
fittingFunctionTk = tk.Radiobutton(singleChannelTk, text="rational", variable=fittingval, value="rational", command=selected)
fittingFunction1Tk = tk.Radiobutton(singleChannelTk, text="exponential", padx = 20,variable=fittingval, value="exponential", command=selected)

fittingFunctionTk.grid(column = 2, row = 0)
fittingFunction1Tk.grid(column = 2, row = 1)

label_rational = tk.Label(propertiesTk, text="RATIONAL FUNCTION: \n f(x)= a + b/(x+c)", fg="blue", font=("Arial", 15)).grid(column = 1, row = 1, pady=10)
label_rational = tk.Label(propertiesTk, text="Initial values for optimization", fg="blue", font=("Arial", 15)).grid(column = 4, row = 1, pady=10)

tk.Label(propertiesTk, text="a_RED:", font=("Arial")).grid(column = 1, row = 2)
p0redval = tk.DoubleVar(propertiesTk, value=-10.)
p0redTk=tk.Entry(propertiesTk, width=10, textvariable=p0redval)
p0redTk.grid(column = 2, row = 2)

tk.Label(propertiesTk, text="b_RED:", font=("Arial")).grid(column = 1, row = 3)
p1redval = tk.DoubleVar(propertiesTk, value=200.)
p1redTk=tk.Entry(propertiesTk, width=10, textvariable=p1redval)
p1redTk.grid(column = 2, row = 3)

tk.Label(propertiesTk, text="c_RED:", font=("Arial")).grid(column = 1, row = 4)
p2redval = tk.DoubleVar(propertiesTk, value=3.)
p2redTk=tk.Entry(propertiesTk, width=10, textvariable=p2redval)
p2redTk.grid(column = 2, row = 4)

tk.Label(propertiesTk, text="a_RED_inverse:", font=("Arial")).grid(column = 4, row = 2)
pinv0redval = tk.DoubleVar(propertiesTk, value=-10.)
pinv0redTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0redval)
pinv0redTk.grid(column = 5, row = 2)

tk.Label(propertiesTk, text="b_RED_inverse:", font=("Arial")).grid(column = 4, row = 3)
pinv1redval = tk.DoubleVar(propertiesTk, value=300.)
pinv1redTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1redval)
pinv1redTk.grid(column = 5, row = 3)

tk.Label(propertiesTk, text="c_RED_inverse:", font=("Arial")).grid(column = 4, row = 4)
pinv2redval = tk.DoubleVar(propertiesTk, value=3.)
pinv2redTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2redval)
pinv2redTk.grid(column = 5, row = 4)

tk.Label(propertiesTk, text="a_GREEN:", font=("Arial")).grid(column = 1, row = 5)
p0greenval = tk.DoubleVar(propertiesTk, value=-10.)
p0greenTk=tk.Entry(propertiesTk, width=10, textvariable=p0greenval)
p0greenTk.grid(column = 2, row = 5)

tk.Label(propertiesTk, text="b_GREEN:", font=("Arial")).grid(column = 1, row = 6)
p1greenval = tk.DoubleVar(propertiesTk, value=300.)
p1greenTk=tk.Entry(propertiesTk, width=10, textvariable=p1greenval)
p1greenTk.grid(column = 2, row = 6)

tk.Label(propertiesTk, text="c_GREEN:", font=("Arial")).grid(column = 1, row = 7)
p2greenval = tk.DoubleVar(propertiesTk, value=3.)
p2greenTk=tk.Entry(propertiesTk, width=10, textvariable=p2greenval)
p2greenTk.grid(column = 2, row = 7)

tk.Label(propertiesTk, text="a_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 5)
pinv0greenval = tk.DoubleVar(propertiesTk, value=-10.)
pinv0greenTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0greenval)
pinv0greenTk.grid(column = 5, row = 5)

tk.Label(propertiesTk, text="b_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 6)
pinv1greenval = tk.DoubleVar(propertiesTk, value=-300.)
pinv1greenTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1greenval)
pinv1greenTk.grid(column = 5, row = 6)

tk.Label(propertiesTk, text="c_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 7)
pinv2greenval = tk.DoubleVar(propertiesTk, value=3.)
pinv2greenTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2greenval)
pinv2greenTk.grid(column = 5, row = 7)

tk.Label(propertiesTk, text="a_BLUE:", font=("Arial")).grid(column = 1, row = 8)
p0blueval = tk.DoubleVar(propertiesTk, value=-10.)
p0blueTk=tk.Entry(propertiesTk, width=10, textvariable=p0blueval)
p0blueTk.grid(column = 2, row = 8)

tk.Label(propertiesTk, text="b_BLUE:", font=("Arial")).grid(column = 1, row = 9)
p1blueval = tk.DoubleVar(propertiesTk, value=300.)
p1blueTk=tk.Entry(propertiesTk, width=10, textvariable=p1blueval)
p1blueTk.grid(column = 2, row = 9)

tk.Label(propertiesTk, text="c_BLUE:", font=("Arial")).grid(column = 1, row = 10)
p2blueval = tk.DoubleVar(propertiesTk, value=3.)
p2blueTk=tk.Entry(propertiesTk, width=10, textvariable=p2blueval)
p2blueTk.grid(column = 2, row = 10)

tk.Label(propertiesTk, text="a_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 8)
pinv0blueval = tk.DoubleVar(propertiesTk, value=-10.)
pinv0blueTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0blueval)
pinv0blueTk.grid(column = 5, row = 8)

tk.Label(propertiesTk, text="b_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 9)
pinv1blueval = tk.DoubleVar(propertiesTk, value=300.)
pinv1blueTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1blueval)
pinv1blueTk.grid(column = 5, row = 9)

tk.Label(propertiesTk, text="c_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 10)
pinv2blueval = tk.DoubleVar(propertiesTk, value=3.)
pinv2blueTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2blueval)
pinv2blueTk.grid(column = 5, row = 10)

label_exponential = tk.Label(propertiesTk, text="EXPONENTIAL FUNCTION: \n f(x)= a*exp(-x/b) + c", fg="blue", font=("Arial", 15)).grid(column = 1, row = 11, pady=10)
label_exponential = tk.Label(propertiesTk, text="Initial values for optimization", fg="blue", font=("Arial", 15)).grid(column = 4, row = 11, pady=10)

tk.Label(propertiesTk, text="a_RED:", font=("Arial")).grid(column = 1, row = 12)
p0redexpval = tk.DoubleVar(propertiesTk, value=-10.)
p0redexpTk=tk.Entry(propertiesTk, width=10, textvariable=p0redexpval)
p0redexpTk.grid(column = 2, row = 12)

tk.Label(propertiesTk, text="b_RED:", font=("Arial")).grid(column = 1, row = 13)
p1redexpval = tk.DoubleVar(propertiesTk, value=200.)
p1redexpTk=tk.Entry(propertiesTk, width=10, textvariable=p1redexpval)
p1redexpTk.grid(column = 2, row = 13)

tk.Label(propertiesTk, text="c_RED:", font=("Arial")).grid(column = 1, row = 14)
p2redexpval = tk.DoubleVar(propertiesTk, value=3.)
p2redexpTk=tk.Entry(propertiesTk, width=10, textvariable=p2redexpval)
p2redexpTk.grid(column = 2, row = 14)

tk.Label(propertiesTk, text="a_RED_inverse:", font=("Arial")).grid(column = 4, row = 12)
pinv0redexpval = tk.DoubleVar(propertiesTk, value=100.)
pinv0redexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0redexpval)
pinv0redexpTk.grid(column = 5, row = 12)

tk.Label(propertiesTk, text="b_RED_inverse:", font=("Arial")).grid(column = 4, row = 13)
pinv1redexpval = tk.DoubleVar(propertiesTk, value=5.)
pinv1redexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1redexpval)
pinv1redexpTk.grid(column = 5, row = 13)

tk.Label(propertiesTk, text="c_RED_inverse:", font=("Arial")).grid(column = 4, row = 14)
pinv2redexpval = tk.DoubleVar(propertiesTk, value=0.)
pinv2redexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2redexpval)
pinv2redexpTk.grid(column = 5, row = 14)

tk.Label(propertiesTk, text="a_GREEN:", font=("Arial")).grid(column = 1, row = 15)
p0greenexpval = tk.DoubleVar(propertiesTk, value=500.)
p0greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=p0greenexpval)
p0greenexpTk.grid(column = 2, row = 15)

tk.Label(propertiesTk, text="b_GREEN:", font=("Arial")).grid(column = 1, row = 16)
p1greenexpval = tk.DoubleVar(propertiesTk, value=-500.)
p1greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=p1greenexpval)
p1greenexpTk.grid(column = 2, row = 16)

tk.Label(propertiesTk, text="c_GREEN:", font=("Arial")).grid(column = 1, row = 17)
p2greenexpval = tk.DoubleVar(propertiesTk, value=300.)
p2greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=p2greenexpval)
p2greenexpTk.grid(column = 2, row = 17)

tk.Label(propertiesTk, text="a_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 15)
pinv0greenexpval = tk.DoubleVar(propertiesTk, value=100.)
pinv0greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0greenexpval)
pinv0greenexpTk.grid(column = 5, row = 15)

tk.Label(propertiesTk, text="b_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 16)
pinv1greenexpval = tk.DoubleVar(propertiesTk, value=10.)
pinv1greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1greenexpval)
pinv1greenexpTk.grid(column = 5, row = 16)

tk.Label(propertiesTk, text="c_GREEN_inverse:", font=("Arial")).grid(column = 4, row = 17)
pinv2greenexpval = tk.DoubleVar(propertiesTk, value=30.)
pinv2greenexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2greenexpval)
pinv2greenexpTk.grid(column = 5, row = 17)

tk.Label(propertiesTk, text="a_BLUE:", font=("Arial")).grid(column = 1, row = 18)
p0blueexpval = tk.DoubleVar(propertiesTk, value=500.)
p0blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=p0blueexpval)
p0blueexpTk.grid(column = 2, row = 18)

tk.Label(propertiesTk, text="b_BLUE:", font=("Arial")).grid(column = 1, row = 19)
p1blueexpval = tk.DoubleVar(propertiesTk, value=-150.)
p1blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=p1blueexpval)
p1blueexpTk.grid(column = 2, row = 19)

tk.Label(propertiesTk, text="c_BLUE:", font=("Arial")).grid(column = 1, row = 20)
p2blueexpval = tk.DoubleVar(propertiesTk, value=300.)
p2blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=p2blueexpval)
p2blueexpTk.grid(column = 2, row = 20)

tk.Label(propertiesTk, text="a_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 18)
pinv0blueexpval = tk.DoubleVar(propertiesTk, value=100.)
pinv0blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv0blueexpval)
pinv0blueexpTk.grid(column = 5, row = 18)

tk.Label(propertiesTk, text="b_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 19)
pinv1blueexpval = tk.DoubleVar(propertiesTk, value=5.)
pinv1blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv1blueexpval)
pinv1blueexpTk.grid(column = 5, row = 19)

tk.Label(propertiesTk, text="c_BLUE_inverse:", font=("Arial")).grid(column = 4, row = 20)
pinv2blueexpval = tk.DoubleVar(propertiesTk, value=0.)
pinv2blueexpTk=tk.Entry(propertiesTk, width=10, textvariable=pinv2blueexpval)
pinv2blueexpTk.grid(column = 5, row = 20)

label_exponential = tk.Label(propertiesTk, text="MULTICHANNEL CALIBRATION", fg="blue", font=("Arial", 15)).grid(column = 1, row = 21, padx=60, pady=10)
label_exponential = tk.Label(propertiesTk, text="Initial values for optimization", fg="blue", font=("Arial", 15)).grid(column = 4, row = 21, padx=90, pady=10)

tk.Label(propertiesTk, text="a_MC:", font=("Arial")).grid(column = 1, row = 22)
a0mcvalval = tk.DoubleVar(propertiesTk, value=0.)
a0mcTk=tk.Entry(propertiesTk, width=10, textvariable=a0mcvalval)
a0mcTk.grid(column = 2, row = 22)

tk.Label(propertiesTk, text="b_MC:", font=("Arial")).grid(column = 1, row = 23)
a1mcvalval = tk.DoubleVar(propertiesTk, value=1000.)
a1mcTk=tk.Entry(propertiesTk, width=10, textvariable=a1mcvalval)
a1mcTk.grid(column = 2, row = 23)

tk.Label(propertiesTk, text="c_MC:", font=("Arial")).grid(column = 1, row = 24)
a2mcvalval = tk.DoubleVar(propertiesTk, value=5.)
a2mcTk=tk.Entry(propertiesTk, width=10, textvariable=a2mcvalval)
a2mcTk.grid(column = 2, row = 24)

tk.Label(propertiesTk, text="a_MC_inverse:", font=("Arial")).grid(column = 4, row = 22)
a0invmcvalval = tk.DoubleVar(propertiesTk, value=0.)
a0invmcTk=tk.Entry(propertiesTk, width=10, textvariable=a0invmcvalval)
a0invmcTk.grid(column = 5, row = 22)

tk.Label(propertiesTk, text="b_MC_inverse:", font=("Arial")).grid(column = 4, row = 23)
a1invmcvalval = tk.DoubleVar(propertiesTk, value=1000.)
a1invmcTk=tk.Entry(propertiesTk, width=10, textvariable=a1mcvalval)
a1invmcTk.grid(column = 5, row = 23)

tk.Label(propertiesTk, text="c_MC_inverse:", font=("Arial")).grid(column = 4, row = 24)
a2invmcvalval = tk.DoubleVar(propertiesTk, value=5.)
a2invmcTk=tk.Entry(propertiesTk, width=10, textvariable=a2invmcvalval)
a2invmcTk.grid(column = 5, row = 24)

tk.Label(propertiesTk, text="Maximum number of fit iterations:", font=("Arial")).grid(column = 1, row = 0, pady=10)
maxitval = tk.IntVar(propertiesTk, value=100000)
maxitvalTk=tk.Entry(propertiesTk, width=10, textvariable=maxitval)
maxitvalTk.grid(column = 2, row = 0)

# tk.Label(propertiesTk, text="Maximum recalibration dose:", font=("Arial")).grid(column = 4, row = 0)
# recval = tk.IntVar(propertiesTk, value=6)
# recvalTk=tk.Entry(propertiesTk, width=10, textvariable=recval)
# recvalTk.grid(column = 5, row = 0)

tk.Label(generalPropertiesTk, text="Scanner resolution (mm):", font=("Arial")).grid(column = 1, row = 0, padx=80)
resval = tk.DoubleVar(generalPropertiesTk, value=25.4)
resvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=resval)
resvalTk.grid(column = 2, row = 0, padx=50, pady=10)

tk.Label(generalPropertiesTk, text="Dots Per Inch (DPI):", font=("Arial")).grid(column = 1, row = 1, padx=80)
dpival = tk.IntVar(generalPropertiesTk, value=150)
dpivalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=dpival)
dpivalTk.grid(column = 2, row = 1, padx=50, pady=10)

tk.Label(generalPropertiesTk, text="Red channel index:", font=("Arial")).grid(column = 3, row = 0, padx=80)
redchval = tk.IntVar(generalPropertiesTk, value=2)
redchvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=redchval)
redchvalTk.grid(column = 4, row = 0, padx=50, pady=10)

tk.Label(generalPropertiesTk, text="Green channel index:", font=("Arial")).grid(column = 3, row = 1, padx=80)
greenchval = tk.IntVar(generalPropertiesTk, value=1)
greenchvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=greenchval)
greenchvalTk.grid(column = 4, row = 1, padx=50, pady=10)

tk.Label(generalPropertiesTk, text="Blue channel index:", font=("Arial")).grid(column = 3, row = 2, padx=80)
bluechval = tk.IntVar(generalPropertiesTk, value=0)
bluechvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=bluechval)
bluechvalTk.grid(column = 4, row = 2, padx=50, pady=10)

tk.Label(generalPropertiesTk, text="Calibration Roi dimension:", font=("Arial")).grid(column = 1, row = 2, padx=80)
calroidimval = tk.IntVar(generalPropertiesTk, value=5)
calroidimvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=calroidimval)
calroidimvalTk.grid(column = 2, row = 2, padx=50, pady=10)

# tk.Label(generalPropertiesTk, text="Central Roi dimension for dose statistics calculation (pixels):", font=("Arial")).grid(column = 1, row = 3, padx=30, pady=10)
# dimRoiCalibrationval = tk.IntVar(generalPropertiesTk, value=10)
# dimRoiCalibrationvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=dimRoiCalibrationval)
# dimRoiCalibrationvalTk.grid(column = 2, row = 3, padx=50, pady=10)

tk.Label(generalPropertiesTk, text="Isodose difference in Gy:", font=("Arial")).grid(column = 1, row = 4, padx=80)
isodoseDifferenceGyval = tk.DoubleVar(generalPropertiesTk, value=0.1)
isodoseDifferenceGyvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=isodoseDifferenceGyval)
isodoseDifferenceGyvalTk.grid(column = 2, row = 4, padx=50, pady=10)


tk.Label(generalPropertiesTk, text="Raw dose image output format:", font=("Arial")).grid(column = 1, row = 6, padx=50)
doseRawImageOutputFormatval = tk.StringVar(generalPropertiesTk, value='tiff')
doseRawImageOutputFormatvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=doseRawImageOutputFormatval)
doseRawImageOutputFormatvalTk.grid(column = 2, row = 6, padx=50, pady=10)

tk.Label(generalPropertiesTk, text="Dose plots color map:", font=("Arial")).grid(column = 1, row = 7, padx=80)
cmapval = tk.StringVar(generalPropertiesTk, value='rainbow')
cmapvalTk=tk.Entry(generalPropertiesTk, width=10, textvariable=cmapval)
cmapvalTk.grid(column = 2, row = 7, padx=50, pady=10)

resultfoderbutton = tk.Button(doseresultsTk, text="OPEN RESULT FOLDER", command= lambda: openresultfolder(rootFolder))
resultfoderbutton.grid(row=0, column=0, pady=27, columnspan=2)


button_singleCalibrtion = tk.Button(singleChannelTk, text = "START SINGLE CHANNEL CALIBRATION AND DOSIMETRY", command = lambda: singleChannelDosimetryGUI(rootFolder, 
                                                                                fittingfunctionselected, 
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
                                                                                10, 
                                                                                int(calroidimvalTk.get()), 
                                                                                int(redchvalTk.get()), 
                                                                                int(greenchvalTk.get()), 
                                                                                int(bluechvalTk.get()), 
                                                                                float(resvalTk.get()), 
                                                                                float(dpivalTk.get()), 
                                                                                (float(resvalTk.get())/float(dpivalTk.get())),
                                                                                0,
                                                                                doseresultsTk, 
                                                                                labelImageredres,
                                                                                labelImagegreenres, 
                                                                                labelImageblueres,
                                                                                singleChannelTk,
                                                                                labelImageredcal,
                                                                                labelImagegreencal,
                                                                                labelImagebluecal
                                                                                )).grid(column = 1, row = 2 , padx=10, pady=10)


button_multichannelCalibration = tk.Button(multiChannelTk, text = "START MULTI-CHANNEL CALIBRATION AND DOSIMETRY", command = lambda: multiChannelDosimetryGUI(rootFolder, 
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
                                                                               10, 
                                                                               int(calroidimvalTk.get()), 
                                                                               int(redchvalTk.get()), 
                                                                               int(greenchvalTk.get()), 
                                                                               int(bluechvalTk.get()), 
                                                                               float(resvalTk.get()), 
                                                                               float(dpivalTk.get()), 
                                                                               (float(resvalTk.get())/float(dpivalTk.get())),
                                                                               0,
                                                                               doseresultsTk,
                                                                               labelImageredres,
                                                                               labelImagegreenres, 
                                                                               labelImageblueres, 
                                                                               labelImage3chres,
                                                                               multiChannelTk,
                                                                               labelImageredcal1,
                                                                               labelImagegreencal1,
                                                                               labelImagebluecal1,
                                                                               labelImage3chcal1,
                                                                               labelImage3chcalRecal1)).grid(column = 1, row = 2 , padx=10, pady=10)





chromoTk.mainloop()
