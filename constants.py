import glob as gb
import numpy as np
import sys

#variabili d'ambiente
# path= '/home/pcdti1/Scrivania/chromo/CHROMO/' #"C:/Users/Imalytics/Desktop/chromo/" # 

medianFilter = True
medianKernel = 3
wienerFilter = False
wienerKernel = 3

singleChannelDosimetry = False
if singleChannelDosimetry:
    multiChannelDosimetry = False
else:
    multiChannelDosimetry = True

plotProfilesResults = False

maximumIterationsFit = 100000 #numero massimo di iterazioni per fit

fitFunction = 'rational' #exponential
maxdoseRecalibration = 6 #DOSE MASSIMA DI RICALIBRAZIONE (Gy)

resolution = 25.4
dpi = 150
dpiResolution = resolution/dpi

dimRoiCalibration = 5 # roi per dose di calibrazione
dimensioneRoiPixel = 10 #es. 4=> 4x4

doseRawImageOutputFormat = 'tiff'
isodoseDifferenceGy = 0.1 #DIFFERENZA ISODOSI DI VISUALIZZAZIONE (Gy)
cmap = 'rainbow' #colore figure

redChannel=2 #ORDINE RGB
greenChannel=1 #ORDINE RGB
blueChannel=0 #ORDINE RGB

p0red = -10., 200., 3. #da cambiare eventualmente il punto iniziale
p0red1 = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0green = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0green1 = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0blue = -10., 300., 3. #da cambiare eventualmente il punto iniziale
p0blue1 = -10., 300., 3. #da cambiare eventualmente il punto iniziale

p0redexp = -10., 200., 3.  #da cambiare eventualmente il punto iniziale
p0red1exp = 100., 5., 0 #da cambiare eventualmente il punto iniziale
p0greenexp = 500., -500., 300 #da cambiare eventualmente il punto iniziale
p0green1exp = 100., 10., 30 #da cambiare eventualmente il punto iniziale
p0blueexp = 500., -150., 300 #da cambiare eventualmente il punto iniziale
p0blue1exp = 100., 5., 0 #da cambiare eventualmente il punto iniziale

a0multichannel = np.array([0, 1000, 5]) #da cambiare eventualmente il punto iniziale
a0multichannel1 = np.array([-10, 200, 3]) #da cambiare eventualmente il punto iniziale
